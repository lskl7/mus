from application.artist_service import ArtistService
from application.track_service import TrackService
from domain.artist.repository import ArtistRepository
from domain.exceptions import MusicError
from domain.track.repository import TrackRepository
from infrastructure.db.json.artist_repository import JsonArtistRepository
from infrastructure.db.json.track_repository import JsonTrackRepository
from infrastructure.db.xml.artist_repository import XmlArtistRepository
from infrastructure.db.xml.track_repository import XmlTrackRepository
from presentation.console import Console, read_line

# Пункт выбора при запуске и соответствующий формат файлов.
STORAGE_FORMATS = {"1": "xml", "2": "json"}


def choose_storage_format() -> str:
    while True:
        choice = read_line(
            "Формат хранения данных (1 - XML, 2 - JSON): "
        ).strip()

        if choice in STORAGE_FORMATS:
            return STORAGE_FORMATS[choice]

        print("Введите 1 или 2")


def build_repositories(
        storage_format: str,
) -> tuple[ArtistRepository, TrackRepository]:
    if storage_format == "json":
        return (
            JsonArtistRepository("data/artists.json"),
            JsonTrackRepository("data/tracks.json"),
        )

    return (
        XmlArtistRepository("data/artists.xml"),
        XmlTrackRepository("data/tracks.xml"),
    )


# Собираем зависимости: репозитории передаются в сервисы,
# сервисы - в консоль.
def build_console(storage_format: str) -> Console:
    artist_repository, track_repository = build_repositories(storage_format)

    artist_service = ArtistService(
        artist_repository=artist_repository,
        track_repository=track_repository,
    )
    track_service = TrackService(
        track_repository=track_repository,
        artist_repository=artist_repository,
    )

    return Console(
        artist_service=artist_service,
        track_service=track_service,
    )


def main() -> None:
    try:
        storage_format = choose_storage_format()
    except (KeyboardInterrupt, EOFError):
        print()
        return

    try:
        console = build_console(storage_format)
    except MusicError as error:
        print(f"Не удалось подготовить хранилище: {error}")
        return

    console.run()


if __name__ == "__main__":
    main()
