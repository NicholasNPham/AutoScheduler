from notion_client import Client, extract_database_id
from key import *

notion = Client(auth=secret)

url = "https://www.notion.so/2a2443b974e280c8b297c9502026b24f?v=2a2443b974e280488e99000c13dacab2"
database_id = extract_database_id(url)

# This might be because of work firewall ill just push this though.

response = notion._clients[0].post()