import os
from dotenv.main import load_dotenv
import re

load_dotenv()

# Bot setup
PREFIX = "."
BOT_NAME= "Example Nextcord (GitHub)"

#Role IDs

DEVELOPER_ROLE_ID= "811902358157131806"
CONTENT_CREATOR_ROLE_ID= "921787921747550249"
YOUTUBE_PING_ROLE_ID= "921787845784502302"
MINECRAFT_PING_ROLE_ID= "816989544623898665"

def custom_id(view: str, id: int) -> str:
    """create a custom id from the bot name : the view : the identifier"""
    return f"{BOT_NAME}:{view}:{id}"