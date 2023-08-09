from loguru import logger
import os
import requests
import pandas as pd
from src.Data import DATA_DIR
import json
import datetime

# Setting date parameters
current_date = datetime.date.today()
a_days_ago = current_date - datetime.timedelta(days=1)
two_days_ago = current_date - datetime.timedelta(days=2)

# Loading old dataset for extracting parameters
current_data = pd.read_csv(DATA_DIR / "Transactions.csv")
num_data_rows = len(current_data)
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

    # Continuously request until reach to the end of database
    while ~all_columns_empty:
        logger.info(f"Requesting for {batch_counter}th batch of data...")

        api_url = "https://api.dubaipulse.gov.ae/open/dld/dld_transactions-open-api"
        headers = {"Authorization": f"Bearer {access_token}"}

        parameters_to_api_query = {
            "order_by": "instance_date",
            "offset": num_data_rows + offset,
        }
        api_response = requests.get(
            api_url, headers=headers, params=parameters_to_api_query
        )

        # Process the API response
        if api_response.status_code == 200:
            logger.info("API call successfull!!!")

            # Convert the JSON response into a Python object
            recived_df = pd.DataFrame(api_response.json()["results"])

            all_columns_empty = recived_df.isnull().all().all()

            # Checking for if we have reached to the end of database
            if all_columns_empty:
                logger.info("calling ended!!!")
                continue

            # Converting all data in column <instance_date> to date format for removing useless data
            recived_df["instance_date"] = pd.to_datetime(recived_df["instance_date"])
            # Concat dataframes
            new_df = pd.concat([recived_df, new_df])

            # changing ofset to get next batch of data
            logger.info("Requesting for next batch of data...")
            offset = offset + 1000

        else:
            logger.error(f"API call failed: {api_response.json()}")

    # Creating final updated dataset
    logger.info("Concating with old data...")

    final_df = pd.concat([new_df, current_data])
    final_df.to_csv(DATA_DIR / "Transactions.csv", mode="w", index=False)

    logger.info("Concatenation done successfully!!!")
    logger.info(f"{len(new_df)} data added!!!")

else:
    print("Error:", response.json())
    logger.error(f"Error: {response.json()}")
