## NYC 311 Dataset

|Column | Description | Type | Notes |
|------|------------|----|-----|
| Unique Key | Unique identifier for each complaint | integer/string | Primary key |
| Created Date | Date and time when the complaint was created | datetime | Format: YYYY-MM-DD HH:MM:SS |
| Closed Date | Date and time when the complaint was closed | datetime | May be empty if not resolved |
| Agency | Abbreviated name of the city agency handling the complaint | string | e.g., NYPD, DOT |
| Agency Name | Full name of the city agency | string | - |
| Problem (formerly Complaint Type) | General type of complaint | string | e.g., Noise, Water Leak |
| Problem Detail (formerly Descriptor) | Detailed description of the complaint | string | Free text |
| Additional Details | Any extra information provided | string | Optional field |
| Location Type | Type of location where incident occurred | string | e.g., Street/Sidewalk, Building |
| Incident Zip | Zip code of the incident location | string | 5-digit code |
| Incident Address | Address of the incident | string | - |
| Street Name | Name of the street where the incident occurred | string | - |
| Cross Street 1 | First intersecting street | string | Optional |
| Cross Street 2 | Second intersecting street | string | Optional |
| Intersection Street 1 | First street at intersection (alternate field) | string | Optional |
| Intersection Street 2 | Second street at intersection (alternate field) | string | Optional |
| Address Type | Type of address provided | string | e.g., Standard, Intersection |
| City | City name | string | Typically "NEW YORK" |
| Landmark | Nearby landmark if applicable | string | Optional |
| Facility Type | Type of facility involved | string | e.g., Park, School |
| Status | Current status of complaint | string | e.g., Open, Closed, Pending |
| Due Date | Date when the complaint is due to be resolved | datetime | May be empty |
| Resolution Description | Explanation of how the complaint was resolved | string | Free text |
| Resolution Action Updated Date | Date when resolution action was last updated | datetime | - |
| Community Board | NYC community board number | integer | 1–59 |
| Council District | NYC council district number | integer | 1–51 |
| Police Precinct | Police precinct number | integer | - |
| BBL | Borough, Block, Lot identifier for property | string | Unique property ID |
| Borough | NYC borough | string | One of: Bronx, Brooklyn, Manhattan, Queens, Staten Island |
| X Coordinate (State Plane) | X coordinate in State Plane system | float | - |
| Y Coordinate (State Plane) | Y coordinate in State Plane system | float | - |
| Open Data Channel Type | Source channel for the complaint | string | e.g., 311 Call Center, Mobile App |
| Park Facility Name | Name of the park involved, if applicable | string | Optional |
| Park Borough | Borough of park facility | string | Optional |
| Vehicle Type | Type of vehicle involved | string | Optional |
| Taxi Company Borough | Borough of taxi company involved | string | Optional |
| Taxi Pick Up Location | Taxi pick-up location | string | Optional |
| Bridge Highway Name | Name of bridge or highway involved | string | Optional |
| Bridge Highway Direction | Direction of travel | string | Optional |
| Road Ramp | Ramp identifier | string | Optional |
| Bridge Highway Segment | Highway segment | string | Optional |
| Latitude | Latitude of incident | float | Decimal degrees |
| Longitude | Longitude of incident | float | Decimal degrees |
| Location | Combined location string | string | Usually "latitude, longitude" |

---

## Yelp Business Dataset
| Column | Description | Type | Notes |
|--------|------------|------|------|
| business_id | Unique Yelp business identifier | string | Primary key |
| name | Business name | string | - |
| address | Street address | string | - |
| city | City where the business is located | string | - |
| state | State code (abbreviation) | string | e.g., NY, CA |
| postal_code | Postal/zip code | string | 5-digit code |
| latitude | Latitude of business | float | Decimal degrees |
| longitude | Longitude of business | float | Decimal degrees |
| stars | Average rating of business | float | 1.0–5.0 |
| review_count | Number of reviews | integer | - |
| is_open | Whether business is open (1) or closed (0) | integer | Binary |
| attributes | Additional business attributes | string | JSON/dictionary format |
| categories | Business categories | string | Comma-separated list |
| hours | Business hours | string | JSON/dictionary format |
