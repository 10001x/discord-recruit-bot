import json
import os
import re
from datetime import datetime, timezone

import discord
from discord import app_commands
from discord.ext import commands


# =========================================================
# CONFIGURAÇÃO
# =========================================================

CATEGORY_PT_ID = 1536948353689194506
CATEGORY_BR_ID = 1536948396953178244
CATEGORY_EN_ID = 1536948447737810966

CATEGORY_ACCEPTED_ID = 1536948511688630315

# 0 = sem cargo específico
# Admin / Manage Channels podem gerir as candidaturas
RECRUITER_ROLE_ID = 0

DATA_FILE = "recruitment_data.json"

PURPLE = discord.Color.from_rgb(123, 63, 242)


# =========================================================
# DATABASE
# =========================================================

def load_data():
    if not os.path.exists(DATA_FILE):
        return {}

    try:
        with open(DATA_FILE, "r", encoding="utf-8") as file:
            return json.load(file)

    except Exception as error:
        print(f"❌ Erro ao carregar {DATA_FILE}: {error}")
        return {}


def save_data(data):
    try:
        with open(DATA_FILE, "w", encoding="utf-8") as file:
            json.dump(
                data,
                file,
                indent=4,
                ensure_ascii=False
            )

    except Exception as error:
        print(f"❌ Erro ao guardar {DATA_FILE}: {error}")


APPLICATIONS = load_data()


def get_application(channel_id):
    return APPLICATIONS.get(str(channel_id))


def save_application(channel_id, application):
    APPLICATIONS[str(channel_id)] = application
    save_data(APPLICATIONS)


# =========================================================
# TRADUÇÕES
# =========================================================

