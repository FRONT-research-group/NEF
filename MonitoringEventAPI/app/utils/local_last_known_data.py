from collections import defaultdict

from app.schemas.monitoring_event import MonitoringEventReport, MonitoringType,LocationFailureCause

class LocalLastKnownData:
    def __init__(self):
        self.last_known_lookup = defaultdict(lambda: defaultdict(MonitoringEventReport))

    def add(self, af_id:str, msisdn:str, event_report: MonitoringEventReport) -> None:
        self.last_known_lookup[af_id][msisdn] = event_report

    def query(self,af_id:str, msisdn:str) -> MonitoringEventReport:
        retrieved_af = self.last_known_lookup.get(af_id)
        if retrieved_af is not None:
            return retrieved_af.get(msisdn,MonitoringEventReport(msisdn=msisdn,monitoringType=MonitoringType.LOCATION_REPORTING,locFailureCause=LocationFailureCause.NOT_REGISTERED_UE))
        return MonitoringEventReport(msisdn=msisdn,monitoringType=MonitoringType.LOCATION_REPORTING,locFailureCause=LocationFailureCause.NOT_REGISTERED_UE)