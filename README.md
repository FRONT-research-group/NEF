# NEF - MonitoringEvent API
Open Source Implementation of NEF MonitoringEvent API that can be integrated in 5G Core Systems (like Open5GS) deployed as a service.

## Features

- **3GPP NEF MonitoringEvent API:** This service provides endpoints based on TS29.122 that exposure the location of a UE connected to 5G Core as a polygon shape resolution.  
- **Flexible Deployment:** Supports deployment via Docker Compose.
- **LocationRetrieval as Monitoring Type:** Implement Location Retriaval as Monitoring Type by supporting Current Location query operations and Last Known Location as well.

## Getting Started
### Prerequisites
Docker and Docker compose

### Clone the Repo
```
git clone https://github.com/FRONT-research-group/NEF.git
cd NEF
git checkout integrate_security
```
after fetching from origin.

## Deployment
### Make target
1. `make deploy`
2. The service will be available at `http://localhost:8000`  
3. For **Last_KNOWN_LOCATION** Feature run the `python db_entries_imsi.py` and `python db_entries_event_report.py` that are stored in the `/NEF/init_db_setup`.

## How to Undeploy
### Make target
1. `make clean`
2. If docker external network was not removed undeploy the resource that still uses the docker network called shared, and run again the `make clean` target.

## Configuration
Environment variables can be set in `.env` for Docker Compose.

## Contribution
Contributions are welcome! Please open issues or submit pull requests for improvements.

## License
This project is licensed under the [Apache License 2.0](https://github.com/FRONT-research-group/NEF/blob/main/LICENSE).

## Contact
For questions or support, contact: p.pavlidis@iit.demokritos.gr



