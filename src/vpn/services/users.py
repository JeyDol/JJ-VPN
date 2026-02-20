from decimal import Decimal

from src.vpn.core.exceptions import AlreadyExistsException, InvalidAmountException, NotFoundException
from src.vpn.db.models.transactions import TransactionType
from src.vpn.repositories.peers import PeersRepository
from src.vpn.repositories.transactions import TransactionsRepository
from src.vpn.repositories.users import UsersRepository
from src.vpn.schemas.transactions import TransactionCreate
from src.vpn.schemas.users import UserRead, UserCreate


class UsersService:
    def __init__(self, user_repo: UsersRepository, peer_repo: PeersRepository, trans_repo: TransactionsRepository):
        self.user_repo = user_repo
        self.peer_repo = peer_repo
        self.trans_repo = trans_repo


    async def register_user(self, tg_id: int, email: str = None) -> UserRead:
        """Регистрация на кнопку зарегаться"""

        existing_user = await self.user_repo.get_by_telegram_id(tg_id)

        if existing_user is not None:
            raise AlreadyExistsException("User", "telegram_id", value=tg_id)

        new_user = await self.user_repo.add(
              UserCreate(                   #type: ignore
                telegram_id=tg_id,
                email=email
            )
        )

        return new_user                     #type: ignore


    async def get_or_create_user(self, tg_id: int) -> UserRead:
        """Регистрация просто при открытия веб-аппа"""

        user = await self.user_repo.get_by_telegram_id(tg_id)

        if user is None:
            user = await self.user_repo.add(
                UserCreate(                 #type: ignore
                    telegram_id=tg_id
                )
            )

        return user


    async def add_balance_with_transaction(self, user_id: int, amount: Decimal, payment_provider: str = None, external_id: str = None) -> UserRead:
        if amount <=  0:
            raise InvalidAmountException(float(amount), "Сумма должна быть положительной")
        user = await self.user_repo.add_balance(user_id=user_id, amount=amount)
        await self.trans_repo.add(
            TransactionCreate(      #type: ignore
                user_id=user_id,
                type=TransactionType.DEPOSIT,
                amount=amount,
                description="Пополнение баланса",
                payment_provider=payment_provider,
                external_id=external_id
            )
        )

        return user


    async def can_create_peer(self, user_id: int, daily_cost: Decimal = Decimal("10.00"), max_peers: int = 5) -> dict:
        user = await self.user_repo.get_by_id(user_id)
        if user is None:
            raise NotFoundException("User", user_id)

        if not user.is_active:
            return {
                "can_create": False,
                "reason": "Аккаунт деактивирован",
                "balance": user.balance,
                "active_peers_count": 0
            }

        if user.balance < daily_cost:
            return {
                "can_create": False,
                "reason": f"Недостаточно средств. Требуется: {daily_cost} руб",
                "balance": user.balance,
                "active_peers_count": 0
            }

        active_peers_count = await self.peer_repo.count_active_by_user_id(user_id)

        if active_peers_count >= max_peers:
            return {
                "can_create": False,
                "reason": f"Превышен лимит устройств ({max_peers})",
                "balance": user.balance,
                "active_peers_count": active_peers_count
            }

        return {
            "can_create": True,
            "reason": None,
            "balance": user.balance,
            "active_peers_count": active_peers_count
        }