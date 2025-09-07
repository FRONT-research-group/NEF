import uuid, asyncio

from collections import defaultdict
from fastapi import status,HTTPException

from app.utils.reports_and_notification_helper import fetch_event_report,create_monitoring_notification,send_notification,parse_and_tranform_document_from_db, transform_document_to_event_report, mapper_msisdn_to_imsi
from app.utils.logger import get_app_logger
from app.utils.db_data_handler import DbDataHandler
from app.utils.local_last_known_data import LocalLastKnownData
from app.config import get_settings
from app.schemas.monitoring_event import MonitoringEventSubscriptionRequest, MonitoringEventSubscriptionResponse, MonitoringEventReport, MonitoringType,LocationType

subscriptions_db: dict[str,dict[str,MonitoringEventSubscriptionRequest]] = defaultdict(dict)
task_registry: dict[str,asyncio.Task] = {}

log = get_app_logger()

local_last_known_data = LocalLastKnownData()

settings = get_settings()

async def generate_event_report_and_send_notification(db_data_handler: DbDataHandler,callback_url:str,subscription_link:str, subscription_id:str, af_id: str, msisdn:str, max_num_reps:int, rep_period:int )-> None:
    try:
        for report_num in range(1,max_num_reps+1):
            event_report = await fetch_event_report(db_data_handler,msisdn,report_num,rep_period)
            local_last_known_data.add(msisdn,event_report)
            monitoring_notification = create_monitoring_notification(subscription_link,[event_report])
            if(report_num == max_num_reps):
                log.info(f"This is the last notification for IMSI {msisdn}")
                monitoring_notification.cancelInd = True
            await send_notification(callback_url,monitoring_notification)
    except asyncio.CancelledError:
        log.info(f"task has canceled for subscription {subscription_id}")
    finally:
        await db_data_handler.delete_unique_subscription_for_af_id(af_id,subscription_id)
        log.info(f"Subscription {subscription_id} deleted")
        task_registry.pop(subscription_id)
        log.info(f"Task registry: {task_registry}")
        

async def register_subscription_pef_af(af_id: str, sub_req: MonitoringEventSubscriptionRequest, request_url: str,db_data_handler: DbDataHandler)-> MonitoringEventReport | MonitoringEventSubscriptionResponse :    
    if (sub_req.monitoringType != MonitoringType.LOCATION_REPORTING) or (sub_req.monitoringType == MonitoringType.LOCATION_REPORTING and (sub_req.locationType is None)) or (sub_req.repPeriod is not None and sub_req.maximumNumberOfReports==1):
        log.error("Error occured: Invalid types")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Check monitoringType and locationType"
        )
    else:
        new_subscription_id = str(uuid.uuid4())

        msisdn = sub_req.msisdn

        rep_period = None
        if(sub_req.repPeriod is not None):
            rep_period = sub_req.repPeriod.duration

        #immediate one time  monitoring request
        if(sub_req.locationType == LocationType.LAST_KNOWN):
            if settings.cache_in_mongo:
                imsi = await mapper_msisdn_to_imsi(db_data_handler, msisdn)
                if imsi is None:
                    log.error(f"IMSI not found for MSISDN {msisdn}")
                    raise HTTPException(
                        status_code=status.HTTP_404_NOT_FOUND,
                        detail="IMSI not found for the given MSISDN"
                    )
                document_result = await db_data_handler.fetch_report_from_db_cache(imsi)
                log.info(f"Fetched document from cache {document_result}")
                fetched_event_report = transform_document_to_event_report(document_result)
                log.info(f"Event Report fetched: {fetched_event_report}")
                return fetched_event_report
            else:
                return local_last_known_data.query(msisdn)
        
        #one time and continuous monitoring request --> event configuration subscription
        await db_data_handler.register_subscription_in_db(af_id,new_subscription_id,sub_req.model_dump(mode="json"))

        created_resource_url = f"{request_url}/{new_subscription_id}"
        
        max_num_reps = sub_req.maximumNumberOfReports

        task = asyncio.create_task(generate_event_report_and_send_notification(db_data_handler,callback_url=str(sub_req.notificationDestination),subscription_link=created_resource_url,subscription_id=new_subscription_id,af_id=af_id,msisdn=msisdn,max_num_reps=max_num_reps,rep_period=rep_period))
        task_registry[new_subscription_id] = task
        log.info(f"Response sent for AF POST request with IMSI {msisdn}")
        return sub_req.to_response(self_link=created_resource_url)

async def get_subscriptions_per_af(af_id: str, request_url: str, db_data_handler: DbDataHandler) -> list[MonitoringEventSubscriptionResponse]:
    subscriptions_by_af_id = []
    fetched_subscriptions = await db_data_handler.fetch_subscriptions_for_af_id(af_id)
    formatted_subs = parse_and_tranform_document_from_db(fetched_subscriptions)

    if formatted_subs is None:
        log.info("No subscriptions found for this AF")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No subscriptions found for this AF"
        )
    else:
        for subscription in formatted_subs:
            resource_url_path= f"{request_url}/{subscription[0]}"
            subscriptions_by_af_id.append(subscription[1].to_response(self_link=resource_url_path))
    log.info(f"subscriptions per af: {subscriptions_by_af_id}")

    return subscriptions_by_af_id
    
async def get_subscription_per_sub_id(af_id:str, subscription_id:str, request_url: str, db_data_handler: DbDataHandler) -> MonitoringEventSubscriptionResponse:
    fetched_subscription = await db_data_handler.fetch_unique_subscription_for_af_id(af_id,subscription_id)
    if fetched_subscription is not None:
        monitoring_event_request = MonitoringEventSubscriptionRequest(**fetched_subscription["monitoringEventSubscription"])
        resource_url_path= f"{request_url}/{subscription_id}"     
        subscription_info = monitoring_event_request.to_response(self_link=resource_url_path)
        log.info(f"subscription info: {subscription_info}")
        return subscription_info
    else:
        log.info(f"No subscription found for AF with id {af_id} with subscription_id {subscription_id}")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No subscription found for this AF"
        )

async def delete_subscription_by_sub_id(af_id: str, subscription_id: str, db_data_handler: DbDataHandler) -> MonitoringEventReport | None:
    fetched_subscription = await db_data_handler.fetch_unique_subscription_for_af_id(af_id,subscription_id)
    log.info(f"The registry is {task_registry}")
    if fetched_subscription is not None and subscription_id in task_registry:
        log.info(f"Deleting subscription with id {subscription_id} for AF with id {af_id}")
        monitoring_event_request = MonitoringEventSubscriptionRequest(**fetched_subscription["monitoringEventSubscription"])
        monitoring_event_request.msisdn
        imsi = monitoring_event_request.msisdn
        task_registry[subscription_id].cancel()
        return local_last_known_data.query(imsi)
    else:
        log.info(f"No subscription found for AF with id {af_id} with subscription_id {subscription_id}")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No subscription matched"
        )