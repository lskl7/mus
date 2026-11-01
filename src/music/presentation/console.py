# readline включает стрелки и историю ввода в input().
import readline  # noqa: F401
from collections.abc import Callable

from application.artist_service import ArtistService
from application.track_service import TrackService
from domain.artist.artist import Artist
from domain.artist.artist_name import ArtistName
from domain.artist.genre import Genre
from domain.exceptions import MusicError, ValidationError
from domain.track.duration import Duration
from domain.track.track import Track
from domain.track.track_title import TrackTitle

MENU = """
Меню:
1 - показать исполнителей
2 - добавить исполнителя
3 - изменить исполнителя
4 - удалить исполнителя
5 - показать треки
6 - найти треки по названию
7 - добавить трек
8 - изменить название трека
9 - удалить трек
0 - выход
"""


# Терминал иногда передает обрывки байтов кириллицы.
# Возвращаем их в байты и отбрасываем то, что не декодируется.
def read_line(prompt: str) -> str:
    raw = input(prompt)
    return raw.encode("utf-8", "surrogateescape").decode("utf-8", "ignore")


# Ввод с проверкой: неверное значение превращается в ValidationError,
# который консоль покажет пользователю.
def ask_int(prompt: str) -> int:
    raw = read_line(prompt).strip()

    try:
        return int(raw)
    except ValueError as error:
        raise ValidationError("Введите целое число") from error


# Плоское меню без подменю. Консоль только спрашивает пользователя
# и печатает результат, а правила живут в сервисах и классах.
class Console:
    def __init__(
            self,
            artist_service: ArtistService,
            track_service: TrackService
    ) -> None:
        self.__artist_service = artist_service
        self.__track_service = track_service

    def run(self) -> None:
        actions: dict[str, Callable[[], None]] = {
            "1": self.__show_artists,
            "2": self.__add_artist,
            "3": self.__change_artist,
            "4": self.__delete_artist,
            "5": self.__show_tracks,
            "6": self.__find_tracks,
            "7": self.__add_track,
            "8": self.__change_title,
            "9": self.__delete_track,
        }

        try:
            while True:
                print(MENU)
                choice = read_line("Выберите пункт: ").strip()

                if choice == "0":
                    print("До свидания")
                    return

                action = actions.get(choice)

                if action is None:
                    print("Такого пункта нет")
                    continue

                self.__run_action(action)
        except (KeyboardInterrupt, EOFError):
            print()

    # Ошибки предметной области и ввода не завершают программу.
    @staticmethod
    def __run_action(action: Callable[[], None]) -> None:
        try:
            action()
        except MusicError as error:
            print(f"Ошибка: {error}")
        except (ValueError, TypeError) as error:
            print(f"Ошибка ввода: {error}")

    def __show_artists(self) -> None:
        artists = self.__artist_service.get_all_artists()

        if not artists:
            print("Исполнителей пока нет")

        for artist in artists:
            self.__print_artist(artist)

    def __add_artist(self) -> None:
        artist = Artist(
            artist_id=self.__artist_service.next_id(),
            name=ArtistName(read_line("Имя исполнителя: ")),
            genre=Genre(read_line("Жанр: ")),
        )

        self.__artist_service.add_artist(artist)
        print(f"Исполнитель добавлен, id: {artist.id}")

    def __change_artist(self) -> None:
        artist_id = ask_int("id исполнителя: ")
        name = ArtistName(read_line("Новое имя: "))
        genre = Genre(read_line("Новый жанр: "))

        self.__artist_service.change_artist(artist_id, name, genre)
        print("Исполнитель изменен")

    def __delete_artist(self) -> None:
        self.__artist_service.delete_artist(ask_int("id исполнителя: "))
        print("Исполнитель удален")

    def __show_tracks(self) -> None:
        self.__print_tracks(self.__track_service.get_all_tracks())

    def __find_tracks(self) -> None:
        text = read_line("Часть названия: ")
        self.__print_tracks(self.__track_service.find_tracks_by_title(text))

    def __add_track(self) -> None:
        track = Track(
            track_id=self.__track_service.next_id(),
            artist_id=ask_int("id исполнителя: "),
            title=TrackTitle(read_line("Название трека: ")),
            duration=Duration(ask_int("Длительность, секунд: ")),
        )

        self.__track_service.add_track(track)
        print(f"Трек добавлен, id: {track.id}")

    def __change_title(self) -> None:
        track_id = ask_int("id трека: ")
        title = TrackTitle(read_line("Новое название: "))

        self.__track_service.change_title(track_id, title)
        print("Название изменено")

    def __delete_track(self) -> None:
        self.__track_service.delete_track(ask_int("id трека: "))
        print("Трек удален")

    def __print_tracks(self, tracks: list[Track]) -> None:
        if not tracks:
            print("Треков нет")

        for track in tracks:
            print(
                f"{track.id} | {track.title.value} | "
                f"{track.duration.text} | исполнитель {track.artist_id}"
            )

    @staticmethod
    def __print_artist(artist: Artist) -> None:
        print(
            f"{artist.id} | {artist.name.value} | "
            f"жанр: {artist.genre.value}"
        )
