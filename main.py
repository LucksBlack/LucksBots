import discord
from discord.ext import commands
import os

intents = discord.Intents.all()
bot = commands.Bot(command_prefix="+", intents=intents)

@bot.event
async def on_ready():
    print(f"✅ LuckBot está online como {bot.user}.")

@bot.event
async def on_member_join(member):
    canal = discord.utils.get(member.guild.text_channels, name="geral")
    if canal:
        embed = discord.Embed(
            title="👋 Bem-vindo ao servidor!",
            description=f"{member.mention}, estamos felizes em te receber aqui!",
            color=discord.Color.green()
        )
        embed.add_field(name="📜 Regras", value="1. Seja respeitoso\n2. Sem spam\n3. Use os canais corretamente", inline=False)
        await canal.send(embed=embed)

    cargo = discord.utils.get(member.guild.roles, name="Membro")
    if cargo:
        await member.add_roles(cargo)

@bot.command()
@commands.has_permissions(manage_roles=True)
async def cargo(ctx, membro: discord.Member, *, nome_do_cargo):
    cargo = discord.utils.get(ctx.guild.roles, name=nome_do_cargo)
    if cargo is None:
        await ctx.send("❌ Cargo não encontrado.")
        return
    try:
        await membro.add_roles(cargo)
        await ctx.send(f"✅ Cargo **{nome_do_cargo}** adicionado a {membro.mention}.")
    except Exception as e:
        await ctx.send(f"⚠️ Erro ao adicionar cargo: {e}")

@bot.command()
@commands.has_permissions(manage_roles=True)
async def removercargo(ctx, membro: discord.Member, *, nome_do_cargo):
    cargo = discord.utils.get(ctx.guild.roles, name=nome_do_cargo)
    if cargo is None:
        await ctx.send("❌ Cargo não encontrado.")
        return
    try:
        await membro.remove_roles(cargo)
        await ctx.send(f"✅ Cargo **{nome_do_cargo}** removido de {membro.mention}.")
    except Exception as e:
        await ctx.send(f"⚠️ Erro ao remover cargo: {e}")

import base64

@bot.command()
async def encrypt(ctx, *, texto: str):
    try:
        texto_bytes = texto.encode('utf-8')
        criptografado = base64.b64encode(texto_bytes).decode('utf-8')

        with open("mensagem_criptografada.txt", "w") as f:
            f.write(criptografado)

        await ctx.send(file=discord.File("mensagem_criptografada.txt"))
        os.remove("mensagem_criptografada.txt")
    except Exception as e:
        await ctx.send(f"❌ Ocorreu um erro: {e}")
        
# Rodar o bot com token da variável de ambiente
bot.run(os.getenv("TOKEN"))
