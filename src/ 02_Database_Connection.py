import mysql.connector
import pandas as pd
import os
from dotenv import load_dotenv

load_dotenv()
# Connect to MySQL
connection = mysql.connector.connect(
    host="localhost",
    user="root",
    password=os.getenv("MYSQL_PASSWORD"),
    database="mutual_fund_analysis"
)

print("MySQL connection successful")

# Read Mutual Fund data
mf_query = "SELECT * FROM mutual_fund"
mf_data = pd.read_sql(mf_query, connection)

print("Mutual Fund Data:")
print(mf_data.head())

# Read Direct Equity data
equity_query = "SELECT * FROM direct_equity"
direct_equity = pd.read_sql(equity_query, connection)

print("\nDirect Equity Data:")
print(direct_equity.head())

# Close connection
connection.close()

print("\nMySQL connection closed")