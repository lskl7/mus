import xml.etree.ElementTree as ET
from pathlib import Path
from uuid import UUID

from domain.exceptions import (
    AlreadyExistsError,
    NotFoundError,
    StorageError,
    ValidationError,
)
from domain.track.duration import Duration
from domain.track.track import Track
from domain.track.track_title import TrackTitle
from infrastructure.db.xml.storage import (
    read_records,
    read_text,
    write_records,
)

ROOT = "tracks"


# Хранит треки в XML-файле: корень <tracks>, внутри элементы <track>.
class XmlTrackRepository:
    def __init__(self, file_path: str | Path) -> None:
        self.__file_path = Path(file_path)

    def add(self, track: Track) -> None:
        records = read_records(self.__file_path, ROOT)

        if self.__find_index(records, track.id) is not None:
            raise AlreadyExistsError(f"Трек {track.id} уже существует")

        records.append(self.__to_element(track))
        write_records(self.__file_path, ROOT, records)

    def get_by_id(self, track_id: UUID) -> Track | None:
        records = read_records(self.__file_path, ROOT)
        index = self.__find_index(records, track_id)

        if index is None:
            return None

        return self.__to_track(records[index])

    def get_all(self) -> list[Track]:
        return [
            self.__to_track(element)
            for element in read_records(self.__file_path, ROOT)
        ]

    def update(self, track: Track) -> None:
        records = read_records(self.__file_path, ROOT)
        index = self.__find_index(records, track.id)

        if index is None:
            raise NotFoundError(f"Трек {track.id} не найден")

        records[index] = self.__to_element(track)
        write_records(self.__file_path, ROOT, records)

    def delete(self, track_id: UUID) -> None:
        records = read_records(self.__file_path, ROOT)
        index = self.__find_index(records, track_id)

        if index is None:
            raise NotFoundError(f"Трек {track_id} не найден")

        del records[index]
        write_records(self.__file_path, ROOT, records)

    @staticmethod
    def __find_index(
            records: list[ET.Element], track_id: UUID
    ) -> int | None:
        for index, element in enumerate(records):
            if element.findtext("id") == str(track_id):
                return index

        return None

    @staticmethod
    def __to_element(track: Track) -> ET.Element:
        element = ET.Element("track")

        ET.SubElement(element, "id").text = str(track.id)
        ET.SubElement(element, "artist_id").text = str(track.artist_id)
        ET.SubElement(element, "title").text = track.title.value
        ET.SubElement(element, "duration").text = str(track.duration.seconds)

        return element

    def __to_track(self, element: ET.Element) -> Track:
        try:
            return Track(
                track_id=UUID(read_text(element, "id")),
                artist_id=UUID(read_text(element, "artist_id")),
                title=TrackTitle(read_text(element, "title")),
                duration=Duration(int(read_text(element, "duration"))),
            )
        except (ValueError, ValidationError) as error:
            raise StorageError(
                f"В файле {self.__file_path} повреждена запись трека"
            ) from error
