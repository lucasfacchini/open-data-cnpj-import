# Description
This tool imports the brazilian companies open data to a MySQL server.

# Usage

## Download

This may take a while, since it downloads and extracts all files.
```
sh download.sh
```

## Import
Create a database in your MySQL server and run the following, replacing for your credentials
```
python mysql_import.py <host> <port> <user> <password> <database>
```
Note: Python 3.6 or higher is required
