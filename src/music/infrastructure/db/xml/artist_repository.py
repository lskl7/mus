import xml.etree.ElementTree as ET
from pathlib import Path

from domain.artist.artist import Artist
from domain.artist.artist_name import ArtistName
from domain.artist.genre import Genre
from domain.exceptions import (
    AlreadyExistsError,
    NotFoundError,
    StorageError,
    ValidationError,
)
from infrastructure.db.xml.storage import (
    read_records,
    read_text,
    write_records,
)

ROOT = "artists"


# Хранит исполнителей в XML-файле: корень <artists>, внутри элементы
# <artist>.
class XmlArtistRepository:
    def __init__(self, file_path: str | Path) -> None:
        self.__file_path = Path(file_path)

    def add(self, artist: Artist) -> None:
        records = read_records(self.__file_path, ROOT)

        if self.__find_index(records, artist.id) is not None:
            raise AlreadyExistsError(
                f"Исполнитель {artist.id} уже существует"
            )

        records.append(self.__to_element(artist))
        write_records(self.__file_path, ROOT, records)

    def get_by_id(self, artist_id: int) -> Artist | None:
        records = read_records(self.__file_path, ROOT)
        index = self.__find_index(records, artist_id)

        if index is None:
            return None

        return self.__to_artist(records[index])

    def get_all(self) -> list[Artist]:
        return [
            self.__to_artist(element)
            for element in read_records(self.__file_path, ROOT)
        ]

    def update(self, artist: Artist) -> None:
        records = read_records(self.__file_path, ROOT)
        index = self.__find_index(records, artist.id)

        if index is None:
            raise NotFoundError(f"Исполнитель {artist.id} не найден")

        records[index] = self.__to_element(artist)
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
            records: list[ET.Element], artist_id: int
    ) -> int | None:
        for index, element in enumerate(records):
            if element.findtext("id") == str(artist_id):
                return index

        return None

    @staticmethod
    def __to_element(artist: Artist) -> ET.Element:
        element = ET.Element("artist")

        ET.SubElement(element, "id").text = str(artist.id)
        ET.SubElement(element, "name").text = artist.name.value
        ET.SubElement(element, "genre").text = artist.genre.value

        return element

    def __to_artist(self, element: ET.Element) -> Artist:
        try:
            return Artist(
                artist_id=int(read_text(element, "id")),
                name=ArtistName(read_text(element, "name")),
                genre=Genre(read_text(element, "genre")),
            )
        except (ValueError, ValidationError) as error:
            raise StorageError(
                f"В файле {self.__file_path} повреждена запись исполнителя"
            ) from error
