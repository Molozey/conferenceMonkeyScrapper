import pandas as pd
from fastapi import APIRouter
from pydantic import BaseModel

from api_service.database import ENGINE
from api_service.logs import create_logger
from api_service.SelectQueries.events_queries import construct_categorical_query
from api_service.SelectQueries.events_queries import get_available_event_info_source
from api_service.SelectQueries.general_filter_generator import (
    Filter,
    general_filter_scrapped_events_generator,
)
from api_service.models.Events import EventsNum
LOGGER = create_logger(__name__)
router = APIRouter(prefix="/events", tags=["events"])


@router.get("/total_number_of_events")
async def total_events_number() -> EventsNum:
    q = f"""
    SELECT COUNT(*) FROM scrapper.scrapped_events
    """
    num = pd.read_sql(q, ENGINE()).iloc[0, 0]
    return EventsNum(collected_events_number=num)


@router.get("/number_of_events_by_source")
async def filtered_by_source(
    source: str = construct_categorical_query(get_available_event_info_source()),
):
    sql = general_filter_scrapped_events_generator(
        [
            Filter(
                filter_column="event_info_source",
                filter_value=source,
                filter_operation="=",
            )
        ],
        return_count=True
    )
    num = pd.read_sql(sql, ENGINE()).iloc[0, 0]
    return EventsNum(collected_events_number=num)

