from pathlib import Path
from typing import Any

from domain.artist.artist import Artist
from domain.artist.artist_name import ArtistName
from domain.artist.genre import Genre
from domain.exceptions import (
    AlreadyExistsError,
    NotFoundError,
    StorageError,
    ValidationError,
)
from infrastructure.db.json.storage import read_records, write_records

ROOT = "artists"


# Хранит исполнителей в JSON-файле вида {"artists": [...]}.
# Каждая операция заново читает файл и сразу записывает изменения.
class JsonArtistRepository:
    def __init__(self, file_path: str | Path) -> None:
        self.__file_path = Path(file_path)

    def add(self, artist: Artist) -> None:
        records = read_records(self.__file_path, ROOT)

        if self.__find_index(records, artist.id) is not None:
            raise AlreadyExistsError(
                f"Исполнитель {artist.id} уже существует"
            )

        records.append(self.__to_dict(artist))
        write_records(self.__file_path, ROOT, records)

    def get_by_id(self, artist_id: int) -> Artist | None:
        records = read_records(self.__file_path, ROOT)
        index = self.__find_index(records, artist_id)

        if index is None:
            return None

        return self.__to_artist(records[index])

    def get_all(self) -> list[Artist]:
        return [
            self.__to_artist(record)
            for record in read_records(self.__file_path, ROOT)
        ]

    def update(self, artist: Artist) -> None:
        records = read_records(self.__file_path, ROOT)
        index = self.__find_index(records, artist.id)

        if index is None:
            raise NotFoundError(f"Исполнитель {artist.id} не найден")

        records[index] = self.__to_dict(artist)
        write_records(self.__file_path, ROOT, records)

    def delete(self, artist_id: int) -> None:
        records = read_records(self.__file_path, ROOT)
        index = self.__find_index(records, artist_id)

        if index is None:
            raise NotFoundError(f"Исполнитель {artist_id} не найден")

        del records[index]
        write_records(self.__file_path, ROOT, records)

    @staticmethod
    def __find_index(
            records: list[dict[str, Any]], artist_id: int
    ) -> int | None:
        for index, record in enumerate(records):
            if record.get("id") == (artist_id):
                return index

        return None

    @staticmethod
    def __to_dict(artist: Artist) -> dict[str, Any]:
        return {
            "id": artist.id,
            "name": artist.name.value,
            "genre": artist.genre.value,
        }

    # Любая ошибка разбора превращается в StorageError
    # с понятным сообщением вместо KeyError или ValueError.
    def __to_artist(self, record: dict[str, Any]) -> Artist:
        try:
            return Artist(
                artist_id=int(record["id"]),
                name=ArtistName(record["name"]),
                genre=Genre(record["genre"]),
            )
        except (KeyError, TypeError, ValueError, ValidationError) as error:
            raise StorageError(
                f"В файле {self.__file_path} повреждена запись исполнителя"
            ) from error
