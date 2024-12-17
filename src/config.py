import os
from dotenv import load_dotenv

load_dotenv()
DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')
HENRIK_TOKEN = os.getenv('HENRIK_TOKEN')

EMOJI_GUILD_ID = 885881710967926785

RANK_COLORS = {
    "Iron": "#4F5157",
    "Bronze": "#A0715E", 
    "Silver": "#B5B5B5",
    "Gold": "#EBC564",
    "Platinum": "#45CABD",
    "Diamond": "#BB6BF3",
    "Ascendant": "#6CFFA3",
    "Immortal": "#FF5552",
    "Radiant": "#FFFFA7"
}

EMPTY_TRIANGLE_COLOR = "#2C394B"
TRIANGLE_BORDER = "#4F5B66"
TRIANGLE_BG = "#1F2326"