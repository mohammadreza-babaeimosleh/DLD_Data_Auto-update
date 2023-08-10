from loguru import logger
import os
import requests
import pandas as pd
from src.Data import DATA_DIR
import json
import datetime

valid_inputs = [1, 2, 3]

while True:
    input_command = int(
        input(
            "Please enter one of the mentioned number to access your desiered data:\n1 - DLD_Transaction data\n2 - DLD_Rent_Contracts data\n3 - DLD_Units_Open\n"
        )
    )
    if input_command in valid_inputs:
        input_command = input_command - 1
        break
    else:
        logger.error("Error: Invalid number please try again")

# Setting date parameters
current_date = datetime.date.today()
a_days_ago = current_date - datetime.timedelta(days=1)
two_days_ago = current_date - datetime.timedelta(days=2)

# Loading old dataset for extracting parameters
logger.info("Loading old dataset...")

old_versions_list = ["Transactions.csv", "Rent_Contracts.csv", "Units.csv"]
current_data = pd.DataFrame()

chunk_size = 1000000  # Adjust this value based on your system's memory capacity
for chunk in pd.read_csv(
    DATA_DIR / old_versions_list[input_command], chunksize=chunk_size
):
    current_data = pd.concat([current_data, chunk])
# current_data = pd.read_csv(DATA_DIR / old_versions_list[input_command])

logger.info("Old dataset loaded successfully!!!")

num_data_rows = len(current_data)
logger.info(f"Number of records loaded is: {num_data_rows}")
offset = 0
column_names = current_data.columns.tolist()

# loading Key and Security from environment variables for more safty in open source code
logger.info("Fetching Key and Security...")

API_KEY = os.environ["DUBAI_KEY"]
APY_SEC = os.environ["DUBAI_SEC"]

logger.info("Fetching Key and Security done!!!")

# Requesting for access token
auth_url = "https://api.dubaipulse.gov.ae/oauth/client_credential/accesstoken"
client_id = f"{API_KEY}"
client_secret = f"{APY_SEC}"
grant_type = "client_credentials"

data = {
    "client_id": client_id,
    "client_secret": client_secret,
}

params = {"grant_type": grant_type}

logger.info("Requesting for token...")
response = requests.post(auth_url, params=params, data=data)

if response.status_code == 200:

    access_token = response.json().get("access_token")
    logger.info("Token recieved successfully!!")

    all_columns_empty = 0
    new_df = pd.DataFrame(columns=column_names)
    batch_counter = 1

    url_list = [
        "https://api.dubaipulse.gov.ae/open/dld/dld_transactions-open-api",
        "https://api.dubaipulse.gov.ae/shared/dld/dld_rent_contracts-open-api",
        "https://api.dubaipulse.gov.ae/open/dld/dld_units-open-api",
    ]
    date_instance_list = ["instance_date", "contract_start_date", "creation_date"]

    # Continuously request until reach to the end of database
    while ~all_columns_empty:
        logger.info(f"Requesting for {batch_counter}th batch of data...")

        api_url = url_list[input_command]
        headers = {"Authorization": f"Bearer {access_token}"}

        parameters_to_api_query = {
            "order_by": date_instance_list[input_command],
            "offset": num_data_rows + offset,
        }
        # print(parameters_to_api_query)
        api_response = requests.get(
            api_url, headers=headers, params=parameters_to_api_query
        )

        # Process the API response
        if api_response.status_code == 200:
            logger.info("API call successfull!!!")

            # Convert the JSON response into a Python object
            recived_df = pd.DataFrame(api_response.json()["results"])

            all_columns_empty = recived_df.isnull().all().all()

            logger.info(f"{len(recived_df)} new data added!!!")

            # Checking for if we have reached to the end of database
            if all_columns_empty:
                logger.info("calling ended!!!")
                continue

            # print(recived_df.columns.tolist())
            # Converting all data in column <instance_date> to date format for removing useless data
            recived_df[date_instance_list[input_command]] = pd.to_datetime(
                recived_df[date_instance_list[input_command]]
            )
            # Concat dataframes
            new_df = pd.concat([recived_df, new_df])

            # changing ofset to get next batch of data
            logger.info("Requesting for next batch of data...")
            offset = offset + 1000
            batch_counter += 1

        else:
            logger.info(f"API call failed: {api_response.json()}")
            logger.info("Requesting for new token...")
            response = requests.post(auth_url, params=params, data=data)
            if response.status_code == 200:
                access_token = response.json().get("access_token")
                logger.info("Token recieved successfully!!")
            else:
                logger.error("ERROR!!!!!")

    # Creating final updated dataset
    logger.info("Concating with old data...")

    final_df = pd.concat([new_df, current_data])
    final_df.to_csv(DATA_DIR / old_versions_list[input_command], mode="w", index=False)
    # new_df.to_csv(DATA_DIR / "test.csv", mode="w", index=False)

    logger.info("Concatenation done successfully!!!")
    logger.info(f"{len(new_df)} data added!!!")

else:
    print("Error:", response.json())
    logger.error(f"Error: {response.json()}")
