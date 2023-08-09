This is a code for automaticaly edit and update the dataset that is provided by DLD

# Requirements
To install requirements, simply run command below in your terminal
```bash
pip install -r requirements.txt
```
# How to Use 
For using code below without any security issue run simply this instructions:
1. To work with API provided by DLD you must have Security and access keys include your keys. in envorimental variables using folowing commands
```bash
    export DUBAI_KEY=<YOUR KEY>
    export DUBAI_SEC=<YOUR SECURITY>
```
2. Run command below in current working directory
```bash
    export PYTHONPATH={PWD}
```
3. Download your base dataset from this [LINK](https://www.dubaipulse.gov.ae/data/dld-transactions/dld_transactions-open) and place it in **Data** folder in ./src
*note*: do note rename the dataset file

4. Dataset provided by DLD has some structural issues. To solve them run code provided in csv_edit folder by using below command
```bash
    python ./src/csv_edit/main.py
```

5. run tha API call code for recieving the newest data like below:
```bash
    python ./src/API-call/main.py
```
the final file will be replaced in your **Data** folder
