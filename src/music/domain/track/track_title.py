from domain.exceptions import ValidationError

MAX_TITLE_LENGTH = 100


# Объект-значение: название трека от 1 до 100 символов.
class TrackTitle:
    def __init__(self, value: str) -> None:
        normalized = " ".join(value.split())

        if not 1 <= len(normalized) <= MAX_TITLE_LENGTH:
            raise ValidationError(
                f"Название трека от 1 до {MAX_TITLE_LENGTH} символов"
            )

        self.__value = normalized

    @property
    def value(self) -> str:
        return self.__value
