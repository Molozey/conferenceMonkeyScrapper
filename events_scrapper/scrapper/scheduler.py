import asyncio
from queue import Queue
from events_scrapper.scrapper.engines.abc_engine import EngineInterface
import logging


LOGGER = logging.getLogger(__name__)


class Scheduler:
    """
    Class that looks to website to get signals that new events are provided.
    Cold start possible doesn't work
    """

    # Naive approach. Works in assumption that events cannot be deleted
    newest_scrapped_event_url = "https://conferencemonkey.org/advice/top-gifts-for-electrical-engineers-1427485"
    def __init__(self, engine: EngineInterface):

        self.scrap_engine = engine


    async def run(self):
        while True:
            new_events = await self.scrap_engine.find_new_events()
            if new_events and new_events != [[0, []]]:
                LOGGER.info("New events found")
                result = await self.scrap_engine.process_new(new_events)
                if result:
                    LOGGER.info(f"Successfully set new {len(result)} events. Wait 60 sec")
                await asyncio.sleep(5)
                continue

            LOGGER.info(f"No new updates: {new_events}")
            await asyncio.sleep(10)


