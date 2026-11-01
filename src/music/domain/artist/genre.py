from domain.exceptions import ValidationError

# Жанры, которые можно выбрать. Список короткий, чтобы его было легко
# проверить и объяснить на защите.
GENRES = ("рок", "поп", "джаз", "классика", "хип-хоп", "электроника")


# Объект-значение: жанр из заранее заданного списка.
class Genre:
    def __init__(self, value: str) -> None:
        normalized = value.strip().lower()

        if normalized not in GENRES:
            raise ValidationError(
                "Жанр должен быть одним из: " + ", ".join(GENRES)
            )

        self.__value = normalized

    @property
    def value(self) -> str:
        return self.__value
