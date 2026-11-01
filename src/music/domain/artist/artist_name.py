from domain.exceptions import ValidationError

MAX_NAME_LENGTH = 100


# Объект-значение: имя исполнителя или группы от 1 до 100 символов.
class ArtistName:
    def __init__(self, value: str) -> None:
        normalized = " ".join(value.split())

        if not 1 <= len(normalized) <= MAX_NAME_LENGTH:
            raise ValidationError(
                f"Имя исполнителя от 1 до {MAX_NAME_LENGTH} символов"
            )

        self.__value = normalized

    @property
    def value(self) -> str:
        return self.__value
