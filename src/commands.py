from rich.console import Console
from .modals import ValorantTracker

console = Console()

def setup_commands(client):
    @client.tree.command(
        name="track",
        description="Track a Valorant player's stats"
    )
    async def track(interaction):
        console.print(f"[bold blue]Track command triggered by {interaction.user} in {interaction.guild.name}[/bold blue]")
        await interaction.response.send_modal(ValorantTracker())