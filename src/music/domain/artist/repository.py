from typing import Protocol

from domain.artist.artist import Artist


# Интерфейс хранилища исполнителей. Его реализуют репозитории JSON и XML,
# поэтому сервисы не зависят от формата файла.
class ArtistRepository(Protocol):
    def add(self, artist: Artist) -> None:
        raise NotImplementedError

    def get_by_id(self, artist_id: int) -> Artist | None:
        raise NotImplementedError

    def get_all(self) -> list[Artist]:
        raise NotImplementedError

    def update(self, artist: Artist) -> None:
        raise NotImplementedError

    def delete(self, artist_id: int) -> None:
        raise NotImplementedError
