import pandas as pd
from loguru import logger

from src.Data import DATA_DIR

logger.info("openning files...")

old_transactions_df = pd.read_csv(DATA_DIR / "Transactions.csv")

logger.info("editting transactions file")

# Converting all data in column <instance_date> to date format for removing useless data
old_transactions_df["instance_date"] = pd.to_datetime(
    old_transactions_df["instance_date"]
)

# Sorting by decending order
old_transactions_df = old_transactions_df.sort_values("instance_date", ascending=False)

logger.info("saving editted file")

old_transactions_df.to_csv(DATA_DIR / "Transactions.csv", mode="w", index=False)

logger.info("editted file saved successfuly")
