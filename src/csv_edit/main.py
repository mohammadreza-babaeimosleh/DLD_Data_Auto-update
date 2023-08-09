import pandas as pd
from loguru import logger

from src.Data import DATA_DIR

logger.info("openning files...")

df_list = ["Transactions.csv", "Rent_Contracts.csv"]
date_instance_list = ["instance_date", "contract_start_date"]

# Adjust this value based on your system's memory capacity
chunk_size = 1000000

for i in range(df_list):
    old_transactions_df = pd.DataFrame()

    for chunk in pd.read_csv(DATA_DIR / df_list[i], chunksize=chunk_size):
        old_transactions_df = pd.concat([old_transactions_df, chunk])

    logger.info("editting transactions file")

    # Converting all data in column <instance_date> to date format for removing useless data
    old_transactions_df[date_instance_list[i]] = pd.to_datetime(
        old_transactions_df[date_instance_list[i]]
    )

    # Sorting by decending order
    old_transactions_df = old_transactions_df.sort_values(
        date_instance_list[i], ascending=False
    )

    logger.info("saving editted file")

    old_transactions_df.to_csv(DATA_DIR / df_list[i], mode="w", index=False)

    logger.info("editted file saved successfuly")
