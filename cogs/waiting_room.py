import discord
from discord.ui import View, Button
from discord import app_commands
from discord.ext import commands


ROLE_ENGLISH_ID = 1536841233677287544
ROLE_PT_PT_ID = 1536840684814737518
ROLE_PT_BR_ID = 1536843358100656259


class LanguageView(View):

    def __init__(self):
        super().__init__(timeout=None)

    async def select_language(
        self,
        interaction: discord.Interaction,
        role_id: int,
        language_name: str
    ):

        guild = interaction.guild
        member = interaction.user

        if guild is None:
            await interaction.response.send_message(
                "❌ This button can only be used inside the server.",
                ephemeral=True
            )
            return

        selected_role = guild.get_role(role_id)

        if selected_role is None:
            await interaction.response.send_message(
                "❌ This language role has not been configured yet.",
                ephemeral=True
            )
            return

        language_roles = [
            ROLE_ENGLISH_ID,
            ROLE_PT_PT_ID,
            ROLE_PT_BR_ID
        ]

        # Remove o idioma anterior
        for role in member.roles:

            if role.id in language_roles and role.id != role_id:

                try:
                    await member.remove_roles(role)
                except discord.Forbidden:
                    pass

        # Adiciona o novo idioma
        try:
            await member.add_roles(selected_role)

        except discord.Forbidden:
            await interaction.response.send_message(
                "❌ I don't have permission to manage this role.",
                ephemeral=True
            )
            return

        await interaction.response.send_message(
            f"✅ **{language_name}** selected!",
            ephemeral=True
        )

    @discord.ui.button(
        label="Portuguese (PT)",
        emoji="🇵🇹",
        style=discord.ButtonStyle.primary,
        custom_id="hustler_language_pt_pt"
    )
    async def portuguese_pt(
        self,
        interaction: discord.Interaction,
        button: Button
    ):

        await self.select_language(
            interaction,
            ROLE_PT_PT_ID,
            "Portuguese (PT)"
        )

    @discord.ui.button(
        label="Portuguese (BR)",
        emoji="🇧🇷",
        style=discord.ButtonStyle.primary,
        custom_id="hustler_language_pt_br"
    )
    async def portuguese_br(
        self,
        interaction: discord.Interaction,
        button: Button
    ):

        await self.select_language(
            interaction,
            ROLE_PT_BR_ID,
            "Portuguese (BR)"
        )

    @discord.ui.button(
        label="English (EN)",
        emoji="🇬🇧",
        style=discord.ButtonStyle.primary,
        custom_id="hustler_language_english"
    )
    async def english(
        self,
        interaction: discord.Interaction,
        button: Button
    ):

        await self.select_language(
            interaction,
            ROLE_ENGLISH_ID,
            "English (EN)"
        )


def create_embed():

    embed = discord.Embed(
        description=(
            "Welcome, Hustler.\n\n"
            "Please select your language:\n\n"
            "🇵🇹 Portuguese (PT)\n"
            "🇧🇷 Portuguese (BR)\n"
            "🇬🇧 English (EN)"
        ),
        color=discord.Color.from_rgb(123, 63, 242)
    )

    return embed


class WaitingRoom(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(
        name="waitingroom",
        description="Send the Hustler recruitment waiting room"
    )
    async def waitingroom(
        self,
        interaction: discord.Interaction
    ):

        await interaction.channel.send(
            embed=create_embed(),
            view=LanguageView()
        )

        await interaction.response.send_message(
            "✅ Waiting room message sent.",
            ephemeral=True
        )


async def setup(bot):

    await bot.add_cog(
        WaitingRoom(bot)
    )

    bot.add_view(
        LanguageView()
    )