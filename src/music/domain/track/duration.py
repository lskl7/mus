from domain.exceptions import ValidationError

# Трек короче полуминуты или длиннее двадцати минут не считается песней.
MIN_SECONDS = 30
MAX_SECONDS = 20 * 60


# Объект-значение: длительность трека в секундах.
class Duration:
    def __init__(self, seconds: int) -> None:
        if not MIN_SECONDS <= seconds <= MAX_SECONDS:
            raise ValidationError(
                f"Длительность от {MIN_SECONDS} до {MAX_SECONDS} секунд"
            )

        self.__seconds = seconds

    @property
    def seconds(self) -> int:
        return self.__seconds

    @property
    def text(self) -> str:
        minutes, rest = divmod(self.__seconds, 60)
        return f"{minutes}:{rest:02d}"
