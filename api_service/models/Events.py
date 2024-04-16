import pandas as pd
from pydantic import BaseModel
from dataclasses import dataclass

class EventsNum(BaseModel):
    collected_events_number: int

@dataclass
class Event():
    event_uuid: str
    event_info_source: str
    event_name: str
    event_location: str
    event_date: str
    event_description: str
    event_meta_info: dict
    event_url: str
    updated_at: str