LANGUAGES = {

    # =====================================================
    # PT-PT
    # =====================================================

    "pt": {

        "name": "Português (PT)",
        "emoji": "🇵🇹",
        "category_id": CATEGORY_PT_ID,

        # START
        "start_button": "Começar candidatura",
        "start_title": "🇵🇹 Candidatura — Português (PT)",
        "start_description": (
            "Bem-vindo ao processo de recrutamento.\n\n"
            "Clica em **Começar candidatura** para iniciar.\n\n"
            "Será criado um canal privado onde iremos recolher "
            "todas as tuas informações."
        ),

        "panel_sent": "✅ Painel de recrutamento enviado.",

        "created": "✅ A tua candidatura foi criada:",
        "server_only": "❌ Este botão só pode ser utilizado dentro do servidor.",
        "already_open": "❌ Já tens uma candidatura aberta em {channel}.",
        "category_missing": "❌ A categoria desta candidatura não foi encontrada.",
        "create_no_permission": "❌ Não tenho permissões para criar canais.",
        "create_error": "❌ Ocorreu um erro ao criar o canal.",

        # REGION
        "region_title": "🌍 Região",
        "region_description": "Seleciona a região onde estás localizado.",
        "region_placeholder": "Seleciona a tua região...",

        "regions": [
            ("🇪🇺", "Europa", "europe"),
            ("🌎", "América do Norte", "north_america"),
            ("🌎", "América do Sul", "south_america"),
            ("🌏", "Ásia", "asia"),
            ("🌍", "África", "africa"),
            ("🌐", "Outro", "other"),
        ],

        # LOCATION
        "location_title": "📍 Localização",
        "location_label": "Localização",
        "location_placeholder": "Ex: Portugal, Lisboa",

        # FOUND
        "found_title": "📢 Como nos encontraste?",
        "found_description": "Como encontraste esta oportunidade?",
        "found_instruction": "✍️ Clica no botão abaixo para responder.",
        "found_button": "Responder",
        "found_label": "Como nos encontraste?",
        "found_placeholder": "Ex: Discord, TikTok, Instagram...",

        # EXPERIENCE
        "experience_title": "💼 Experiência",
        "experience_description": "Conta-nos sobre a tua experiência relevante.",
        "experience_instruction": "✍️ Clica no botão abaixo para responder.",
        "experience_button": "Responder",
        "experience_label": "Experiência",
        "experience_placeholder": "Descreve a tua experiência...",

        # WORK
        "work_title": "🎓 Trabalho / Escola",
        "work_description": (
            "Estás atualmente a trabalhar ou a estudar?\n"
            "Qual é a tua disponibilidade?"
        ),
        "work_instruction": "✍️ Clica no botão abaixo para responder.",
        "work_button": "Responder",
        "work_label": "Trabalho / Escola",
        "work_placeholder": (
            "Descreve a tua situação atual e disponibilidade..."
        ),

        # ABOUT
        "about_title": "👤 Fala-nos sobre ti",
        "about_description": (
            "Conta-nos um pouco sobre ti, a tua personalidade "
            "e porque achas que serias uma boa escolha."
        ),
        "about_instruction": "✍️ Clica no botão abaixo para responder.",
        "about_button": "Responder",
        "about_label": "Sobre ti",
        "about_placeholder": "Escreve uma resposta detalhada...",

        # SHIFT
        "shift_title": "⏰ Preferência de horário",
        "shift_description": (
            "Seleciona o horário que funciona melhor para ti."
        ),

        "shift_08_16": "08:00 – 16:00",
        "shift_16_00": "16:00 – 00:00",
        "shift_00_08": "00:00 – 08:00",
        "shift_all": "Todos os horários",

        "shift_value_08_16": "08:00 – 16:00",
        "shift_value_16_00": "16:00 – 00:00",
        "shift_value_00_08": "00:00 – 08:00",
        "shift_value_all": "Todos os horários",

        # SUBMITTED
        "submitted_title": "✅ Candidatura submetida",
        "submitted_description": (
            "A tua candidatura foi enviada para a equipa "
            "de recrutamento.\n\n"
            "Aguarda enquanto analisamos a tua candidatura."
        ),

        # APPLICATION
        "application_title": "🇵🇹 CANDIDATURA",
        "field_candidate": "👤 Candidato",
        "field_discord": "🆔 Discord",
        "field_language": "🌐 Idioma",
        "field_region": "🌍 Região",
        "field_location": "📍 Localização",
        "field_found": "📢 Como nos encontrou?",
        "field_experience": "💼 Experiência",
        "field_work": "🎓 Trabalho / Escola",
        "field_about": "👤 Sobre",
        "field_shift": "⏰ Horário",
        "field_status": "📌 Estado",

        "status_pending": "🟡 Pendente",
        "status_accepted": "🟢 Aceite",

        # STAFF
        "approve_button": "APROVAR",
        "reject_button": "REJEITAR",

        "no_permission": "❌ Não tens permissão para fazer isto.",
        "application_not_found": "❌ Candidatura não encontrada.",

        "accepted_title": "🟢 CANDIDATURA ACEITE",
        "accepted_description": (
            "Candidatura aceite por {user}."
        ),

        "reject_notice": (
            "🗑️ Candidatura rejeitada. O canal será eliminado."
        ),

        # COMMON
        "not_your_application": (
            "❌ Esta candidatura não te pertence."
        ),
    },


    # =====================================================
    # PT-BR
    # =====================================================

    "br": {

        "name": "Português (BR)",
        "emoji": "🇧🇷",
        "category_id": CATEGORY_BR_ID,

        # START
        "start_button": "Começar candidatura",
        "start_title": "🇧🇷 Candidatura — Português (BR)",
        "start_description": (
            "Bem-vindo ao processo de recrutamento.\n\n"
            "Clique em **Começar candidatura** para iniciar.\n\n"
            "Será criado um canal privado onde vamos coletar "
            "todas as suas informações."
        ),

        "panel_sent": "✅ Painel de recrutamento enviado.",

        "created": "✅ Sua candidatura foi criada:",
        "server_only": "❌ Este botão só pode ser utilizado dentro do servidor.",
        "already_open": "❌ Você já possui uma candidatura aberta em {channel}.",
        "category_missing": "❌ A categoria desta candidatura não foi encontrada.",
        "create_no_permission": "❌ Não tenho permissão para criar canais.",
        "create_error": "❌ Ocorreu um erro ao criar o canal.",

        # REGION
        "region_title": "🌍 Região",
        "region_description": "Selecione a região onde você está localizado.",
        "region_placeholder": "Selecione sua região...",

        "regions": [
            ("🇪🇺", "Europa", "europe"),
            ("🌎", "América do Norte", "north_america"),
            ("🌎", "América do Sul", "south_america"),
            ("🌏", "Ásia", "asia"),
            ("🌍", "África", "africa"),
            ("🌐", "Outro", "other"),
        ],

        # LOCATION
        "location_title": "📍 Localização",
        "location_label": "Localização",
        "location_placeholder": "Ex: Brasil, São Paulo",

        # FOUND
        "found_title": "📢 Como nos encontrou?",
        "found_description": "Como você encontrou esta oportunidade?",
        "found_instruction": "✍️ Clique no botão abaixo para responder.",
        "found_button": "Responder",
        "found_label": "Como nos encontrou?",
        "found_placeholder": "Ex: Discord, TikTok, Instagram...",

        # EXPERIENCE
        "experience_title": "💼 Experiência",
        "experience_description": "Conte-nos sobre sua experiência relevante.",
        "experience_instruction": "✍️ Clique no botão abaixo para responder.",
        "experience_button": "Responder",
        "experience_label": "Experiência",
        "experience_placeholder": "Descreva sua experiência...",

        # WORK
        "work_title": "🎓 Trabalho / Estudos",
        "work_description": (
            "Você está trabalhando ou estudando atualmente?\n"
            "Qual é a sua disponibilidade?"
        ),
        "work_instruction": "✍️ Clique no botão abaixo para responder.",
        "work_button": "Responder",
        "work_label": "Trabalho / Estudos",
        "work_placeholder": (
            "Descreva sua situação atual e disponibilidade..."
        ),

        # ABOUT
        "about_title": "👤 Fale sobre você",
        "about_description": (
            "Conte um pouco sobre você, sua personalidade "
            "e por que você seria uma boa escolha."
        ),
        "about_instruction": "✍️ Clique no botão abaixo para responder.",
        "about_button": "Responder",
        "about_label": "Sobre você",
        "about_placeholder": "Escreva uma resposta detalhada...",

        # SHIFT
        "shift_title": "⏰ Preferência de horário",
        "shift_description": (
            "Selecione o horário que funciona melhor para você."
        ),

        "shift_08_16": "08:00 – 16:00",
        "shift_16_00": "16:00 – 00:00",
        "shift_00_08": "00:00 – 08:00",
        "shift_all": "Todos os horários",

        "shift_value_08_16": "08:00 – 16:00",
        "shift_value_16_00": "16:00 – 00:00",
        "shift_value_00_08": "00:00 – 08:00",
        "shift_value_all": "Todos os horários",

        # SUBMITTED
        "submitted_title": "✅ Candidatura enviada",
        "submitted_description": (
            "Sua candidatura foi enviada para nossa equipe "
            "de recrutamento.\n\n"
            "Aguarde enquanto analisamos sua candidatura."
        ),

        # APPLICATION
        "application_title": "🇧🇷 CANDIDATURA",
        "field_candidate": "👤 Candidato",
        "field_discord": "🆔 Discord",
        "field_language": "🌐 Idioma",
        "field_region": "🌍 Região",
        "field_location": "📍 Localização",
        "field_found": "📢 Como nos encontrou?",
        "field_experience": "💼 Experiência",
        "field_work": "🎓 Trabalho / Estudos",
        "field_about": "👤 Sobre",
        "field_shift": "⏰ Horário",
        "field_status": "📌 Status",

        "status_pending": "🟡 Pendente",
        "status_accepted": "🟢 Aceita",

        # STAFF
        "approve_button": "APROVAR",
        "reject_button": "REJEITAR",

        "no_permission": "❌ Você não tem permissão para fazer isso.",
        "application_not_found": "❌ Candidatura não encontrada.",

        "accepted_title": "🟢 CANDIDATURA ACEITA",
        "accepted_description": (
            "Candidatura aceita por {user}."
        ),

        "reject_notice": (
            "🗑️ Candidatura rejeitada. O canal será excluído."
        ),

        # COMMON
        "not_your_application": (
            "❌ Esta candidatura não pertence a você."
        ),
    },


    # =====================================================
    # ENGLISH
    # =====================================================

    "en": {

        "name": "English",
        "emoji": "🇬🇧",
        "category_id": CATEGORY_EN_ID,

        # START
        "start_button": "Start Application",
        "start_title": "🇬🇧 Application — English",
        "start_description": (
            "Welcome to the recruitment process.\n\n"
            "Click **Start Application** to begin.\n\n"
            "A private channel will be created where we will collect "
            "all of your information."
        ),

        "panel_sent": "✅ Recruitment panel sent.",

        "created": "✅ Your application has been created:",
        "server_only": "❌ This button can only be used inside the server.",
        "already_open": "❌ You already have an open application in {channel}.",
        "category_missing": "❌ The application category could not be found.",
        "create_no_permission": "❌ I don't have permission to create channels.",
        "create_error": "❌ An error occurred while creating the channel.",

        # REGION
        "region_title": "🌍 Region",
        "region_description": "Select the region where you are located.",
        "region_placeholder": "Select your region...",

        "regions": [
            ("🇪🇺", "Europe", "europe"),
            ("🌎", "North America", "north_america"),
            ("🌎", "South America", "south_america"),
            ("🌏", "Asia", "asia"),
            ("🌍", "Africa", "africa"),
            ("🌐", "Other", "other"),
        ],

        # LOCATION
        "location_title": "📍 Location",
        "location_label": "Location",
        "location_placeholder": "Ex: Portugal, Lisbon",

        # FOUND
        "found_title": "📢 How did you find us?",
        "found_description": "How did you find this opportunity?",
        "found_instruction": "✍️ Click the button below to answer.",
        "found_button": "Answer",
        "found_label": "How did you find us?",
        "found_placeholder": "Ex: Discord, TikTok, Instagram...",

        # EXPERIENCE
        "experience_title": "💼 Experience",
        "experience_description": "Tell us about your relevant experience.",
        "experience_instruction": "✍️ Click the button below to answer.",
        "experience_button": "Answer",
        "experience_label": "Experience",
        "experience_placeholder": "Describe your experience...",

        # WORK
        "work_title": "🎓 Work / School",
        "work_description": (
            "Are you currently working or studying?\n"
            "What is your availability?"
        ),
        "work_instruction": "✍️ Click the button below to answer.",
        "work_button": "Answer",
        "work_label": "Work / School",
        "work_placeholder": (
            "Describe your current situation and availability..."
        ),

        # ABOUT
        "about_title": "👤 Tell us about yourself",
        "about_description": (
            "Tell us about yourself, your personality "
            "and why you believe you would be a good fit."
        ),
        "about_instruction": "✍️ Click the button below to answer.",
        "about_button": "Answer",
        "about_label": "About you",
        "about_placeholder": "Write a detailed answer...",

        # SHIFT
        "shift_title": "⏰ Shift Preference",
        "shift_description": (
            "Select the schedule that works best for you."
        ),

        "shift_08_16": "08:00 – 16:00",
        "shift_16_00": "16:00 – 00:00",
        "shift_00_08": "00:00 – 08:00",
        "shift_all": "All Shifts",

        "shift_value_08_16": "08:00 – 16:00",
        "shift_value_16_00": "16:00 – 00:00",
        "shift_value_00_08": "00:00 – 08:00",
        "shift_value_all": "All Shifts",

        # SUBMITTED
        "submitted_title": "✅ Application submitted",
        "submitted_description": (
            "Your application has been submitted to our "
            "recruitment team.\n\n"
            "Please wait while we review your application."
        ),

        # APPLICATION
        "application_title": "🇬🇧 APPLICATION",
        "field_candidate": "👤 Candidate",
        "field_discord": "🆔 Discord",
        "field_language": "🌐 Language",
        "field_region": "🌍 Region",
        "field_location": "📍 Location",
        "field_found": "📢 How did they find us?",
        "field_experience": "💼 Experience",
        "field_work": "🎓 Work / School",
        "field_about": "👤 About",
        "field_shift": "⏰ Shift",
        "field_status": "📌 Status",

        "status_pending": "🟡 Pending",
        "status_accepted": "🟢 Accepted",

        # STAFF
        "approve_button": "APPROVE",
        "reject_button": "REJECT",

        "no_permission": "❌ You don't have permission to do this.",
        "application_not_found": "❌ Application not found.",

        "accepted_title": "🟢 APPLICATION ACCEPTED",
        "accepted_description": (
            "Application accepted by {user}."
        ),

        "reject_notice": (
            "🗑️ Application rejected. The channel will be deleted."
        ),

        # COMMON
        "not_your_application": (
            "❌ This application does not belong to you."
        ),
    }
}


