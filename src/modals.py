import discord
from discord.ui import Modal, TextInput, View
from rich.console import Console
from .components.buttons import GraphButton
from .utils.api import (
    get_account_data,
    get_mmr_data,
    get_matches_data,
    get_mmr_history,
    process_matches_data,
    calculate_match_stats
)
from .utils.emoji import get_agent_emoji, get_rank_emoji

console = Console()

class ValorantTracker(Modal, title='Track Valorant Player'):
    name_input = TextInput(
        label='Name',
        placeholder='Enter player name...',
        required=True,
    )
    tag_input = TextInput(
        label='Tag',
        placeholder='Enter player tag...',
        required=True,
    )

    def get_rr_max(self, rank):
        """Get the maximum RR based on rank."""
        if rank == "Immortal 1":
            return 100
        elif rank == "Immortal 2":
            return 200
        elif rank == "Immortal 3":
            return 550
        return 100

    async def on_submit(self, interaction: discord.Interaction):
        await interaction.response.defer()

        try:
            account_data = get_account_data(self.name_input.value, self.tag_input.value)
            puuid = account_data['puuid']
            account_level = account_data['account_level']
            card_id = account_data['card']
            card_banner = f"https://media.valorant-api.com/playercards/{card_id}/wideart.png"

            mmr_data = get_mmr_data(puuid)
            current_rank = "Unranked"
            peak_rank = "Unranked"
            current_rr = "N/A"

            if mmr_data:
                current_rank = mmr_data['current_data']['currenttierpatched']
                peak_rank = mmr_data['highest_rank']['patched_tier']
                current_rr = mmr_data['current_data'].get('ranking_in_tier', 'N/A')

            matches_data = get_matches_data(puuid)
            if not matches_data:
                await interaction.followup.send("No match data found")
                return

            processed_matches = process_matches_data(matches_data, puuid)
            kd_ratio, shot_percentages = calculate_match_stats(processed_matches)

            mmr_history = get_mmr_history(puuid)
            rr_changes = {}
            if mmr_history and 'history' in mmr_history:
                for match in mmr_history['history']:
                    rr_changes[match['match_id']] = match['last_change']

            embed = discord.Embed(
                title=f"Valorant Stats for {self.name_input.value}#{self.tag_input.value}",
                color=discord.Color.from_rgb(52, 64, 80)
            )

            current_rank_emoji = get_rank_emoji(interaction.client, current_rank)
            peak_rank_emoji = get_rank_emoji(interaction.client, peak_rank)

            embed.add_field(name="Current Rank", value=f"{current_rank} {current_rank_emoji}", inline=True)
            embed.add_field(name="Peak Rank", value=f"{peak_rank} {peak_rank_emoji}", inline=True)
            embed.add_field(name='', value='', inline=False)
            embed.add_field(name="Current RR", value=f"{current_rr} / {self.get_rr_max(current_rank)}", inline=True)
            embed.add_field(name="Account Level", value=account_level, inline=True)
            embed.add_field(name="KD", value=f"{kd_ratio}", inline=True)
            embed.add_field(
                name="Head | Body | Legs", 
                value=f"{shot_percentages['hs_percentage']:^2}% | {shot_percentages['body_percentage']:^2}% | {shot_percentages['leg_percentage']}%", 
                inline=True
            )

            if processed_matches:
                matches_display = []
                for match in processed_matches:
                    agent_emoji = get_agent_emoji(interaction.client, match['agent'])
                    rr_change = rr_changes.get(match['match_id'], 'N/A')
                    rr_display = f"+{rr_change}" if isinstance(rr_change, (int, float)) and rr_change > 0 else str(rr_change)

                    match_line = (
                        f"`{match['gamemode'][:11].ljust(11)} │ {match['map'][:7].ljust(7)} │ {match['score']:5} │ {match['kills']}/{match['deaths']}/{match['assists']:1}".ljust(41) + f"│`  {agent_emoji} `│ RR: {rr_display:>3}`"
                    )
                    matches_display.append(match_line)

                embed.add_field(name="Recent Matches", value="\n".join(matches_display), inline=False)
            else:
                embed.add_field(name="Recent Matches", value="No recent matches found", inline=False)

            if card_banner:
                embed.set_image(url=card_banner)

            embed.set_footer(text="Format: Gamemode | Map | K/D/A | Agent | RR Change")

            view = View(timeout=180)
            graph_button = GraphButton(processed_matches, f"{self.name_input.value}#{self.tag_input.value}")
            view.add_item(graph_button)

            await interaction.followup.send(embed=embed, view=view)

        except Exception as e:
            console.print("[bold red]Error occurred:[/bold red]", str(e))
            console.print("[bold red]Full error:[/bold red]")
            console.print_exception()
            await interaction.followup.send(f"An error occurred: {str(e)}")