code for automatically editing and updating the dataset that DLD provides

# Requirements
To install requirements, run the command below in your terminal
```bash
pip install -r requirements.txt
```
# How to Use 
To use the code below without any security issues run simply these instructions:
1. To work with API provided by DLD you must have Security and access keys. include your keys in environmental variables using the following commands
```bash
    export DUBAI_KEY=<YOUR KEY>
    export DUBAI_SEC=<YOUR SECURITY>
```
2. Run the command below in the current working directory
```bash
    export PYTHONPATH={PWD}
```
3. Download your base dataset from this [LINK](https://www.dubaipulse.gov.ae/data/dld-transactions/dld_transactions-open) and place it in **Data** folder in ./src \
*note*: do not rename the dataset file

4. Datasets provided by DLD have some structural issues. To solve them run the code provided in the csv_edit folder by using the below command
```bash
    python ./src/csv_edit/main.py
```

5. run the API call code for receiving the newest data like below:
```bash
    python ./src/API-call/main.py
```
6. After running any of the part 4 or 5 commands you will get a massage to select with the dataset you want to do processes on it. Select it with a valid entry

the final file will be replaced in your **Data** folder