# =========================================================
# UTILITÁRIOS
# =========================================================

def safe_channel_name(language_key, member):

    username = member.name.lower()

    username = re.sub(
        r"[^a-z0-9]+",
        "-",
        username
    )

    username = username.strip("-")

    if not username:
        username = "candidate"

    username = username[:30]

    return f"{language_key}-{username}-{str(member.id)[-4:]}"


def is_staff(interaction):

    member = interaction.user

    if not isinstance(member, discord.Member):
        return False

    if member.guild_permissions.administrator:
        return True

    if member.guild_permissions.manage_channels:
        return True

    if RECRUITER_ROLE_ID:

        if any(
            role.id == RECRUITER_ROLE_ID
            for role in member.roles
        ):
            return True

    return False


async def get_category(guild, category_id):

    channel = guild.get_channel(category_id)

    if isinstance(
        channel,
        discord.CategoryChannel
    ):
        return channel

    return None


async def verify_candidate(
    interaction,
    application
):

    if not application:

        await interaction.response.send_message(
            "❌ Application not found.",
            ephemeral=True
        )

        return False

    if application["user_id"] != interaction.user.id:

        language = LANGUAGES.get(
            application.get("language"),
            LANGUAGES["en"]
        )

        await interaction.response.send_message(
            language["not_your_application"],
            ephemeral=True
        )

        return False

    return True


