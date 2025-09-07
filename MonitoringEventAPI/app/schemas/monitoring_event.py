from typing import Optional, List
from enum import Enum
from datetime import datetime

from pydantic import BaseModel, Field, IPvAnyAddress, AnyHttpUrl

#{apiRoot}/3gpp-monitoring-event/v1
#Applicability location notification NEF northbound API feature, e.g. Location Reporting Monitor Type

#The enumeration Accuracy represents a desired granularity of accuracy of the requested location information.
class Accuracy(str,Enum):
    cgi_ecgi = "CGI_ECGI" # The AF requests to be notified using cell level location accuracy.
    ta_ra = "TA_RA" # The AF requests to be notified using TA/RA level location accuracy.
    geo_area = "GEO_AREA" # The AF requests to be notified using the geographical area accuracy.
    civic_addr = "CIVIC_ADDR" # The AF requests to be notified using the civic address accuracy. #EDGEAPP

class PlmnId(BaseModel):
    mcc: str = Field(...,description="String encoding a Mobile Country Code, comprising of 3 digits.")
    mnc: str = Field(...,description="String encoding a Mobile Network Code, comprising of 2 or 3 digits.")

class DurationSec(BaseModel):
    duration: int = Field(0,description="Unsigned integer identifying a period of time in units of seconds")

class DurationMin(BaseModel):
    duration: int = Field(0,description="Unsigned integer identifying a period of time in units of minutes",ge=0)

class LocationFailureCause(str,Enum):
    position_denied = "POSITIONING_DENIED" # Positioning is denied.
    unsupported_by_ue = "UNSUPPORTED_BY_UE" # Positioning is not supported by UE.
    not_registered_ue = "NOT_REGISTERED_UE" # UE is not registered.
    unspecified = "UNSPECIFIED" # Unspecified cause.


# class SupportedGADShapes(str,Enum):
#     point = "POINT" # Point shape
#     point_uncertainty_circle = "POINT_UNCERTAINTY_CIRCLE"


class GeographicalCoordinates(BaseModel):
    lon: float = Field(..., description="Longitude coordinate.")
    lat: float = Field(..., description="Latitude coordinate.")

class PointList(BaseModel):
    geographical_coords: list[GeographicalCoordinates] = Field(..., description="List of geographical coordinates defining the points.",min_length=3,max_length=15)

class Polygon(BaseModel):
    point_list: PointList = Field(..., description="List of points defining the polygon.")

class GeographicArea(BaseModel):
    polygon: Optional[Polygon] = Field(None, description="Identifies a polygonal geographic area.")

#This data type represents the user location information which is sent from the NEF to the AF.
class LocationInfo(BaseModel):
    ageOfLocationInfo: DurationMin | None = Field(None,description="Indicates the elapsed time since the last network contact of the UE.")
    cellId: Optional[str] = Field(None, description="Cell ID where the UE is located.")
    trackingAreaId: Optional[str] = Field(None, description="TrackingArea ID where the UE is located.")
    enodeBId: Optional[str] = Field(None, description="eNodeB ID where the UE is located.")
    routingAreaId: Optional[str] = Field(None, description="Routing Area ID where the UE is located")
    plmnId: Optional[PlmnId] = Field(None, description="PLMN ID where the UE is located.")
    twanId: Optional[str] = Field(None, description="TWAN ID where the UE is located.")
    geographicArea: GeographicArea | None = Field(None,description="Identifies a geographic area of the user where the UE is located.")

#If locationType set to "LAST_KNOWN_LOCATION", the monitoring event request from AF shall be only for one-time monitoring request
class LocationType(str,Enum):
    CURRENT_LOCATION =  "CURRENT_LOCATION" # The AF requests to be notified for current location.
    LAST_KNOWN = "LAST_KNOWN_LOCATION" # The AF requests to be notified for last known location.

#This data type represents a monitoring event type.
class MonitoringType(str, Enum):
    LOCATION_REPORTING = "LOCATION_REPORTING"

# This data type represents a monitoring event notification which is sent from the NEF to the AF.
class MonitoringEventReport(BaseModel):
    externalId: Optional[str] = Field(None,description="Identifies a user, clause 4.6.2 TS 23.682") 
    msisdn: Optional[str] = Field(None,description="Identifies the MS internal PSTN/ISDN number allocated for a UE.")
    locationInfo: Optional[LocationInfo] = Field(None, description="Indicates the user location related information.")
    locFailureCause: Optional[LocationFailureCause] = Field(None, description="Indicates the location positioning failure cause.")
    monitoringType: MonitoringType = Field(..., description="Identifies the type of monitoring as defined in clause 5.3.2.4.3.")
    eventTime: Optional[datetime] = Field(None, description="Identifies when the event is detected or received. Shall be included for each group of UEs.")

