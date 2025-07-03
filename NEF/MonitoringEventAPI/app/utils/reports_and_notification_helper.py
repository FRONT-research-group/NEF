import asyncio, httpx
from datetime import datetime
from fastapi import status,HTTPException

from app.utils.logger import get_app_logger
from app.utils.db_data_handler import DbDataHandler
from app.schemas.monitoring_event import MonitoringEventReport, MonitoringType,MonitoringNotification,LocationInfo,MonitoringEventSubscriptionRequest,GeographicArea

log = get_app_logger()

async def fetch_event_report(location_db_handler: DbDataHandler, imsi:str, current_rep: int, rep_period: int ) -> MonitoringEventReport:
    log.info(f"Processing report for IMSI: {imsi}, Report Number: {current_rep}")
    if rep_period is not None:
        await asyncio.sleep(rep_period)

    fetched_document = await location_db_handler.find_location_by_imsi(imsi)
    tuple_result_info = parse_document_to_ue_location(fetched_document)
    event_time = tuple_result_info[0]
    location_info = tuple_result_info[1]

    return MonitoringEventReport(msisdn=imsi,locationInfo=location_info,monitoringType=MonitoringType.LOCATION_REPORTING,eventTime=event_time)

async def mapper_msisdn_to_imsi(db_data_handler: DbDataHandler, msisdn: str) -> str:
    log.info(f"MSISDN {msisdn}")
    fetched_document = await db_data_handler.fetch_mapping_from_msisdn_to_imsi(msisdn)
    fetched_imsi = fetched_document.get("_id")
    log.info(f"Fetched IMSI {fetched_imsi}")
    return fetched_imsi

async def mapper_cell_id_to_polygon_shape_area(db_data_handler: DbDataHandler, cell_id : str) -> GeographicArea:
    fetched_area = await db_data_handler.fetch_mapping_from_cell_id_to_polygon(cell_id)
    log.info(f"Fetched geographic area {fetched_area}")
    return GeographicArea(**fetched_area)

def parse_document_to_ue_location(document: dict | None = None) -> tuple[datetime,LocationInfo]:
    if document is None:
          log.error("No event reports received from NEF.")
          raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No subscriptions found for this AF"
        )
    else:
        log.info(f"Fetched Docuement: {document}")
        event_time = document["UELocationTimestamp"]
        # age_of_location_info = document[]
        cell_id = document["cellId"]
        tac_id = document["trackingAreaId"]
        plmn_id = document["plmnId"]
        routing_aread_id = document["routingAreaId"]
        enodeb_id = document["enodeBId"]
        twan_id = document["twanId"]
        # geographic_area = document["geo"]

        return (event_time,LocationInfo(cellId=cell_id,trackingAreaId=tac_id,enodeBId=enodeb_id,routingAreaId=routing_aread_id,twanId=twan_id,plmnId=plmn_id))

def transform_cached_document_to_event_report(document: dict | None = None) -> MonitoringEventReport:
    if document is None:
        log.error("No document provided for event report transformation.")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No event report document found"
        )
    try:
        msisdn = document["msisdn"]
        location_info = document["locationInfo"]
        monitoring_type = document["monitoringType"]
        event_time = document["eventTime"]
        return MonitoringEventReport(
            msisdn=msisdn,
            locationInfo=location_info,
            monitoringType=monitoring_type,
            eventTime=event_time
        )
    except KeyError as exc:
        log.error(f"Missing key in document: {exc}", exc_info=exc)
        raise

def parse_and_transform_document_from_db(documents: list[dict]) -> list[tuple[str, MonitoringEventSubscriptionRequest]]:
    subscriptions: list[tuple[str, MonitoringEventSubscriptionRequest]] = []
    for doc in documents:
        try:
            subscription_id = doc["_id"]
            monitoring_event_subscription = doc["monitoringEventSubscription"]
            fetched_subscription = MonitoringEventSubscriptionRequest(**monitoring_event_subscription)
            subscriptions.append((subscription_id, fetched_subscription))
        except Exception as exc:
            log.error("Error transforming document", exc_info=exc)
    log.info(f"Converted documents to subscriptions: {subscriptions}")
    return subscriptions

def create_monitoring_notification(subscription_link: str, event_report: list[MonitoringEventReport]) -> MonitoringNotification:
    log.info(f"I have received the event report for subscription: {subscription_link}") 
    return MonitoringNotification(subscription=subscription_link, monitoringEventReports=event_report)

async def send_notification(callback_url: str, monitoring_notification: MonitoringNotification) -> None:
    async with httpx.AsyncClient() as client:
        log.info(f"Sending Monitoring Notification: {monitoring_notification}")
        try:
            result = await client.post(callback_url, json=monitoring_notification.model_dump())
            if result.status_code == status.HTTP_204_NO_CONTENT:
                log.info("Notification sent successfully")
            else:
                log.warning(f"Unexpected response status: {result.status_code}")
        except httpx.TimeoutException as exc:
            log.error("Timeout sending callback information from NEF", exc_info=exc)
        except httpx.RequestError as exc:
            log.error("Request error sending callback information from NEF", exc_info=exc)
