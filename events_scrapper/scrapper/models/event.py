from dataclasses import dataclass
import pandas as pd
from hashlib import md5
import uuid


@dataclass
class Event:
    model_config = {"arbitrary_types_allowed": True}

    event_info_source: str
    event_name: str

    event_location: str  # Could have geo type, but for simplify reasons i decide to use string
    event_date: pd.Timestamp

    event_description: str
    event_meta_info: dict | None = None

    def __post_init__(self):
        if self.event_meta_info is None:
            self.event_meta_info = {}
    @property
    def event_uid(self):
        encoded = str(
            {
                "event_info_source": self.event_info_source,
                "event_name": self.event_name,
                "event_location": self.event_location,
                "event_date": self.event_date,
            }
        ).encode("utf-8")
        return uuid.UUID(bytes=md5(encoded).digest(), version=4)

    def __hash__(self):
        return hash(self.event_uid)


if __name__ == "__main__":
    date = pd.Timestamp("2022-01-02")
    event = Event(
        event_info_source="monkey_events",
        event_name="test_event",
        event_location="Puskina, Kolotyskina",
        event_date=date,
        event_description="test descr",
        event_meta_info={},
    )
    event2 = Event(
        event_info_source="monkey_events",
        event_name="test_event",
        event_location="Puskina, Kolotyskins",
        event_date=date,
        event_description="test descr",
        event_meta_info={},
    )
