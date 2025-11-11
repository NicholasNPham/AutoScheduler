from notion_client import Client
from key import *

"""
This is working on notion_client version 2.4.0 not 2.7.0
2.7.0 does not have query() but does have extract_database_id() which is kind of nice
2.4.0 is working but might have compatibility issues further testing is needed. 
"""

"""
2a2443b9-74e2-802b-9a1e-ebac75906542
16dd872b-594c-81fe-8df9-000267cf4bb0
2a2443b9-74e2-80c8-b297-c9502026b24f
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
        print(page['id'] + " :")
        print(properties)

except Exception as e:
    print(f"Error Type: {type(e).__name__}")
    print(f"Error Message: {e}")