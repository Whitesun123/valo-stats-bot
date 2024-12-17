import discord
from discord.ui import Button
from ..utils.graph import create_performance_graph

class GraphButton(Button):
    def __init__(self, matches_data, player_name):
        super().__init__(label="Show Performance Graph", style=discord.ButtonStyle.primary)
        self.matches_data = matches_data
        self.player_name = player_name

    async def callback(self, interaction: discord.Interaction):
        await interaction.response.defer()
        
        buf = create_performance_graph(self.matches_data, self.player_name)
        
        embed = discord.Embed(
            title=f"Performance Graph for {self.player_name}",
            color=discord.Color.from_rgb(44, 47, 51)
        )
        
        file = discord.File(buf, filename='performance_graph.png')
        embed.set_image(url="attachment://performance_graph.png")
        await interaction.followup.send(file=file, embed=embed)