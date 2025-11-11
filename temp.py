from notion_client import Client
from key import *

"""
This is working on notion_client version 2.4.0 not 2.7.0
2.7.0 does not have query() but does have extract_database_id() which is kind of nice
2.4.0 is working but might have compatibility issues further testing is needed. 
"""

# Initialize client with your token
notion = Client(auth=secret)
print("Client created Successfully...")

# Your database ID
database_id = SAO_page_id
print(f"Database ID: {database_id}")

try:
    response = notion.databases.query(database_id=database_id)
    print("Success.")

    for page in response['results']:
        properties = page['properties']
        print(properties)

except Exception as e:
    print(f"Error Type: {type(e).__name__}")
    print(f"Error Message: {e}")