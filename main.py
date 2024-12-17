import discord
from discord import app_commands
from rich.console import Console
import os
from dotenv import load_dotenv
from src.modals import ValorantTracker

load_dotenv()
DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')

console = Console()

class Client(discord.Client):
    def __init__(self):
        intents = discord.Intents.default()
        intents.message_content = True
        super().__init__(intents=intents)
        self.tree = app_commands.CommandTree(self)

    async def setup_hook(self):
        await self.tree.sync()
        console.print("[bold green]Commands synced![/bold green]")

client = Client()

@client.event
async def on_ready():
    console.print(f"[bold green]Logged in as {client.user}[/bold green]")

@client.tree.command(name="track", description="Track a Valorant player's stats")
async def track(interaction: discord.Interaction):
    console.print(f"[bold blue]Track command triggered by {interaction.user}[/bold blue]")
    await interaction.response.send_modal(ValorantTracker())

def main():
    console.print("[bold yellow]Starting bot...[/bold yellow]")
    try:
        client.run(DISCORD_TOKEN)
    except Exception as e:
        console.print(f"[bold red]Error starting bot: {e}[/bold red]")

if __name__ == "__main__":
    main()