# Logistic optimization: Delivery drivers location optimisation with Causal Inference

## Project Overview
This project aims to optimize the placement of delivery drivers (referred to as pilots) for Gokada, Nigeria's largest last-mile delivery service. Gokada has encountered issues with the sub-optimal placement of pilots, leading to a high number of unfulfilled delivery requests. Using causal inference, we aim to identify the primary causes of these unfulfilled requests and recommend optimal driver locations to enhance order completion rates.

## Business need
Gokada partners with motorbike owners and drivers to deliver parcels across Lagos, Nigeria. The company has completed over a million deliveries with a fleet of more than 1200 riders. The challenge is to reduce the number of unfulfilled delivery requests by optimizing the placement of drivers. This optimization will help improve client satisfaction and business growth.


## Data
Four datasets are used:

- Completed Orders
   - Columns: Trip ID, Trip Origin, Trip Destination, Trip Start Time, Trip End Time
- Delivery Requests
   - Columns: id, order_id, driver_id, driver_action, lat, lng, created_at, updated_at
- Holiday 
    - Columns: date, name, type
- Weather
    - Columns: date, temperature, rain

## Folder Structure
- `data/`: Contains the datasets.
- `scripts/`: Contains the Python scripts for data processing, feature engineering, and modeling.
- `notebooks/`: Contains Jupyter notebooks for analysis.
- `trip_history/`: Displays the trip history of multiple trips.
- `screenshots/`: Contains important screenshots of the project.
- `config/`: Contains configuration files.
- `requirements.txt`: List of dependencies.
- `README.md`: Project documentation.

## Setup
1. Set up a virtual environment:
    ``` sh
    python3 -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
    ```
2. Install the dependencies `pip install -r requirements.txt`
3. Configure API keys in `config/config.yaml`.

## Usage
1. Configure API keys in `config/config.yaml`.
2. Run data loading and preprocessing
3. Fetch and add external data
4. Perform EDA and causal inference
5. Conduct model training

## License

This project is licensed under the MIT License.


## Contributors

- [@abyt101](https://github.com/AbYT101) - Abraham Teka

<br>

## Challenge by

![10 Academy](https://static.wixstatic.com/media/081e5b_5553803fdeec4cbb817ed4e85e1899b2~mv2.png/v1/fill/w_246,h_106,al_c,q_85,usm_0.66_1.00_0.01,enc_auto/10%20Academy%20FA-02%20-%20transparent%20background%20-%20cropped.png)