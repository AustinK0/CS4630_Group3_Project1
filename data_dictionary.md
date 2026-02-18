## Philly 311 Dataset
| Column               | Description                                      | Type    | Notes                              |
|----------------------|--------------------------------------------------|---------|------------------------------------|
| objectid             | Unique record identifier                         | int64   | Primary key                        |
| service_request_id   | 311 service request ID                           | int64   | Unique per request                 |
| subject              | Brief subject/title of the request               | object  | Free text                          |
| status               | Current status of the request                    | object  | e.g., Open, Closed                 |
| status_notes         | Additional notes on the status                   | object  | Optional, may be empty             |
| service_name         | Type/category of service requested               | object  | e.g., Abandoned Vehicle, Graffiti  |
| service_code         | Code corresponding to the service name           | object  | Internal category code             |
| agency_responsible   | City agency assigned to handle the request       | object  | e.g., Streets Department           |
| service_notice       | Notice or expected response information          | object  | Optional                           |
| requested_datetime   | Date and time when the request was submitted     | object  | Format: YYYY-MM-DD HH:MM:SS       |
| updated_datetime     | Date and time the request was last updated       | object  | Format: YYYY-MM-DD HH:MM:SS       |
| expected_datetime    | Expected completion date and time                | object  | May be empty                       |
| closed_datetime      | Date and time the request was closed             | object  | May be empty if not resolved       |
| address              | Street address of the request                    | object  | -                                  |
| zipcode              | ZIP code of the request location                 | float64 | 5-digit code, has nulls            |
| media_url            | URL to associated media/photo                    | object  | Optional, may be empty             |
| lat                  | Latitude of the request location                 | float64 | Decimal degrees, has nulls         |
| lon                  | Longitude of the request location                | float64 | Decimal degrees, has nulls         |

---

## Yelp Business Dataset
| Column | Description | Type | Notes |
|--------|------------|------|------|
| business_id | Unique Yelp business identifier | object | Primary key |
| name | Business name | object | - |
| address | Street address | object | - |
| city | City where the business is located | object | - |
| state | State code (abbreviation) | object | e.g., NY, CA |
| postal_code | Postal/zip code | object | 5-digit code |
| latitude | Latitude of business | float64 | Decimal degrees |
| longitude | Longitude of business | float64 | Decimal degrees |
| stars | Average rating of business | float64 | 1.0–5.0 |
| review_count | Number of reviews | int64 | - |
| is_open | Whether business is open (1) or closed (0) | int64 | Binary |
| attributes | Additional business attributes | object | JSON/dictionary format |
| categories | Business categories | object | Comma-separated list |
| hours | Business hours | object | JSON/dictionary format |