class MonitoringEventSubscriptionRequest(BaseModel):
    accuracy: Optional[Accuracy] = Field(None,description="Accuracy represents a desired granularity of accuracy of the requested location information.")
    externalId: Optional[str] = Field(None, description="Identifies a user clause 4.6.2 TS 23.682 (optional)")
    msisdn: Optional[str] = Field(None,description="Identifies the MS internal PSTN/ISDN number allocated for a UE.")
    ipv4Addr: Optional[IPvAnyAddress] = Field(None,description="Identifies the Ipv4 address.")
    ipv6Addr: Optional[IPvAnyAddress] = Field(None,description="Identifies the Ipv6 address.")
    notificationDestination: AnyHttpUrl = Field(..., description="URI of a notification destination that the T8 message shall be delivered to.")
    monitoringType: MonitoringType = Field(..., description="Enumeration of monitoring type. Refer to clause 5.3.2.4.3.")
    maximumNumberOfReports: Optional[int] = Field(None, description="Identifies the maximum number of event reports to be generated by the AMF to the NEF and then the AF.")
    monitorExpireTime: Optional[datetime] = Field(None, description="Identifies the absolute time at which the related monitoring event request is considered to expire.")
    locationType: Optional[LocationType] = Field(None, description="Indicates whether the request is for Current Location, Initial Location, or Last Known Location.")
    repPeriod: Optional[DurationSec] = Field(None,description="Identifies the periodic time for the event reports.")
    minimumReportInterval: Optional[DurationSec] = Field(None,description="identifies a minimum time interval between Location Reporting notifications")

    def to_response(self,self_link:str) -> "MonitoringEventSubscriptionResponse":
        return MonitoringEventSubscriptionResponse(
            self_link=self_link,
            externalId=self.externalId,
            msisdn=self.msisdn,
            ipv4Addr=self.ipv4Addr,
            ipv6Addr=self.ipv6Addr,
            monitoringType=self.monitoringType,
            maximumNumberOfReports=self.maximumNumberOfReports,
            monitorExpireTime=self.monitorExpireTime
        )

class MonitoringEventSubscriptionResponse(BaseModel):
    self_link: AnyHttpUrl = Field(..., description="Supplied by NEF in HTTP responses, Individual Monitoring Event Subscription, Cardinality optional.")
    externalId: Optional[str] = Field(None, description="Identifies a user clause 4.6.2 TS 23.682 (optional)")
    msisdn: Optional[str] = Field(None,description="Identifies the MS internal PSTN/ISDN number allocated for a UE.")
    ipv4Addr: Optional[IPvAnyAddress] = Field(None,description="Identifies the Ipv4 address.")
    ipv6Addr: Optional[IPvAnyAddress] = Field(None,description="Identifies the Ipv6 address.")
    monitoringType: MonitoringType = Field(..., description="Enumeration of monitoring type. Refer to clause 5.3.2.4.3.")
    maximumNumberOfReports: Optional[int] = Field(None, description="Identifies the maximum number of event reports to be generated by the AMF to the NEF and then the AF.")
    monitorExpireTime: Optional[datetime] = Field(None, description="Identifies the absolute time at which the related monitoring event request is considered to expire.")
    monitoringEventReport: Optional[MonitoringEventReport] = Field(None, description="Identifies a monitoring event report which is sent from the NEF to the AF.")

class MonitoringEventSubscriptionPatch(BaseModel):
    pass

# This data type represents a monitoring notification which is sent from the NEF to the AF.
class MonitoringNotification(BaseModel):
    subscription: AnyHttpUrl = Field(..., description="Link to the subscription resource to which this notification is related.")
    monitoringEventReports: Optional[List[MonitoringEventReport]] = Field(None, description="Each element identifies a monitoring event report (optional).")
    cancelInd: Optional[bool] = Field(False,description="Indicates whether to request to cancel the corresponding monitoring subscription. Set to false or omitted otherwise.")

class MonitoringNotificationResponse(BaseModel):
    pass