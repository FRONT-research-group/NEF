from collections import defaultdict

from app.schemas.monitoring_event import MonitoringEventReport

class LocalLastKnownData:
    def __init__(self):
        self.msisdn_lookup = defaultdict(MonitoringEventReport)

    def add(self, msisdn:str, event_report: MonitoringEventReport) -> None:
        self.msisdn_lookup[msisdn] = event_report

    def query(self, msisdn) -> MonitoringEventReport:
        return self.msisdn_lookup.get(msisdn, MonitoringEventReport)