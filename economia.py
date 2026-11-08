import discord
from discord.ext import commands
from discord import app_commands
from datetime import datetime, timedelta
from utils.database import get_db, get_or_create_user

class Economia(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="daily", description="Pegue suas moedas diárias")
    async def daily(self, interaction: discord.Interaction):
        user = get_or_create_user(interaction.user.id)
        agora = datetime.now()
        if user["ultimo_daily"]:
            ultimo = datetime.fromisoformat(user["ultimo_daily"])
            if agora - ultimo < timedelta(hours=24):
                falta = timedelta(hours=24) - (agora - ultimo)
                horas = int(falta.total_seconds() // 3600)
                await interaction.response.send_message(f"calma! nego, você já pegou hoje. volta em {horas}h.", ephemeral=True)
                return
        conn = get_db()
        conn.execute("UPDATE users SET moedas = moedas + 100, ultimo_daily = ? WHERE user_id = ?", (agora.isoformat(), interaction.user.id))
        conn.commit()
        conn.close()
        await interaction.response.send_message("Você ganhou **+100 moedas** hahahahah")

    @app_commands.command(name="rep", description="Dê +1 de reputação para alguém")
    async def rep(self, interaction: discord.Interaction, membro: discord.Member):
        if membro.id == interaction.user.id:
            await interaction.response.send_message("você kkkkkk !", ephemeral=True)
            return
        if membro.bot:
            await interaction.response.send_message("Não dá pra dar rep pra bot!", ephemeral=True)
            return
        get_or_create_user(membro.id)
        conn = get_db()
        conn.execute("UPDATE users SET rep = rep + 1 WHERE user_id = ?", (membro.id,))
        conn.commit()
        conn.close()
        await interaction.response.send_message(f"{interaction.user.mention} deu +1 rep para {membro.mention}! ✨")

async def setup(bot):
    await bot.add_cog(Economia(bot))
