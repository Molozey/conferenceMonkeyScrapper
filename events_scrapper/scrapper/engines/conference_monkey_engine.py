import asyncio

from events_scrapper.scrapper.engines.abc_engine import EngineInterface, NEW_EVENTS
from events_scrapper.scrapper.models.event import Event
from aiohttp import ClientSession
from bs4 import BeautifulSoup
import pandas as pd
from itertools import chain



class ConferenceMonkeyEngine(EngineInterface):
    root_url = "https://conferencemonkey.org"
    info_source = "ConferenceMonkey"
    headers = {
        "accept": "image/avif,image/webp,image/apng,image/svg+xml,image/,/*;q=0.8",
        "user-agent": "Mozilla/5.0",
    }

    def __init__(self):
        self.last_detected_url: str = "https://conferencemonkey.org/conference/26th-infer-annual-conference-in-economics-1541499"

    async def _get_event_info(self, event_url: str, session: ClientSession) -> Event:
        async with session.get(url=event_url, headers=self.headers) as response:
            response_text = await response.text()

            soup = BeautifulSoup(response_text, "html.parser")

            # FIXME: delete first and last spaces
            event_name = " ".join(
                soup.find("div", class_="title").text.replace("\n", "").lstrip().split()
            )
            event_location = " ".join(
                soup.find("div", class_="location-details")
                .text.replace("\n", "")
                .lstrip()
                .split()
            )
            event_date = soup.find("meta", attrs={"itemprop": "startDate"})["content"]
            event_description = str(soup.find("div", class_="post-description").text)

            event = Event(
                event_info_source=self.info_source,
                event_name=event_name,
                event_location=event_location,
                event_date=pd.Timestamp(event_date),
                event_description=event_description,
                event_meta_info={},
            )
            return event

    def child_links_at_page(self, page: BeautifulSoup) -> list[(int, str)]:
        """
        Номера нужны для того чтобы можно было в дальнейшем при необходимости использовать асинхронные движки.
        Тут они не нужны, но будут нужны для восстановления порядка записей на уровне вызывающей функции
        :param page:
        :return:
        """
        all_links = page.find_all("a", class_="post-link")
        results = []
        for link_num, link_obj in enumerate(all_links):
            results.append((link_num, self.root_url + link_obj["href"]))
        return results

    async def find_new_events(self) -> NEW_EVENTS:
        url_i = "https://conferencemonkey.org/top/conferences?page={}"
        page_num = 0

        detected_new_urls: list[(int, list[(int, str)])] = []
        async with ClientSession() as session:
            while True:
                async with session.get(url=url_i.format(page_num)) as response:
                    response_text = await response.text()
                    soup = BeautifulSoup(response_text, "html.parser")
                links = self.child_links_at_page(page=soup)
                if self.last_detected_url in [link for _, link in links]:
                    _detected_position = [link for _, link in links].index(
                        self.last_detected_url
                    )
                    detected_new_urls.append(
                        [
                            page_num,
                            [
                                (num, link)
                                for num, link in links
                                if num < _detected_position
                            ],
                        ]
                    )
                    break
                detected_new_urls.append([page_num, links])
                page_num += 1
        return detected_new_urls

    def set_new_detected(self, process_batch: NEW_EVENTS):
        self.last_detected_url = process_batch[0][-1][0]

    async def process_new(self, process_batch: NEW_EVENTS) -> list[Event]:
        need_to_process = [link for _, links in process_batch for __, link in links]
        async with ClientSession() as session:
            # Тут нет никаких TypeError. Классическое поведение IDE с gather.
            results: list[Event] = await asyncio.gather(
                *[
                    self._get_event_info(event_url=event_url, session=session)
                    for event_url in need_to_process
                ],
                return_exceptions=True,
            )

        self.set_new_detected(process_batch)
        return results


async def main():
    monkey = ConferenceMonkeyEngine()
    NEW_BATCH = await monkey.find_new_events()
    new_events = await monkey.process_new(NEW_BATCH)
    print(len(new_events))


if __name__ == "__main__":
    asyncio.run(main())
