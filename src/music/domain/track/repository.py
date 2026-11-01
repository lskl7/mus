from typing import Protocol
from uuid import UUID

from domain.track.track import Track


# Интерфейс хранилища треков. Его реализуют репозитории JSON и XML.
class TrackRepository(Protocol):
    def add(self, track: Track) -> None:
        raise NotImplementedError

    def get_by_id(self, track_id: UUID) -> Track | None:
        raise NotImplementedError

    def get_all(self) -> list[Track]:
        raise NotImplementedError

    def update(self, track: Track) -> None:
        raise NotImplementedError

    def delete(self, track_id: UUID) -> None:
        raise NotImplementedError
