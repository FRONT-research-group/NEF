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
```

## Deployment
### Docker Compose
1. Build and start service:
   `docker compose up --build`
2. The service will be available at `http://localhost:8080`

## Configuration
Environment variables can be set in `.env` for Docker Compose.

## Contribution
Contributions are welcome! Please open issues or submit pull requests for improvements.

## License
This project is licensed under the [Apache License 2.0](https://github.com/FRONT-research-group/NEF/blob/main/LICENSE).

## Contact
For questions or support, contact: p.pavlidis@iit.demokritos.gr



