import os
import asyncio
import logging
from dotenv import load_dotenv
from telethon import TelegramClient
from telethon.tl.types import Message
from telethon.errors import SessionPasswordNeededError
import json 
from datetime import datetime
from pathlib import Path
import re

load_dotenv()
API_ID = int(os.getenv("TELEGRAM_API_ID"))
API_HASH = os.getenv("TELEGRAM_API_HASH")
SESSION_NAME = os.getenv("SESISON_NAME", "telegram_scraper")

LOG_DIR = "logs"
os.makedirs(LOG_DIR, exist_ok=True)

logging.basicConfig(
    filename=os.path.join(LOG_DIR,"scraper.log"),
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
    )
logger = logging.getLogger(__name__)


def create_telegram_client():
    return TelegramClient(
        SESSION_NAME,
        API_ID,
        API_HASH
    )
    
async def test_connection(channel_url:str):
    client = create_telegram_client()
    
    await client.start()
    logger.info("Telegram client started successfully")
    
    try:
        channel =   await client.get_entity(channel_url)
        
        print("Connection successful")
        print(channel.title, channel.id)
        
    except Exception as e:
        logger.error(f"Falied to access channel {channel_url}")
        raise
    finally:
        await client.disconnect()
        
async def fetch_channel_messages(
    client: TelegramClient,
    channel_url: str,
    limit: int = None
):
    messages = []
    try:
        channel = await client.get_entity(channel_url)
        async for msg in client.iter_messages(channel, limit=limit):
            message_dict = msg.to_dict()
            
            messages.append(message_dict)
            
        logger.info(
            f"Fetched {len(messages)} messages from {channel.title}"
        )
        return channel.title, messages
    except Exception as e:
        logger.error(f"Error fetching messages from {channel_url}")
        raise
def json_serializer(obj):
    from datetime import datetime
    if isinstance(obj,datetime):
        return obj.isoformat()
    
    return str(obj)
def clean_filename(name: str) -> str:
    name = name.replace(" ", "_")
    return re.sub(r'[<>:"/\\|?*]', "_", name)
   
def save_messages_to_datalake(
    channel_name: str,
    messages:list,
    base_path:str = "../data/raw/telegram_messages"
):
    safe_channel_name = clean_filename(channel_name.lower())
    
    date_partition = datetime.utcnow().strftime("%Y-%m-%d")
    
    output_dir = Path(base_path) / date_partition
    output_dir.mkdir(parents=True, exist_ok=True)
    output_file = output_dir / f"{safe_channel_name}.json"
    
    with open(output_file, "w", encoding='utf-8') as f:
        json.dump(messages, f, ensure_ascii=False, indent=2, default=json_serializer)
        
    logger.info(
        f"Saved{len(messages)} messages to {output_file}"
    )
    
async def download_message_photo(client: TelegramClient, msg, channel_name:str):
    if msg.photo:
        safe_name = clean_filename(channel_name.lower())
        image_dir = Path("../data/raw/images") / safe_name
        image_dir.mkdir(parents=True, exist_ok=True)
        
        image_path = image_dir / f"{msg.id}.jpg"
        await client.download_media(msg, file=image_path)
        logger.info(f"Downloaded image for message {msg.id} in {channel_name}")
    
        