# =========================================================
# STEP EMBEDS
# =========================================================

def step_embed(
    language_key,
    title,
    description,
    instruction=None
):

    language = LANGUAGES[language_key]

    text = description

    if instruction:
        text += f"\n\n{instruction}"

    return discord.Embed(
        title=title,
        description=text,
        color=PURPLE
    )


# =========================================================
# START APPLICATION
# =========================================================

class StartApplicationView(discord.ui.View):

    def __init__(self, language_key):

        super().__init__(timeout=None)

        self.language_key = language_key

        language = LANGUAGES[
            language_key
        ]

        button = discord.ui.Button(
            label=language["start_button"],
            emoji="📝",
            style=discord.ButtonStyle.primary,
            custom_id=f"recruitment_start_{language_key}"
        )

        button.callback = self.start_application

        self.add_item(button)

    async def start_application(
        self,
        interaction
    ):

        language_key = self.language_key
        language = LANGUAGES[
            language_key
        ]

        guild = interaction.guild

        if guild is None:

            await interaction.response.send_message(
                language["server_only"],
                ephemeral=True
            )

            return

        # Verificar candidatura aberta
        for application in APPLICATIONS.values():

            if (
                application.get("user_id")
                == interaction.user.id
                and application.get("status")
                in ("pending",)
            ):

                existing_channel = guild.get_channel(
                    int(
                        application.get(
                            "channel_id",
                            0
                        )
                    )
                )

                if existing_channel:

                    await interaction.response.send_message(
                        language["already_open"].format(
                            channel=existing_channel.mention
                        ),
                        ephemeral=True
                    )

                    return

        category = await get_category(
            guild,
            language["category_id"]
        )

        if category is None:

            await interaction.response.send_message(
                language["category_missing"],
                ephemeral=True
            )

            return

        # =================================================
        # PERMISSÕES
        # =================================================

        overwrites = {

            guild.default_role:
                discord.PermissionOverwrite(
                    view_channel=False
                ),

            interaction.user:
                discord.PermissionOverwrite(
                    view_channel=True,
                    send_messages=True,
                    read_message_history=True,
                    attach_files=True
                ),

            guild.me:
                discord.PermissionOverwrite(
                    view_channel=True,
                    send_messages=True,
                    read_message_history=True,
                    manage_channels=True,
                    manage_messages=True
                )
        }

        if RECRUITER_ROLE_ID:

            recruiter_role = guild.get_role(
                RECRUITER_ROLE_ID
            )

            if recruiter_role:

                overwrites[
                    recruiter_role
                ] = discord.PermissionOverwrite(
                    view_channel=True,
                    send_messages=True,
                    read_message_history=True
                )

        channel_name = safe_channel_name(
            language_key,
            interaction.user
        )

        # =================================================
        # CRIAR CANAL
        # =================================================

        try:

            channel = await guild.create_text_channel(
                name=channel_name,
                category=category,
                overwrites=overwrites,
                reason=(
                    "Recruitment application - "
                    f"{interaction.user}"
                )
            )

        except discord.Forbidden:

            await interaction.response.send_message(
                language["create_no_permission"],
                ephemeral=True
            )

            return

        except discord.HTTPException as error:

            print(
                f"❌ Error creating recruitment channel: {error}"
            )

            await interaction.response.send_message(
                language["create_error"],
                ephemeral=True
            )

            return

        # =================================================
        # GUARDAR
        # =================================================

        application = {

            "channel_id": channel.id,

            "user_id": interaction.user.id,

            "username": str(
                interaction.user
            ),

            "language": language_key,

            "language_name": language["name"],

            "status": "pending",

            "created_at":
                datetime.now(
                    timezone.utc
                ).isoformat(),

            "region": "",
            "location": "",
            "how_found_us": "",
            "experience": "",
            "work_school": "",
            "about": "",
            "shift": ""
        }

        save_application(
            channel.id,
            application
        )

        # =================================================
        # CONFIRMAÇÃO EPHEMERAL
        # =================================================

        await interaction.response.send_message(
            f"{language['created']} {channel.mention}",
            ephemeral=True
        )

        # =================================================
        # PRIMEIRO PASSO
        # =================================================

        embed = step_embed(
            language_key,
            language["region_title"],
            language["region_description"]
        )

        await channel.send(
            content=interaction.user.mention,
            embed=embed,
            view=RegionView(
                channel.id,
                language_key
            )
        )


