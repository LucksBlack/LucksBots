import os
import discord
from discord.ext import commands

TOKEN = os.getenv("TOKEN")  # Pegando o token da variável de ambiente

intents = discord.Intents.default()
intents.members = True
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"{bot.user.name} está online!")

@bot.event
async def on_member_join(member):
    guild = member.guild
    canal = discord.utils.get(guild.text_channels, name="geral")
    cargo = discord.utils.get(guild.roles, name="Membro")

    if cargo:
        await member.add_roles(cargo)

    if canal:
        embed = discord.Embed(
            title="👋 Boas-vindas!",
            description=f"{member.mention}, seja bem-vindo(a) ao servidor **{guild.name}**!",
            color=0x00ff00
        )
        embed.add_field(
            name="📜 Regras",
            value="1. Seja respeitoso\n2. Nada de spam\n3. Use os canais corretamente",
            inline=False
        )
        embed.set_footer(text="Divirta-se!")
        await canal.send(embed=embed)

bot.run(TOKEN)