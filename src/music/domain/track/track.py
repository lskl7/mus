from domain.track.duration import Duration
from domain.track.track_title import TrackTitle


# Трек принадлежит исполнителю, поэтому хранит его id.
# Название меняется методом change_title, id остается прежним.
class Track:
    def __init__(
            self,
            track_id: int,
            artist_id: int,
            title: TrackTitle,
            duration: Duration
    ) -> None:
        self.__id = track_id
        self.__artist_id = artist_id
        self.__title = title
        self.__duration = duration

    def change_title(self, title: TrackTitle) -> None:
        self.__title = title

    @property
    def id(self) -> int:
        return self.__id

    @property
    def artist_id(self) -> int:
        return self.__artist_id

    @property
    def title(self) -> TrackTitle:
        return self.__title

    @property
    def duration(self) -> Duration:
        return self.__duration
