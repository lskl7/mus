from pathlib import Path
from typing import Any

from domain.exceptions import (
    AlreadyExistsError,
    NotFoundError,
    StorageError,
    ValidationError,
)
from domain.track.duration import Duration
from domain.track.track import Track
from domain.track.track_title import TrackTitle
from infrastructure.db.json.storage import read_records, write_records

ROOT = "tracks"


# Хранит треки в JSON-файле вида {"tracks": [...]}.
# Каждая операция заново читает файл и сразу записывает изменения.
class JsonTrackRepository:
    def __init__(self, file_path: str | Path) -> None:
        self.__file_path = Path(file_path)

    def add(self, track: Track) -> None:
        records = read_records(self.__file_path, ROOT)

        if self.__find_index(records, track.id) is not None:
            raise AlreadyExistsError(f"Трек {track.id} уже существует")

        records.append(self.__to_dict(track))
        write_records(self.__file_path, ROOT, records)

    def get_by_id(self, track_id: int) -> Track | None:
        records = read_records(self.__file_path, ROOT)
        index = self.__find_index(records, track_id)

        if index is None:
            return None

        return self.__to_track(records[index])

    def get_all(self) -> list[Track]:
        return [
            self.__to_track(record)
            for record in read_records(self.__file_path, ROOT)
        ]

    def update(self, track: Track) -> None:
        records = read_records(self.__file_path, ROOT)
        index = self.__find_index(records, track.id)

        if index is None:
            raise NotFoundError(f"Трек {track.id} не найден")

        records[index] = self.__to_dict(track)
        write_records(self.__file_path, ROOT, records)

    def delete(self, track_id: int) -> None:
        records = read_records(self.__file_path, ROOT)
        index = self.__find_index(records, track_id)

        if index is None:
            raise NotFoundError(f"Трек {track_id} не найден")

        del records[index]
        write_records(self.__file_path, ROOT, records)

    @staticmethod
    def __find_index(
            records: list[dict[str, Any]], track_id: int
    ) -> int | None:
        for index, record in enumerate(records):
            if record.get("id") == (track_id):
                return index

        return None

    @staticmethod
    def __to_dict(track: Track) -> dict[str, Any]:
        return {
            "id": track.id,
            "artist_id": track.artist_id,
            "title": track.title.value,
            "duration": track.duration.seconds,
        }

    # Любая ошибка разбора превращается в StorageError.
    def __to_track(self, record: dict[str, Any]) -> Track:
        try:
            return Track(
                track_id=int(record["id"]),
                artist_id=int(record["artist_id"]),
                title=TrackTitle(record["title"]),
                duration=Duration(record["duration"]),
            )
        except (KeyError, TypeError, ValueError, ValidationError) as error:
            raise StorageError(
                f"В файле {self.__file_path} повреждена запись трека"
            ) from error
