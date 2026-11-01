from domain.artist.artist import Artist
from domain.artist.artist_name import ArtistName
from domain.artist.genre import Genre
from domain.artist.repository import ArtistRepository
from domain.exceptions import NotFoundError, ValidationError
from domain.track.repository import TrackRepository


# Сценарии работы с исполнителями.
class ArtistService:
    def __init__(
            self,
            artist_repository: ArtistRepository,
            track_repository: TrackRepository
    ) -> None:
        self.__artist_repository = artist_repository
        self.__track_repository = track_repository

    # Новый id на единицу больше самого большого из сохраненных.
    def next_id(self) -> int:
        ids = [artist.id for artist in self.get_all_artists()]
        return max(ids, default=0) + 1

    def add_artist(self, artist: Artist) -> None:
        self.__artist_repository.add(artist)

    def get_artist(self, artist_id: int) -> Artist:
        artist = self.__artist_repository.get_by_id(artist_id)

        if artist is None:
            raise NotFoundError(f"Исполнитель {artist_id} не найден")

        return artist

    def get_all_artists(self) -> list[Artist]:
        return self.__artist_repository.get_all()

    def change_artist(
            self, artist_id: int, name: ArtistName, genre: Genre
    ) -> None:
        artist = self.get_artist(artist_id)
        artist.change(name, genre)
        self.__artist_repository.update(artist)

    # Исполнителя с треками удалять нельзя: у треков останется
    # ссылка на несуществующего исполнителя.
    def delete_artist(self, artist_id: int) -> None:
        self.get_artist(artist_id)

        tracks = self.__track_repository.get_all()

        if any(track.artist_id == artist_id for track in tracks):
            raise ValidationError(
                "Нельзя удалить исполнителя: у него есть треки"
            )

        self.__artist_repository.delete(artist_id)
