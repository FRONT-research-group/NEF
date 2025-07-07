# NEF
Implementation of NEF in Open5GS and support for CAMARA APIs

This API exposes the functionality of NEF's MonitoringEvent API. There are two location types for the retrieval of a UE's location. The LAST_KNOWN_LOCATION and CURRENT_LOCATION.
Both of these are configured in the request's body of HTTP POST mesage that will be sent to the NEF.

# How to run
A Dockerfile is provided to run the API and the Log Agent for monitoring of a UE's location.

Simply run **docker compose up --build** to deploy the containerized form of the application.

After that, you can open the Swagger UI in the {node_ip:8000}/docs to perform HTTP Operations.

# Dummy configuration data for Swagger UI

Below you can find some dummy configuration data for HTTP POST in Swagger: <br />

```json
{
	"accuracy": "CGI_ECGI",
	"msisdn": "001010143245445",
	"notificationDestination": "http://test_server:8001",
	"monitoringType": "LOCATION_REPORTING",
	"maximumNumberOfReports": 3,
	"monitorExpireTime": "2025-04-11T07:18:26.978Z",
	"locationType": "CURRENT_LOCATION",
	"repPeriod": {
		"duration": 20
	}
}
```
