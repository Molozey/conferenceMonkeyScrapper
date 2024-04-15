from abc import ABC, abstractmethod
from events_scrapper.scrapper.models.event import Event
from aiohttp import ClientSession


NEW_EVENTS = list[(int, list[(int, str)])]


class EngineInterface(ABC):
    info_source: str

    @abstractmethod
    async def _get_event_info(self, event_url: str, session: ClientSession) -> Event:
        pass

    @abstractmethod
    async def find_new_events(self) -> NEW_EVENTS:
        pass

    @abstractmethod
    async def process_new(self, process_batch: NEW_EVENTS) -> list[Event]:
        pass

    @property
    def info_source(self):
        return self.info_source

    def make_event_record(self):
        pass
