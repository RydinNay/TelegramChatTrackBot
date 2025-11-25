import asyncio
from datetime import datetime

from aiogram.types import FSInputFile
import nest_asyncio

from tg_bot.bot_instance import bot
from config import CHANNEL
from celery_app.celery_config import app
from database.db_services import UserService
from services.report_constuctor import generate_pdf

# Логгер
from logger_config import setup_logger
logger = setup_logger(__name__, log_file="celery_tasks.log")

nest_asyncio.apply()


@app.task
def make_report(date_from: str = None, date_to: str = None):
    async def async_logic():
        logger.info("Запуск задачи make_report()")

        try:
            admins = await bot.get_chat_administrators(chat_id=f"{CHANNEL}")
            admin_ids = [adm.user.id for adm in admins]
            logger.info(f"Найдено админов: {len(admin_ids)}")
        except Exception as e:
            logger.error(f"Ошибка получения администраторов: {e}")
            return

        df = datetime.fromisoformat(date_from) if date_from else None
        dt = datetime.fromisoformat(date_to) if date_to else None

        try:
            data = await UserService.get_report_data(date_from=df, date_to=dt)
            logger.info("Данные для отчёта успешно получены.")
        except Exception as e:
            logger.error(f"Ошибка при получении данных отчёта: {e}")
            return

        sources_rows = data["sources"]
        totals = data["totals"]

        if df and dt:
            period_text = f"Период: {df.date()} — {dt.date()}"
        elif df:
            period_text = f"С {df.date()} по сегодня"
        elif dt:
            period_text = f"До {dt.date()}"
        else:
            period_text = "За всё время"

        filename = "users_report.pdf"

        try:
            generate_pdf(
                filename=filename,
                title="Отчёт по источникам пользователей",
                period_text=period_text,
                report_rows=sources_rows,
                unsubscribed_count=totals["unsubscribed"],
                active_users_count=totals["active"],
                total_count=totals["total"]
            )
            logger.info(f"PDF отчет '{filename}' успешно создан.")
        except Exception as e:
            logger.error(f"Ошибка создания PDF: {e}")
            return

        file = FSInputFile(filename)

        for admin_id in admin_ids:
            try:
                await bot.send_document(chat_id=admin_id, document=file)
                logger.info(f"PDF успешно отправлен админу {admin_id}")
            except Exception as e:
                logger.error(f"Не удалось отправить PDF администратору {admin_id}: {e}")

    asyncio.run(async_logic())


@app.task
def check_subscriptions_task():
    async def check_subscriptions():
        logger.info("Запуск задачи check_subscriptions_task()")

        try:
            active_users = await UserService.get_active_users()
            logger.info(f"Активных пользователей: {len(active_users)}")
        except Exception as e:
            logger.error(f"Ошибка получения списка активных пользователей: {e}")
            return

        to_deactivate = []

        for user in active_users:
            try:
                member = await bot.get_chat_member(f"{CHANNEL}", user.tg_id)

                if member.status in ['left', 'kicked']:
                    to_deactivate.append(user.id)
                    logger.info(f"Пользователь {user.tg_id} больше не подписан")

            except Exception as e:
                to_deactivate.append(user.id)
                logger.warning(f"Ошибка проверки {user.tg_id}, добавлен в деактивацию: {e}")

        if to_deactivate:
            try:
                await UserService.deactivate_users(to_deactivate)
                logger.info(f"Пользователи деактивированы: {len(to_deactivate)}")
            except Exception as e:
                logger.error(f"Ошибка деактивации пользователей: {e}")
        else:
            logger.info("Все пользователи активны.")

        logger.info(f"✔ Проверка завершена. Неактивных: {len(to_deactivate)}")

    asyncio.run(check_subscriptions())
