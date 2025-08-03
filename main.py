import discord
from discord.ext import commands

intents = discord.Intents.default()
intents.members = True
intents.message_content = True
bot = commands.Bot(command_prefix="+", intents=intents)

# Evento de boas-vindas
@bot.event
async def on_member_join(member):
    canal = discord.utils.get(member.guild.text_channels, name="geral")  # Altere se necessário
    cargo = discord.utils.get(member.guild.roles, name="Membro")

    if cargo:
        await member.add_roles(cargo)

    if canal:
        embed = discord.Embed(
            title="👋 Boas-vindas!",
            description=f"Olá {member.mention}, bem-vindo(a) ao servidor!",
            color=discord.Color.green()
        )
        embed.add_field(
            name="📜 Regras",
            value="1. Respeite todos\n2. Sem spam\n3. Use os canais corretamente",
            inline=False
        )
        embed.set_footer(text="Aproveite sua estadia!")
        await canal.send(embed=embed)

# Comando para adicionar cargo
@bot.command()
@commands.has_permissions(manage_roles=True)
async def cargo(ctx, membro: discord.Member, cargo_nome: str):
    cargo_nome = cargo_nome.lower()

    cargos_validos = {
        "staff": "Staff",
        "adm": "ADM"
    }

    if cargo_nome not in cargos_validos:
        await ctx.send("❌ Cargo inválido. Use apenas `Staff` ou `ADM`.")
        return

    cargo = discord.utils.get(ctx.guild.roles, name=cargos_validos[cargo_nome])
    if not cargo:
        await ctx.send(f"❌ O cargo `{cargos_validos[cargo_nome]}` não existe.")
        return

    await membro.add_roles(cargo)
    await ctx.send(f"✅ Cargo `{cargos_validos[cargo_nome]}` adicionado ao {membro.mention} com sucesso!")

# Tratamento de erro de permissão
@cargo.error
async def cargo_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("🚫 Você não tem permissão para usar este comando.")
    elif isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("❗ Use o comando assim: `+cargo @usuário Staff`")
    else:
        await ctx.send("⚠️ Ocorreu um erro.")

# Token (use variável de ambiente no Railway)
import os
TOKEN = os.getenv("TOKEN")

bot.run(TOKEN)
