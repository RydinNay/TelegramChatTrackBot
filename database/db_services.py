from database.database import async_session
from sqlalchemy import select, func, update

from .models import User


class UserService:
    @staticmethod
    async def create_user(tg_id: int, name: str = None, source: str = None) -> User:
        async with async_session() as session:
            async with session.begin():
                result = await session.execute(select(User).where(User.tg_id == tg_id))
                user = result.scalar_one_or_none()
                if user:
                    return user
                new_user = User(tg_id=tg_id, name=name, source=source)
                session.add(new_user)
                return new_user

    @staticmethod
    async def get_report_data(date_from=None, date_to=None):
        async with async_session() as session:

            base_query = select(User)
            if date_from:
                base_query = base_query.where(User.created_at >= date_from)
            if date_to:
                base_query = base_query.where(User.created_at <= date_to)

            result = await session.execute(base_query)
            users = result.scalars().all()

            stats = {}

            for user in users:
                src = user.source or "unknown"

                if src not in stats:
                    stats[src] = {
                        "total": 0,
                        "active": 0,
                        "unsubscribed": 0
                    }

                stats[src]["total"] += 1

                if user.is_still_active:
                    stats[src]["active"] += 1
                else:
                    stats[src]["unsubscribed"] += 1

            final_sources = []
            total_all = 0
            total_active = 0
            total_unsub = 0

            for src, vals in stats.items():
                total_all += vals["total"]
                total_active += vals["active"]
                total_unsub += vals["unsubscribed"]

                final_sources.append({
                    "source": src,
                    "total": vals["total"],
                    "active": vals["active"],
                    "unsubscribed": vals["unsubscribed"],
                })

            return {
                "sources": final_sources,
                "totals": {
                    "total": total_all,
                    "active": total_active,
                    "unsubscribed": total_unsub
                }
            }


    @staticmethod
    async def get_active_users() -> list[User]:
        async with async_session() as session:
            result = await session.execute(
                select(User).where(User.is_still_active == True)
            )
            return result.scalars().all()

    @staticmethod
    async def deactivate_users(user_ids: list[int]):
        if not user_ids:
            return

        async with async_session() as session:
            async with session.begin():
                await session.execute(
                    update(User)
                    .where(User.id.in_(user_ids))
                    .values(is_still_active=False)
                )