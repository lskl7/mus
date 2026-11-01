from domain.artist.artist_name import ArtistName
from domain.artist.genre import Genre


# Исполнитель или группа. Имя и жанр меняются методом change,
# id остается прежним.
class Artist:
    def __init__(
            self,
            artist_id: int,
            name: ArtistName,
            genre: Genre
    ) -> None:
        self.__id = artist_id
        self.__name = name
        self.__genre = genre

    def change(self, name: ArtistName, genre: Genre) -> None:
        self.__name = name
        self.__genre = genre

    @property
    def id(self) -> int:
        return self.__id

    @property
    def name(self) -> ArtistName:
        return self.__name

    @property
    def genre(self) -> Genre:
        return self.__genre
