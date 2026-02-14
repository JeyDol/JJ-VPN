


# ===== Базовое исключение =====
class VPNException(Exception):

    def __init__(self, message: str, detail: str | None = None):
        self.message = message
        self.detail = detail
        super().__init__(self.message)


# ===== Исключения репозитория =====
class RepositoryException(VPNException):
    pass

class NotFoundException(RepositoryException):
    """Объект не найден в бд"""

    def __init__(self, model_name: str, identifier: int | str):
        message = f"{model_name} не найден"
        detail = f"Идентификатор: {identifier}"
        super().__init__(message, detail)

class AlreadyExistsException(RepositoryException):
    """Такой объект уже существует"""

    def __init__(self, model_name: str, field: str, value: str | int):
        message = f"{model_name} c таким {field} уже существует"
        detail = f"{field: {value}}"
        super.__init__(message, detail)

# ===== Исключения бизнес логики =====
class ServiceException(VPNException):
    pass


class InsufficientBalanceException(ServiceException):
    """Недостаточно средств на балансе"""

    def __init__(self, user_id: int, required: float, available: float):
        message = "Недостаточно средств на балансе"
        detail = f"User ID: {user_id}, Требуется к пополнению: {required}, Доступно: {available}"
        super().__init__(message, detail)


class InvalidAmountException(ServiceException):
    """Неккоректная сумма операции"""

    def __init__(self, amount: float, reason: str = "Сумма должна быть положительной"):
        message = f"Неккоректная сумма: {amount}"
        detail = reason
        super().__init__(message, detail)


class PeerLimitExceededException(ServiceException):
    """Превышен лимит peer'ов для пользователя"""

    def __init__(self, user_id: int, limit: int = 5):
        message = f"Превышен лимит peer'ов"
        detail = f"User ID: {user_id}, Лимит: {limit}"
        super().__init__(message, detail)


class NoAvailableIPException(ServiceException):
    """Нет доступных IP-адресов в пуле"""

    def __init__(self):
        message = "Нет доступных IP адресов"
        detail = "Все IP адреса в пуле заняты"
        super().__init__(message, detail)

class PeerAlreadyActiveException(ServiceException):
    """Peer уже активен"""

    def __init__(self, peer_id: int):
        message = f"Peer: {peer_id} уже активен"
        super().__init__(message)


class PeerNotActiveException(ServiceException):
    """Peer не активен"""

    def __init__(self, peer_id: int):
        message = f"Peer: {peer_id} не активен"
        super().__init__(message)


# ===== Исключения WireGuard =====
class WireGuardException(ServiceException):
    pass

#дописать как перейду к wireguard


# ===== Исключения платежей =====
# дописать как перейду


# ===== Исключения Telegram Bot =====
#дописать как перейду

class ValidationException(VPNException):
    """Ошибка валидации данных"""
    def __init__(self, field: str, reason: str):
        message = f"Ошибка валидации поля - {field}"
        super().__init__(message)