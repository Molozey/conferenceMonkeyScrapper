import typing

import pandas as pd
from fastapi import APIRouter
from pydantic import BaseModel
import json
from api_service.database import ENGINE
from api_service.logs import create_logger
from api_service.SelectQueries.events_queries import construct_categorical_query
from api_service.SelectQueries.events_queries import get_available_event_info_source
from api_service.SelectQueries.general_filter_generator import (
    Filter,
    general_filter_scrapped_events_generator,
)
from api_service.models.Events import EventsNum, Event

LOGGER = create_logger(__name__)
router = APIRouter(prefix="/universal_filter", tags=["filter"])


def _create_filter_list(
    source: str = construct_categorical_query(get_available_event_info_source()),
    source_sign: typing.Literal["=", "!="] = "=",
    event_date: str = None,
    event_date_sign: typing.Literal["<", ">", "=", "!="] = "=",
    updated_at: str = None,
    updated_at_sign: typing.Literal["<", ">", "=", "!="] = "=",
) -> list[Filter]:
    filters_list = []
    if source:
        filters_list.append(
            Filter(
                filter_column="event_info_source",
                filter_value=source,
                filter_operation=source_sign,
            )
        )
    if event_date:
        event_date = pd.Timestamp(event_date)
        filters_list.append(
            Filter(
                filter_column="event_date",
                filter_value=event_date,
                filter_operation=event_date_sign,
            )
        )
    if updated_at:
        updated_at = pd.Timestamp(updated_at)
        filters_list.append(
            Filter(
                filter_column="updated_at",
                filter_value=updated_at,
                filter_operation=updated_at_sign,
            )
        )
    return filters_list


@router.get("/total_number_of_filtered_events")
async def total_filtered_events(
    source: str = construct_categorical_query(get_available_event_info_source()),
    source_sign: typing.Literal["=", "!="] = "=",
    event_date: str = None,
    event_date_sign: typing.Literal["<", ">", "=", "!="] = "=",
    updated_at: str = None,
    updated_at_sign: typing.Literal["<", ">", "=", "!="] = "=",
) -> EventsNum:
    filters_list = _create_filter_list(
        source=source,
        source_sign=source_sign,
        event_date=event_date,
        event_date_sign=event_date_sign,
        updated_at=updated_at,
        updated_at_sign=updated_at_sign,
    )
    sql = general_filter_scrapped_events_generator(
        filters_list,
        return_count=True,
    )
    num = pd.read_sql(sql, ENGINE()).iloc[0, 0]
    return EventsNum(collected_events_number=num)


@router.get("/filtered_events")
async def filtered_events(
    source: str = construct_categorical_query(get_available_event_info_source()),
    source_sign: typing.Literal["=", "!="] = "=",
    event_date: str = None,
    event_date_sign: typing.Literal["<", ">", "=", "!="] = "=",
    updated_at: str = None,
    updated_at_sign: typing.Literal["<", ">", "=", "!="] = "=",
) -> list[Event]:
    filters_list = _create_filter_list(
        source=source,
        source_sign=source_sign,
        event_date=event_date,
        event_date_sign=event_date_sign,
        updated_at=updated_at,
        updated_at_sign=updated_at_sign,
    )
    sql = general_filter_scrapped_events_generator(
        filters_list,
        return_count=False,
    )
    results = pd.read_sql(sql, ENGINE())
    return [
        Event(
            event_uuid=item.get("event_uuid", "unknown"),
            event_info_source=item.get("event_info_source", "unknown"),
            event_name=item.get("event_name", "unknown"),
            event_location=item.get("event_location", "unknown"),
            event_date=pd.Timestamp(item.get("event_date", "1970-01-01")).isoformat(),
            event_description=item.get("event_description", "unknown"),
            event_meta_info=item.get("event_meta_info", {}),
            event_url=item.get("event_url", "unknown"),
            updated_at=pd.Timestamp(item.get("event_date", "1970-01-01")).isoformat(),
        )
        for item in results.to_dict("records")
    ]

@router.get("/filtered_events/page/")
async def filtered_events(
    page_number: int,
    page_size: int,
    source: str = construct_categorical_query(get_available_event_info_source()),
    source_sign: typing.Literal["=", "!="] = "=",
    event_date: str = None,
    event_date_sign: typing.Literal["<", ">", "=", "!="] = "=",
    updated_at: str = None,
    updated_at_sign: typing.Literal["<", ">", "=", "!="] = "=",
) -> list[Event]:
    filters_list = _create_filter_list(
        source=source,
        source_sign=source_sign,
        event_date=event_date,
        event_date_sign=event_date_sign,
        updated_at=updated_at,
        updated_at_sign=updated_at_sign,
    )
    sql = general_filter_scrapped_events_generator(
        filters_list,
        return_count=False,
        page_size=page_size,
        page_number=page_number
    )
    results = pd.read_sql(sql, ENGINE())
    return [
        Event(
            event_uuid=item.get("event_uuid", "unknown"),
            event_info_source=item.get("event_info_source", "unknown"),
            event_name=item.get("event_name", "unknown"),
            event_location=item.get("event_location", "unknown"),
            event_date=pd.Timestamp(item.get("event_date", "1970-01-01")).isoformat(),
            event_description=item.get("event_description", "unknown"),
            event_meta_info=item.get("event_meta_info", {}),
            event_url=item.get("event_url", "unknown"),
            updated_at=pd.Timestamp(item.get("event_date", "1970-01-01")).isoformat(),
        )
        for item in results.to_dict("records")
    ]