from typing import Any

from fastapi import APIRouter, Response, status, Request, Depends

from app.utils.db_data_handler import DbDataHandler
from app.schemas.monitoring_event import MonitoringEventSubscriptionRequest, MonitoringEventSubscriptionResponse, MonitoringEventReport,MonitoringNotification,MonitoringNotificationResponse

from app.services import monitoring_event_service as sub_service

from app.utils.db_data_handler import get_db_data_handler, DbDataHandler

router = APIRouter()
invoices_callback_router = APIRouter()

@invoices_callback_router.post("{$request.body.notificationDestination}", description="No Content (successful notification)", response_model=MonitoringNotificationResponse)
async def send_notification(callback_url: str, monitoring_notification: MonitoringNotification) -> None:
    '''Exposure for Swagger Documentation'''
    pass

@router.get("/{scsAsId}/subscriptions",
            description="Read all of the active subscriptions for the AF",
            tags=["MonitoringEvent API AF level GET Operation"], 
            response_model= list[MonitoringEventSubscriptionResponse],
            response_model_exclude_defaults=True)
async def get_subscriptions(scsAsId: str, request: Request, db_data_handler: DbDataHandler = Depends(get_db_data_handler)) -> list[MonitoringEventSubscriptionResponse]:
    return await sub_service.get_subscriptions_per_af(scsAsId, str(request.url), db_data_handler)

@router.post(
        "/{scsAsId}/subscriptions",
        description="Creates a new subscription resource for monitoring event notification",
        tags=["MonitoringEvent API Subscription level POST Operation"],
        responses={status.HTTP_200_OK:{"model":MonitoringEventReport, "description": "200 OK"},
                   status.HTTP_201_CREATED: {"model":MonitoringEventSubscriptionResponse, "description":"201 Created"}},
        response_model_exclude_unset=True,
        callbacks=invoices_callback_router.routes)
async def create_subscription(request: Request, scsAsId: str, sub_req: MonitoringEventSubscriptionRequest, response: Response, db_data_handler: DbDataHandler = Depends(get_db_data_handler)) -> MonitoringEventReport | MonitoringEventSubscriptionResponse:
    post_result = await sub_service.register_subscription_pef_af(scsAsId,sub_req,str(request.url),db_data_handler)
    if isinstance(post_result, MonitoringEventReport):
        response.status_code = status.HTTP_200_OK
        return post_result
    else:
        response.headers["Location"] = str(post_result.self_link)
        response.status_code = status.HTTP_201_CREATED
        return post_result

@router.get("/{scsAsId}/subscriptions/{subscriptionId}",
            description="Read an active subscriptions for the AF and the subscription Id",
            tags=["MonitoringEvent API Subscription level GET Operation"], 
            response_model=MonitoringEventSubscriptionResponse, 
            response_model_exclude_unset=True)
async def get_subscription_by_id(scsAsId:str, subscriptionId:str, request: Request, db_data_handler: DbDataHandler = Depends(get_db_data_handler)) -> MonitoringEventSubscriptionResponse:
    return await sub_service.get_subscription_per_sub_id(scsAsId, subscriptionId, str(request.url), db_data_handler)

#Revisit put
@router.put("/{scsAsId}/subscriptions/{subscriptionId}",
            description="Updates/replaces an existing subscription resource",
            tags=["MonitoringEvent API subscription level PUT Operation"],
            response_model=MonitoringEventSubscriptionResponse,
            response_model_exclude_unset=True)
async def modify_subscription_by_id(scsAsId:str, subscriptionId: str) -> Any:
    '''Future purposes'''
    pass
    
@router.delete("/{scsAsId}/subscriptions/{subscriptionId}",
               description="Deletes an already existing monitoring event subscription",
               tags=["MonitoringEvent API Subscription level DELETE Operation"],
               responses={status.HTTP_200_OK:{"model":list[MonitoringEventReport], "description": "200 OK"},
                          status.HTTP_204_NO_CONTENT: {"description":"204 No Content"}},
               response_model_exclude_unset=True)
async def delete_subscription_by_id(scsAsId:str, subscriptionId: str, response:Response, db_data_handler: DbDataHandler = Depends(get_db_data_handler)) -> MonitoringEventReport | None:
    result = await sub_service.delete_subscription_by_sub_id(scsAsId, subscriptionId, db_data_handler)
    if result:
        response.status_code = status.HTTP_200_OK
        return result
    else:
        response.status_code = status.HTTP_204_NO_CONTENT