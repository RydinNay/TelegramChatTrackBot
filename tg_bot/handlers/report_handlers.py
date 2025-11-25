from aiogram import types, Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from datetime import datetime

report_command_router = Router()

class ReportStates(StatesGroup):
    waiting_start_date = State()
    waiting_end_date = State()


def validate_date(date_text: str) -> str | None:
    try:
        datetime.strptime(date_text, "%Y-%m-%d")
        return date_text
    except ValueError:
        return None


@report_command_router.callback_query(lambda c: c.data == "get_report")
async def process_report_button(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.answer(
        "Введите начальную дату в формате YYYY-MM-DD или оставьте пустым для всего периода:"
    )
    await state.set_state(ReportStates.waiting_start_date)
    await callback.answer()


@report_command_router.message(ReportStates.waiting_start_date)
async def process_start_date(message: types.Message, state: FSMContext):
    start_date = validate_date(message.text.strip())
    await state.update_data(start_date=start_date)  # None если неверный формат или пусто
    await message.answer(
        "Введите конечную дату в формате YYYY-MM-DD или оставьте пустым для всего периода:"
    )
    await state.set_state(ReportStates.waiting_end_date)


@report_command_router.message(ReportStates.waiting_end_date)
async def process_end_date(message: types.Message, state: FSMContext):
    from celery_app.tasks import make_report
    end_date = validate_date(message.text.strip())
    data = await state.get_data()
    start_date = data.get("start_date")

    await state.clear()  # очищаем FSM

    # Запускаем Celery задачу
    make_report.delay(date_from=start_date, date_to=end_date)

    # Сообщение пользователю
    report_text = f"Отчет формируется и будет отправлен администраторам.\nПериод:\nС: {start_date or 'весь период'}\nДо: {end_date or 'весь период'}"
    await message.answer(report_text)
