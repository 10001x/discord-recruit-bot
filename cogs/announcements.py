import discord
from discord.ext import commands


class AnnouncementModal(discord.ui.Modal, title="Create Announcement"):

    title_input = discord.ui.TextInput(
        label="Título",
        placeholder="Ex: Recruitment Update",
        required=True,
        max_length=256
    )

    message_input = discord.ui.TextInput(
        label="Mensagem",
        placeholder="Escreve o conteúdo do anúncio...",
        style=discord.TextStyle.paragraph,
        required=True,
        max_length=4000
    )

    footer_input = discord.ui.TextInput(
        label="Footer",
        placeholder="Ex: Hustler Recruitment",
        required=False,
        max_length=200
    )

    async def on_submit(self, interaction: discord.Interaction):

        embed = discord.Embed(
            title=self.title_input.value,
            description=self.message_input.value,
            color=discord.Color.from_rgb(123, 63, 242)
        )

        if self.footer_input.value:
            embed.set_footer(
                text=self.footer_input.value
            )

        embed.timestamp = discord.utils.utcnow()

        await interaction.channel.send(
            embed=embed
        )

        await interaction.response.send_message(
            "✅ Announcement sent.",
            ephemeral=True
        )


class Announcements(commands.Cog):

    def __init__(self, bot):
        self.bot = bot


    @discord.app_commands.command(
        name="announce",
        description="Create and send an announcement"
    )
    async def announce(
        self,
        interaction: discord.Interaction
    ):

        await interaction.response.send_modal(
            AnnouncementModal()
        )


async def setup(bot):

    await bot.add_cog(
        Announcements(bot)
    )