# =========================================================
# REGION
# =========================================================

class RegionView(discord.ui.View):

    def __init__(
        self,
        channel_id,
        language_key
    ):

        super().__init__(
            timeout=None
        )

        self.channel_id = channel_id
        self.language_key = language_key

        language = LANGUAGES[
            language_key
        ]

        options = []

        for emoji, label, value in language["regions"]:

            options.append(
                discord.SelectOption(
                    label=label,
                    value=value,
                    emoji=emoji
                )
            )

        select = discord.ui.Select(
            placeholder=language[
                "region_placeholder"
            ],
            min_values=1,
            max_values=1,
            custom_id=(
                f"recruitment_region_"
                f"{language_key}_"
                f"{channel_id}"
            ),
            options=options
        )

        select.callback = self.region_selected

        self.add_item(select)

    async def region_selected(
        self,
        interaction
    ):

        application = get_application(
            self.channel_id
        )

        if not await verify_candidate(
            interaction,
            application
        ):
            return

        value = interaction.data[
            "values"
        ][0]

        region_labels = {
            "europe": {
                "pt": "Europa",
                "br": "Europa",
                "en": "Europe"
            },
            "north_america": {
                "pt": "América do Norte",
                "br": "América do Norte",
                "en": "North America"
            },
            "south_america": {
                "pt": "América do Sul",
                "br": "América do Sul",
                "en": "South America"
            },
            "asia": {
                "pt": "Ásia",
                "br": "Ásia",
                "en": "Asia"
            },
            "africa": {
                "pt": "África",
                "br": "África",
                "en": "Africa"
            },
            "other": {
                "pt": "Outro",
                "br": "Outro",
                "en": "Other"
            }
        }

        application[
            "region"
        ] = region_labels[
            value
        ][
            application["language"]
        ]

        save_application(
            self.channel_id,
            application
        )

        language = LANGUAGES[
            application["language"]
        ]

        await interaction.response.send_modal(
            LocationModal(
                self.channel_id,
                language
            )
        )


# =========================================================
# LOCATION
# =========================================================

class LocationModal(discord.ui.Modal):

    def __init__(
        self,
        channel_id,
        language
    ):

        super().__init__(
            title=language[
                "location_title"
            ]
        )

        self.channel_id = channel_id

        self.answer = discord.ui.TextInput(
            label=language[
                "location_label"
            ],
            placeholder=language[
                "location_placeholder"
            ],
            required=True,
            max_length=150
        )

        self.add_item(
            self.answer
        )

    async def on_submit(
        self,
        interaction
    ):

        application = get_application(
            self.channel_id
        )

        if not await verify_candidate(
            interaction,
            application
        ):
            return

        application[
            "location"
        ] = self.answer.value

        save_application(
            self.channel_id,
            application
        )

        language = LANGUAGES[
            application["language"]
        ]

        embed = step_embed(
            application["language"],
            language["found_title"],
            language["found_description"],
            language["found_instruction"]
        )

        await interaction.response.send_message(
            embed=embed,
            view=FoundUsView(
                self.channel_id,
                application["language"]
            )
        )


# =========================================================
# FOUND VIEW
# =========================================================

class FoundUsView(discord.ui.View):

    def __init__(
        self,
        channel_id,
        language_key
    ):

        super().__init__(
            timeout=None
        )

        self.channel_id = channel_id
        self.language_key = language_key

        language = LANGUAGES[
            language_key
        ]

        button = discord.ui.Button(
            label=language[
                "found_button"
            ],
            emoji="✍️",
            style=discord.ButtonStyle.primary,
            custom_id=(
                f"recruitment_found_"
                f"{channel_id}"
            )
        )

        button.callback = self.open_modal

        self.add_item(button)

    async def open_modal(
        self,
        interaction
    ):

        application = get_application(
            self.channel_id
        )

        if not await verify_candidate(
            interaction,
            application
        ):
            return

        language = LANGUAGES[
            application["language"]
        ]

        await interaction.response.send_modal(
            FoundModal(
                self.channel_id,
                language
            )
        )


# =========================================================
# FOUND MODAL
# =========================================================

class FoundModal(discord.ui.Modal):

    def __init__(
        self,
        channel_id,
        language
    ):

        super().__init__(
            title=language[
                "found_title"
            ]
        )

        self.channel_id = channel_id

        self.answer = discord.ui.TextInput(
            label=language[
                "found_label"
            ],
            placeholder=language[
                "found_placeholder"
            ],
            required=True,
            max_length=300
        )

        self.add_item(
            self.answer
        )

    async def on_submit(
        self,
        interaction
    ):

        application = get_application(
            self.channel_id
        )

        if not await verify_candidate(
            interaction,
            application
        ):
            return

        application[
            "how_found_us"
        ] = self.answer.value

        save_application(
            self.channel_id,
            application
        )

        language = LANGUAGES[
            application["language"]
        ]

        embed = step_embed(
            application["language"],
            language["experience_title"],
            language["experience_description"],
            language["experience_instruction"]
        )

        await interaction.response.send_message(
            embed=embed,
            view=ExperienceView(
                self.channel_id,
                application["language"]
            )
        )


# =========================================================
# EXPERIENCE VIEW
# =========================================================

