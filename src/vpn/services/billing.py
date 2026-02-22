from datetime import date
from decimal import Decimal
from typing import List

from src.vpn.db.models.transactions import TransactionType
from src.vpn.repositories.peers import PeersRepository
from src.vpn.repositories.transactions import TransactionsRepository
from src.vpn.repositories.users import UsersRepository
from src.vpn.schemas.transactions import TransactionCreate
from src.vpn.schemas.users import UserRead


class BillingService:

    DAILY_RATE = Decimal("4.00")

    def __init__(self, user_repo: UsersRepository, peer_repo: PeersRepository, trans_repo: TransactionsRepository):
        self.user_repo = user_repo
        self.peer_repo = peer_repo
        self.transaction_repo = trans_repo


    async def daily_billing(self) -> dict:
        charged_users = 0
        deactivated_users = 0
        total_charged = Decimal("0.00")
        errors = []

        print(f"Начала биллинга: {date.today()}")

        users_with_peers = await self._get_users_with_active_peers()

        print(f"Найдено пользователей: {len(users_with_peers)}")

        for user in users_with_peers:
            try:
                if user.balance >= self.DAILY_RATE:
                    await self.user_repo.deduct_balance(user.id, self.DAILY_RATE)


                    await self.transaction_repo.add(
                        TransactionCreate(          #type: ignore
                            user_id=user.id,
                            type=TransactionType.CHARGE,
                            amount=self.DAILY_RATE,
                            description=f"Ежедневная плата за VPN ({date.today()})"
                        )
                    )

                    charged_users += 1
                    total_charged += self.DAILY_RATE
                    print(f"Списано {self.DAILY_RATE} руб. с пользователя {user.id}")

                else:
                    deactivated = await self._deactivate_all_user_peers(user.id)
                    deactivated_users += 1
                    print(f"User - {user.id}: недостаточно средств, деактивированы {deactivated} peer'ов")

            except Exception as e:
                error_msg = f"User - {user.id}: {str(e)}"
                errors.append(error_msg)
                print(f"Ошибка - {error_msg}")
                continue

        result = {
            "date": str(date.today()),
            "charged_users": charged_users,
            "deactivated_users": deactivated_users,
            "total_charged": float(total_charged),
            "errors": errors
        }

        print(f"Биллинг завершён: {result}")
        return result


    async def _get_users_with_active_peers(self) -> List[UserRead]:
        users_with_active_peers = await self.peer_repo.get_all_active()

        user_ids = list(set(peer.user_id for peer in users_with_active_peers))

        users = []

        for user_id in user_ids:
            user = await self.user_repo.get_by_id(user_id)

            if user and user.is_active:
                users.append(user)

        return users


    async def _deactivate_all_user_peers(self, user_id: int) -> int:
        users_with_active_peers = await self.peer_repo.get_active_by_user_id(user_id)

        deactivated_count = 0

        for peer in users_with_active_peers:
            try:
                await self.peer_repo.deactivate_by_id(peer.id)
                deactivated_count += 1
            except Exception as e:
                print(f"Ошибка деактивации peer {peer.id}: {e}")
                continue

        return deactivated_count

