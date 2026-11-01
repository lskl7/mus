from uuid import UUID

from domain.artist.repository import ArtistRepository
from domain.exceptions import NotFoundError, ValidationError
from domain.track.repository import TrackRepository
from domain.track.track import Track
from domain.track.track_title import TrackTitle


# Сценарии работы с треками.
class TrackService:
    def __init__(
            self,
            track_repository: TrackRepository,
            artist_repository: ArtistRepository
    ) -> None:
        self.__track_repository = track_repository
        self.__artist_repository = artist_repository

    def add_track(self, track: Track) -> None:
        if self.__artist_repository.get_by_id(track.artist_id) is None:
            raise NotFoundError(f"Исполнитель {track.artist_id} не найден")

        self.__check_title_free(track.artist_id, track.title)
        self.__track_repository.add(track)

    def get_track(self, track_id: UUID) -> Track:
        track = self.__track_repository.get_by_id(track_id)

        if track is None:
            raise NotFoundError(f"Трек {track_id} не найден")

        return track

    def get_all_tracks(self) -> list[Track]:
        return self.__track_repository.get_all()

    def find_tracks_by_title(self, text: str) -> list[Track]:
        needle = text.strip().casefold()

        return [
            track
            for track in self.get_all_tracks()
            if needle in track.title.value.casefold()
        ]

    def change_title(self, track_id: UUID, title: TrackTitle) -> None:
        track = self.get_track(track_id)
        self.__check_title_free(track.artist_id, title)

        track.change_title(title)
        self.__track_repository.update(track)

    def delete_track(self, track_id: UUID) -> None:
        self.get_track(track_id)
        self.__track_repository.delete(track_id)

    # У одного исполнителя не может быть двух треков с одинаковым названием.
    def __check_title_free(self, artist_id: UUID, title: TrackTitle) -> None:
        if any(
            track.artist_id == artist_id
            and track.title.value.casefold() == title.value.casefold()
            for track in self.get_all_tracks()
        ):
            raise ValidationError(
                f"У исполнителя уже есть трек «{title.value}»"
            )