class ExperienceView(discord.ui.View):

    def __init__(
        self,
        channel_id,
        language_key
    ):

        super().__init__(
            timeout=None
        )

        self.channel_id = channel_id
        self.language_key = language_key

        language = LANGUAGES[
            language_key
        ]

        button = discord.ui.Button(
            label=language[
                "experience_button"
            ],
            emoji="✍️",
            style=discord.ButtonStyle.primary,
            custom_id=(
                f"recruitment_experience_"
                f"{channel_id}"
            )
        )

        button.callback = self.open_modal

        self.add_item(
            button
        )

    async def open_modal(
        self,
        interaction
    ):

        application = get_application(
            self.channel_id
        )

        if not await verify_candidate(
            interaction,
            application
        ):
            return

        language = LANGUAGES[
            application["language"]
        ]

        await interaction.response.send_modal(
            ExperienceModal(
                self.channel_id,
                language
            )
        )


# =========================================================
# EXPERIENCE MODAL
# =========================================================

class ExperienceModal(discord.ui.Modal):

    def __init__(
        self,
        channel_id,
        language
    ):

        super().__init__(
            title=language[
                "experience_title"
            ]
        )

        self.channel_id = channel_id

        self.answer = discord.ui.TextInput(
            label=language[
                "experience_label"
            ],
            placeholder=language[
                "experience_placeholder"
            ],
            style=discord.TextStyle.paragraph,
            required=True,
            max_length=1500
        )

        self.add_item(
            self.answer
        )

    async def on_submit(
        self,
        interaction
    ):

        application = get_application(
            self.channel_id
        )

        if not await verify_candidate(
            interaction,
            application
        ):
            return

        application[
            "experience"
        ] = self.answer.value

        save_application(
            self.channel_id,
            application
        )

        language = LANGUAGES[
            application["language"]
        ]

        embed = step_embed(
            application["language"],
            language["work_title"],
            language["work_description"],
            language["work_instruction"]
        )

        await interaction.response.send_message(
            embed=embed,
            view=WorkSchoolView(
                self.channel_id,
                application["language"]
            )
        )


# =========================================================
# WORK / SCHOOL VIEW
# =========================================================

class WorkSchoolView(discord.ui.View):

    def __init__(
        self,
        channel_id,
        language_key
    ):

        super().__init__(
            timeout=None
        )

        self.channel_id = channel_id
        self.language_key = language_key

        language = LANGUAGES[
            language_key
        ]

        button = discord.ui.Button(
            label=language[
                "work_button"
            ],
            emoji="✍️",
            style=discord.ButtonStyle.primary,
            custom_id=(
                f"recruitment_work_"
                f"{channel_id}"
            )
        )

        button.callback = self.open_modal

        self.add_item(
            button
        )

    async def open_modal(
        self,
        interaction
    ):

        application = get_application(
            self.channel_id
        )

        if not await verify_candidate(
            interaction,
            application
        ):
            return

        language = LANGUAGES[
            application["language"]
        ]

        await interaction.response.send_modal(
            WorkSchoolModal(
                self.channel_id,
                language
            )
        )


# =========================================================
# WORK / SCHOOL MODAL
# =========================================================

class WorkSchoolModal(discord.ui.Modal):

    def __init__(
        self,
        channel_id,
        language
    ):

        super().__init__(
            title=language[
                "work_title"
            ]
        )

        self.channel_id = channel_id

        self.answer = discord.ui.TextInput(
            label=language[
                "work_label"
            ],
            placeholder=language[
                "work_placeholder"
            ],
            style=discord.TextStyle.paragraph,
            required=True,
            max_length=1000
        )

        self.add_item(
            self.answer
        )

    async def on_submit(
        self,
        interaction
    ):

        application = get_application(
            self.channel_id
        )

        if not await verify_candidate(
            interaction,
            application
        ):
            return

        application[
            "work_school"
        ] = self.answer.value

        save_application(
            self.channel_id,
            application
        )

        language = LANGUAGES[
            application["language"]
        ]

        embed = step_embed(
            application["language"],
            language["about_title"],
            language["about_description"],
            language["about_instruction"]
        )

        await interaction.response.send_message(
            embed=embed,
            view=AboutView(
                self.channel_id,
                application["language"]
            )
        )


# =========================================================
# ABOUT VIEW
# =========================================================

class AboutView(discord.ui.View):

    def __init__(
        self,
        channel_id,
        language_key
    ):

        super().__init__(
            timeout=None
        )

        self.channel_id = channel_id
        self.language_key = language_key

        language = LANGUAGES[
            language_key
        ]

        button = discord.ui.Button(
            label=language[
                "about_button"
            ],
            emoji="✍️",
            style=discord.ButtonStyle.primary,
            custom_id=(
                f"recruitment_about_"
                f"{channel_id}"
            )
        )

        button.callback = self.open_modal

        self.add_item(
            button
        )

    async def open_modal(
        self,
        interaction
    ):

        application = get_application(
            self.channel_id
        )

        if not await verify_candidate(
            interaction,
            application
        ):
            return

        language = LANGUAGES[
            application["language"]
        ]

        await interaction.response.send_modal(
            AboutModal(
                self.channel_id,
                language
            )
        )


# =========================================================
# ABOUT MODAL
# =========================================================

