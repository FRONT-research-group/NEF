import asyncio, httpx
from fastapi import status,HTTPException

from app.utils.logger import get_app_logger
from app.utils.location_db_data_handler import LocationDbDataHandler
from app.schemas.monitoring_event import MonitoringEventReport, MonitoringType,MonitoringNotification,LocationInfo

log = get_app_logger()

async def fetch_event_report(location_handler: LocationDbDataHandler, imsi:str, current_rep: int, rep_period: int ) -> MonitoringEventReport:
    log.info(f"Processing report for IMSI: {imsi}, Report Number: {current_rep}")
    if rep_period is not None:
        await asyncio.sleep(rep_period)

    fetched_document = await location_handler.find_location_by_imsi(imsi)
    location_info = parse_document_to_ue_location(fetched_document)

    return MonitoringEventReport(msisdn=imsi,locationInfo=location_info,monitoringType=MonitoringType.LOCATION_REPORTING)

def parse_document_to_ue_location(document: dict | None = None) -> LocationInfo:
    if document is None:
          log.error("No event reports received from NEF.")
          raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No subscriptions found for this AF"
        )
    else:
        log.info(f"Fetched Docuement: {document}")
        cell_id = document["amf_info"]["ueLocation"]["nrLocation"]["ncgi"]["nrCellId"]
        tac_id = document["amf_info"]["ueLocation"]["nrLocation"]["tai"]["tac"]
        plmn_id = document["amf_info"]["ueLocation"]["nrLocation"]["tai"]["plmnId"]
        return LocationInfo(cellId=cell_id,trackingAreaId=tac_id,plmnId=plmn_id)

def create_monitoring_notification(subscription_link: str, event_report: list[MonitoringEventReport]) -> MonitoringNotification:
    log.info(f"I have received the event report for subscription: {subscription_link}") 
    return MonitoringNotification(subscription=subscription_link, monitoringEventReports=event_report)

async def send_notification(callback_url: str, monitoring_notification: MonitoringNotification) -> None:
    async with httpx.AsyncClient() as client:
            log.info(f"Monitoring Notification: {monitoring_notification}")
            try:
                result = await client.post(callback_url, json=monitoring_notification.model_dump_json())
                if result.status_code == status.HTTP_204_NO_CONTENT:
                    log.info("Response received successfully")
                else:
                    log.info("Response unrecognizable")
            except httpx.TimeoutException as exc:
                log.error("Error in sending callback information from NEF",exc_info=exc)