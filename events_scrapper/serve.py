import asyncio
from events_scrapper.scrapper.engines.conference_monkey_engine import (
    ConferenceMonkeyEngine,
)
from events_scrapper.scrapper.scheduler import Scheduler
from events_scrapper.utils.record_utils import select_last_scrapped_url
from events_scrapper.logs import create_logger

LOGGER = create_logger(__name__)


if __name__ == "__main__":
    # TODO: off course machine_id not always equals to 1 :)
    last_selected_url = select_last_scrapped_url(machine_id=1).iloc[0].to_dict()
    LOGGER.info(f"Starting scraping with init dot of {last_selected_url}")
    monkey = ConferenceMonkeyEngine(last_detected_url=last_selected_url["last_saved_url"])
    scheduler = Scheduler(engine=monkey)
    asyncio.run(scheduler.run())