from datetime import date
import asyncio

from src.vpn.db.base import AsyncSessionLocal
from src.vpn.repositories.peers import PeersRepository
from src.vpn.repositories.transactions import TransactionsRepository
from src.vpn.repositories.users import UsersRepository
from src.vpn.services.billing import BillingService
from src.vpn.tasks.celery_app import celery_app


@celery_app.task(name="src.vpn.tasks.billing_tasks.daily_billing_tasks")
def daily_billing_task():
    print(f"Celery задача запущена: {date.today()}")

    result = asyncio.run(run_daily_billing())

    print(f"Celery задача завершена: {result}")
    return result


async def run_daily_billing():
    print(f"Запуск асинхронного биллинга")

    async with AsyncSessionLocal() as session:
        user_repo = UsersRepository(session)
        peer_repo = PeersRepository(session)
        trans_repo = TransactionsRepository(session)

        billing_service = BillingService(
            user_repo=user_repo,
            peer_repo=peer_repo,
            trans_repo=trans_repo
        )

        result = await billing_service.daily_billing()

        return result