from notion_client import Client
from key import *

"""
This is working on notion_client version 2.4.0 not 2.7.0
2.7.0 does not have query() but does have extract_database_id() which is kind of nice
2.4.0 is working but might have compatibility issues further testing is needed. 
Need to add this to autopop.py functional and working testing is need for raspPI 4 and on saturdays.
"""

# Initialize client with your token
notion = Client(auth=secret)
print("Client created Successfully...")

# Your database ID
database_id = SAO_page_id
print(f"Database ID: {database_id}")

response = notion.databases.query(database_id=database_id)
print("Success.")

row_id_list = []

for page in response['results']:

    # This is the row id
    row_id = page['id']
    row_id_list.append(row_id)

    # This is for items in the row
    properties = page['properties']

    # print(row_id, properties)

test_dict = {'SAO10 SHIFT 1': ['2025-11-13T08:00:00-05:00', '2025-11-13T17:00:00-05:00'], 'SAO10 SHIFT 2': ['2025-11-14T08:00:00-05:00', '2025-11-14T17:00:00-05:00'], 'SAO10 SHIFT 3': ['2025-11-15T08:00:00-05:00', '2025-11-15T17:00:00-05:00'], 'SAO10 SHIFT 4': ['2025-11-16T08:00:00-05:00', '2025-11-16T17:00:00-05:00'], 'SAO10 SHIFT 5': ['2025-11-17T08:00:00-05:00', '2025-11-17T17:00:00-05:00']}


# Row 2 and 3 is switched, Quick Fix
row_id_list[1], row_id_list[2] = row_id_list[2], row_id_list[1]

try:
    for i in range(0, 5):
        name = f"SAO10 SHIFT {i + 1}"
        text_property = {"title": [{"text": {"content": name}}]}
        date_property = {"date": {"start": test_dict[f"SAO10 SHIFT {i+1}"][0], "end": test_dict[f"SAO10 SHIFT {i+1}"][1]}}

        full_property = {"Name": text_property, "Date": date_property}

        response = notion.pages.update(page_id=row_id_list[i], properties=full_property)
        print("Property: 'Name' updated Successfully...")

except Exception as e:
    print(f"Error Type: {type(e).__name__}")
    print(f"Error Message: {e}")