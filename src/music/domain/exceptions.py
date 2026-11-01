# Базовое исключение приложения: консоль перехватывает его
# и показывает пользователю сообщение вместо трассировки.
class MusicError(Exception):
    pass


# Данные нарушают правила предметной области.
class ValidationError(MusicError):
    pass


# Записи с указанным id нет в хранилище.
class NotFoundError(MusicError):
    pass


# Такая запись уже есть в хранилище.
class AlreadyExistsError(MusicError):
    pass


# Файл хранилища не удалось прочитать, записать или разобрать.
class StorageError(MusicError):
    pass
