import discord
from discord.ext import commands
import os
import asyncio

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
 @bot.event
async def on_member_remove(member):
    canal = discord.utils.get(member.guild.text_channels, name='geral')
    if canal:
        await canal.send(
            f"😢 O usuário **{member.name}** saiu do servidor.\n"
            "Esperamos que volte algum dia!"
        )
        
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

 @bot.command()
@commands.has_permissions(manage_roles=True)
async def mute(ctx, member: discord.Member, dias: int):
    mute_role = discord.utils.get(ctx.guild.roles, name="Mutado")

    if not mute_role:
        mute_role = await ctx.guild.create_role(name="Mutado")
        for channel in ctx.guild.channels:
            await channel.set_permissions(mute_role, send_messages=False, speak=False)

    await member.add_roles(mute_role)
    await ctx.send(f"🔇 {member.mention} foi mutado por {dias} dia(s).")

    await asyncio.sleep(dias * 86400)
    await member.remove_roles(mute_role)
    await ctx.send(f"🔈 {member.mention} foi desmutado automaticamente após {dias} dia(s).")

 @bot.command()
@commands.has_permissions(manage_roles=True)
async def unmute(ctx, member: discord.Member):
    mute_role = discord.utils.get(ctx.guild.roles, name="Mutado")
    if mute_role and mute_role in member.roles:
        await member.remove_roles(mute_role)
        await ctx.send(f"🔈 {member.mention} foi desmutado com sucesso.")
    else:
        await ctx.send("⚠️ Esse usuário não está mutado.")

 @bot.command()
async def ajuda(ctx):
    embed = discord.Embed(
        title="🧠 LuckBot - Lista de Comandos",
        description="Aqui estão os comandos disponíveis:",
        color=discord.Color.blue()
    )
    embed.add_field(name="🧍‍♂️ +cargo @usuário Cargo", value="Adiciona o cargo `Staff` ou `ADM` ao usuário mencionado. Requer permissão.", inline=False)
    embed.add_field(name="🧍‍♂️ remove cargo @usuário Cargo", value="Remove o cargo do usuário mencionado. Requer permissão.", inline=False)
    embed.add_field(name="🔇 +mute @usuário dias", value="Silencia o usuário por uma quantidade de dias. Requer permissão.", inline=False)
    embed.add_field(name="🔊 +unmute @usuário", value="Remove o mute do usuário. Requer permissão.", inline=False)
    embed.add_field(name="🔐 +encrypt mensagem", value="Criptografa a mensagem e envia como arquivo.", inline=False)
    embed.add_field(name="📩 +ajuda", value="Exibe esta lista de comandos.", inline=False)

    await ctx.send(embed=embed)

 @bot.command()
async def sobre(ctx):
    embed = discord.Embed(
        title="🤖 Sobre o LuckBot",
        description=(
            "O **LuckBot** foi criado com o objetivo de trazer comandos criativos, úteis e "
            "engraçados para servidores do Discord. Ele nasceu de um projeto pessoal para testar ideias "
            "inovadoras, e foi evoluindo com o tempo até se tornar um bot com várias funções administrativas, "
            "de entretenimento e criptografia.\n\n"
            "Feito com ❤️ por quem ama tecnologia e quer transformar servidores em experiências mais vivas e únicas."
        ),
        color=discord.Color.green()
    )
    embed.set_footer(text="Obrigado por usar o LuckBot!")
    await ctx.send(embed=embed)
    
# Rodar o bot com token da variável de ambiente
bot.run(os.getenv("TOKEN"))