class AboutModal(discord.ui.Modal):

    def __init__(
        self,
        channel_id,
        language
    ):

        super().__init__(
            title=language[
                "about_title"
            ]
        )

        self.channel_id = channel_id

        self.answer = discord.ui.TextInput(
            label=language[
                "about_label"
            ],
            placeholder=language[
                "about_placeholder"
            ],
            style=discord.TextStyle.paragraph,
            required=True,
            max_length=2000
        )

        self.add_item(
            self.answer
        )

    async def on_submit(
        self,
        interaction
    ):

        application = get_application(
            self.channel_id
        )

        if not await verify_candidate(
            interaction,
            application
        ):
            return

        application[
            "about"
        ] = self.answer.value

        save_application(
            self.channel_id,
            application
        )

        language = LANGUAGES[
            application["language"]
        ]

        embed = step_embed(
            application["language"],
            language["shift_title"],
            language["shift_description"]
        )

        await interaction.response.send_message(
            embed=embed,
            view=ShiftView(
                self.channel_id,
                application["language"]
            )
        )


# =========================================================
# SHIFT VIEW
# =========================================================

class ShiftView(discord.ui.View):

    def __init__(
        self,
        channel_id,
        language_key
    ):

        super().__init__(
            timeout=None
        )

        self.channel_id = channel_id
        self.language_key = language_key

        language = LANGUAGES[
            language_key
        ]

        # 08-16
        self.add_item(
            self.make_shift_button(
                label=language["shift_08_16"],
                value=language["shift_value_08_16"],
                emoji="☀️",
                custom_id=f"shift_08_16_{channel_id}"
            )
        )

        # 16-00
        self.add_item(
            self.make_shift_button(
                label=language["shift_16_00"],
                value=language["shift_value_16_00"],
                emoji="🌇",
                custom_id=f"shift_16_00_{channel_id}"
            )
        )

        # 00-08
        self.add_item(
            self.make_shift_button(
                label=language["shift_00_08"],
                value=language["shift_value_00_08"],
                emoji="🌙",
                custom_id=f"shift_00_08_{channel_id}"
            )
        )

        # ALL
        self.add_item(
            self.make_shift_button(
                label=language["shift_all"],
                value=language["shift_value_all"],
                emoji="🔄",
                custom_id=f"shift_all_{channel_id}",
                primary=True
            )
        )

    def make_shift_button(
        self,
        label,
        value,
        emoji,
        custom_id,
        primary=False
    ):

        button = discord.ui.Button(
            label=label,
            emoji=emoji,
            style=(
                discord.ButtonStyle.primary
                if primary
                else discord.ButtonStyle.secondary
            ),
            custom_id=custom_id
        )

        async def callback(interaction):

            await self.submit_shift(
                interaction,
                value
            )

        button.callback = callback

        return button

    async def submit_shift(
        self,
        interaction,
        shift_name
    ):

        application = get_application(
            self.channel_id
        )

        if not await verify_candidate(
            interaction,
            application
        ):
            return

        application[
            "shift"
        ] = shift_name

        application[
            "status"
        ] = "pending"

        application[
            "submitted_at"
        ] = datetime.now(
            timezone.utc
        ).isoformat()

        save_application(
            self.channel_id,
            application
        )

        guild = interaction.guild

        embed = build_application_embed(
            application,
            guild
        )

        await interaction.response.edit_message(
            content=None,
            embed=embed,
            view=RecruitmentActionView(
                self.channel_id,
                application["language"]
            )
        )

        language = LANGUAGES[
            application["language"]
        ]

        await interaction.channel.send(
            embed=discord.Embed(
                title=language[
                    "submitted_title"
                ],
                description=language[
                    "submitted_description"
                ],
                color=PURPLE
            )
        )


# =========================================================
# APPLICATION EMBED
# =========================================================

def build_application_embed(
    application,
    guild
):

    language = LANGUAGES[
        application["language"]
    ]

    embed = discord.Embed(
        title=language[
            "application_title"
        ],
        color=PURPLE
    )

    member = None

    if guild:

        member = guild.get_member(
            application["user_id"]
        )

    username = (
        member.mention
        if member
        else application["username"]
    )

    embed.add_field(
        name=language["field_candidate"],
        value=username,
        inline=False
    )

    embed.add_field(
        name=language["field_discord"],
        value=application["username"],
        inline=True
    )

    embed.add_field(
        name=language["field_language"],
        value=language["name"],
        inline=True
    )

    embed.add_field(
        name=language["field_region"],
        value=application["region"] or "—",
        inline=True
    )

    embed.add_field(
        name=language["field_location"],
        value=application["location"] or "—",
        inline=False
    )

    embed.add_field(
        name=language["field_found"],
        value=application["how_found_us"] or "—",
        inline=False
    )

    embed.add_field(
        name=language["field_experience"],
        value=application["experience"] or "—",
        inline=False
    )

    embed.add_field(
        name=language["field_work"],
        value=application["work_school"] or "—",
        inline=False
    )

    embed.add_field(
        name=language["field_about"],
        value=application["about"] or "—",
        inline=False
    )

    embed.add_field(
        name=language["field_shift"],
        value=application["shift"] or "—",
        inline=False
    )

    if application["status"] == "accepted":

        status = language[
            "status_accepted"
        ]

    else:

        status = language[
            "status_pending"
        ]

    embed.add_field(
        name=language["field_status"],
        value=status,
        inline=False
    )

    embed.set_footer(
        text="Hustler Recruitment"
    )

    return embed


# =========================================================
# STAFF ACTIONS
# =========================================================

