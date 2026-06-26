import os
from dotenv import load_dotenv
load_dotenv()
from db.mongo_client import get_database

db = get_database()
if db is not None:
    print('DB connected. Collections:', db.list_collection_names())
    chat_sessions = list(db['live_chat_sessions'].find({}))
    print(f'Found {len(chat_sessions)} live chat sessions in DB.')
    for s in chat_sessions:
        print(f'User {s.get("user_id")}: {len(s.get("messages", []))} messages')
        if s.get("messages"):
            print('Sample message:', s.get("messages")[0])
else:
    print("Database connection failed.")
