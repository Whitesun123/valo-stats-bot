import discord
from ..config import EMOJI_GUILD_ID

def get_agent_emoji(client, agent_name):
    emoji_guild = client.get_guild(EMOJI_GUILD_ID)
    if emoji_guild:
        emoji = discord.utils.get(emoji_guild.emojis, name=agent_name)
        return str(emoji) if emoji else agent_name[:6]
    return agent_name[:6]

def get_rank_emoji(client, rank_name):
    emoji_guild = client.get_guild(EMOJI_GUILD_ID)
    if not emoji_guild:
        return ''

    if not rank_name or rank_name == "Unranked":
        emoji_name = "Unranked_Rank"
    else:
        if "Ascendant" in rank_name:
            number = rank_name[-1]
            emoji_name = f"Ascendant_{number}_Rank"
        elif "Immortal" in rank_name:
            number = rank_name[-1]
            emoji_name = f"Immortal_{number}_Rank"
        elif "Diamond" in rank_name:
            number = rank_name[-1]
            emoji_name = f"Diamond_{number}_Rank"
        elif "Platinum" in rank_name:
            number = rank_name[-1]
            emoji_name = f"Platinum_{number}_Rank"
        elif "Gold" in rank_name:
            number = rank_name[-1]
            emoji_name = f"Gold_{number}_Rank"
        elif "Silver" in rank_name:
            number = rank_name[-1]
            emoji_name = f"Silver_{number}_Rank"
        elif "Bronze" in rank_name:
            number = rank_name[-1]
            emoji_name = f"Bronze_{number}_Rank"
        elif "Iron" in rank_name:
            number = rank_name[-1]
            emoji_name = f"Iron_{number}_Rank"
        elif rank_name == "Radiant":
            emoji_name = "Radiant_Rank"
        else:
            emoji_name = "Unranked_Rank"
    
    emoji = discord.utils.get(emoji_guild.emojis, name=emoji_name)
    return str(emoji) if emoji else ''