class RecruitmentActionView(
    discord.ui.View
):

    def __init__(
        self,
        channel_id,
        language_key
    ):

        super().__init__(
            timeout=None
        )

        self.channel_id = channel_id
        self.language_key = language_key

        language = LANGUAGES[
            language_key
        ]

        # APPROVE
        approve_button = discord.ui.Button(
            label=language[
                "approve_button"
            ],
            emoji="✅",
            style=discord.ButtonStyle.success,
            custom_id=(
                f"recruitment_approve_"
                f"{channel_id}"
            )
        )

        approve_button.callback = (
            self.approve
        )

        self.add_item(
            approve_button
        )

        # REJECT
        reject_button = discord.ui.Button(
            label=language[
                "reject_button"
            ],
            emoji="❌",
            style=discord.ButtonStyle.danger,
            custom_id=(
                f"recruitment_reject_"
                f"{channel_id}"
            )
        )

        reject_button.callback = (
            self.reject
        )

        self.add_item(
            reject_button
        )

    # =====================================================
    # APPROVE
    # =====================================================

    async def approve(
        self,
        interaction
    ):

        if not is_staff(
            interaction
        ):

            language = LANGUAGES[
                self.language_key
            ]

            await interaction.response.send_message(
                language["no_permission"],
                ephemeral=True
            )

            return

        application = get_application(
            self.channel_id
        )

        if not application:

            language = LANGUAGES[
                self.language_key
            ]

            await interaction.response.send_message(
                language[
                    "application_not_found"
                ],
                ephemeral=True
            )

            return

        guild = interaction.guild

        accepted_category = await get_category(
            guild,
            CATEGORY_ACCEPTED_ID
        )

        if accepted_category is None:

            language = LANGUAGES[
                self.language_key
            ]

            await interaction.response.send_message(
                language[
                    "category_missing"
                ],
                ephemeral=True
            )

            return

        application[
            "status"
        ] = "accepted"

        application[
            "approved_by"
        ] = interaction.user.id

        application[
            "approved_at"
        ] = datetime.now(
            timezone.utc
        ).isoformat()

        save_application(
            self.channel_id,
            application
        )

        channel = interaction.channel

        if not isinstance(
            channel,
            discord.TextChannel
        ):
            return

        try:

            await channel.edit(
                category=accepted_category,
                reason=(
                    "Application accepted by "
                    f"{interaction.user}"
                )
            )

        except discord.Forbidden:

            language = LANGUAGES[
                self.language_key
            ]

            await interaction.response.send_message(
                language[
                    "create_no_permission"
                ],
                ephemeral=True
            )

            return

        language = LANGUAGES[
            application["language"]
        ]

        embed = build_application_embed(
            application,
            guild
        )

        await interaction.response.edit_message(
            embed=embed,
            view=None
        )

        await channel.send(
            embed=discord.Embed(
                title=language[
                    "accepted_title"
                ],
                description=language[
                    "accepted_description"
                ].format(
                    user=interaction.user.mention
                ),
                color=discord.Color.green()
            )
        )

    # =====================================================
    # REJECT
    # =====================================================

    async def reject(
        self,
        interaction
    ):

        if not is_staff(
            interaction
        ):

            language = LANGUAGES[
                self.language_key
            ]

            await interaction.response.send_message(
                language["no_permission"],
                ephemeral=True
            )

            return

        application = get_application(
            self.channel_id
        )

        if not application:

            language = LANGUAGES[
                self.language_key
            ]

            await interaction.response.send_message(
                language[
                    "application_not_found"
                ],
                ephemeral=True
            )

            return

        language = LANGUAGES[
            application["language"]
        ]

        # Remover da base
        APPLICATIONS.pop(
            str(self.channel_id),
            None
        )

        save_data(
            APPLICATIONS
        )

        await interaction.response.send_message(
            language[
                "reject_notice"
            ],
            ephemeral=True
        )

        channel = interaction.channel

        if channel:

            try:

                await channel.delete(
                    reason=(
                        "Application rejected by "
                        f"{interaction.user}"
                    )
                )

            except discord.Forbidden:

                print(
                    f"❌ Não tenho permissão para apagar "
                    f"o canal {channel.id}"
                )


# =========================================================
# COG
# =========================================================

class Recruitment(commands.Cog):

    def __init__(
        self,
        bot
    ):

        self.bot = bot

    async def send_test_panel(
        self,
        interaction,
        language_key
    ):

        language = LANGUAGES[
            language_key
        ]

        embed = discord.Embed(
            title=language[
                "start_title"
            ],
            description=language[
                "start_description"
            ],
            color=PURPLE
        )

        embed.set_footer(
            text="Hustler Recruitment"
        )

        await interaction.channel.send(
            embed=embed,
            view=StartApplicationView(
                language_key
            )
        )

        await interaction.response.send_message(
            language[
                "panel_sent"
            ],
            ephemeral=True
        )

    # =====================================================
    # PT-PT
    # =====================================================

    @app_commands.command(
        name="testept",
        description=(
            "Enviar o teste de recrutamento PT-PT"
        )
    )
    async def testept(
        self,
        interaction
    ):

        await self.send_test_panel(
            interaction,
            "pt"
        )

    # =====================================================
    # PT-BR
    # =====================================================

    @app_commands.command(
        name="testebr",
        description=(
            "Enviar o teste de recrutamento PT-BR"
        )
    )
    async def testebr(
        self,
        interaction
    ):

        await self.send_test_panel(
            interaction,
            "br"
        )

    # =====================================================
    # ENGLISH
    # =====================================================

    @app_commands.command(
        name="testeeng",
        description=(
            "Send the English recruitment test"
        )
    )
    async def testeeng(
        self,
        interaction
    ):

        await self.send_test_panel(
            interaction,
            "en"
        )


# =========================================================
# SETUP
# =========================================================

async def setup(bot):

    await bot.add_cog(
        Recruitment(bot)
    )

    # Painéis iniciais persistentes
    bot.add_view(
        StartApplicationView("pt")
    )

    bot.add_view(
        StartApplicationView("br")
    )

    bot.add_view(
        StartApplicationView("en")
    )