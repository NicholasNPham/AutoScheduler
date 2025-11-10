from notion_client import Client, extract_database_id
from key import *

notion = Client(auth=secret)

url = "https://www.notion.so/2a2443b974e280c8b297c9502026b24f?v=2a2443b974e280488e99000c13dacab2"
database_id = extract_database_id(url)

# Query the database using direct API call
response = notion._clients[0].post(
    f"https://api.notion.com/v1/databases/{database_id}/query",
    headers={
        "Authorization": f"Bearer {secret}",
        "Notion-Version": "2022-06-28"
    },
    json={}
)

data = response.json()

print(f"Found {len(data['results'])} pages\n")

for page in data['results']:
    properties = page['properties']

    # Extract Name
    if 'Name' in properties:
        name_data = properties['Name']['title']
        name = name_data[0]['plain_text'] if name_data else "No name"
    else:
        name = "No name"

    # Extract Date
    if 'date' in properties and properties['date']['date']:
        date = properties['date']['date']['start']
    else:
        date = "No date"

    print(f"Name: {name}")
    print(f"Date: {date}")
    print("---")