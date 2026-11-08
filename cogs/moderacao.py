import discord
from discord import app_commands
from discord.ext import commands

class Moderacao(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="ban", description="Bane um usuário do servidor.")
    @app_commands.describe(usuario="Usuário que será banido", motivo="Motivo do banimento")
    @app_commands.checks.has_permissions(ban_members=True)
    async def ban(self, interaction: discord.Interaction, usuario: discord.Member, motivo: str = "Não informado"):
        try:
            await usuario.ban(reason=motivo)
            embed = discord.Embed(
                title="🔨 Usuário Banido",
                description=f"**Usuário:** {usuario.mention}\n**ID:** `{usuario.id}`\n**Motivo:** {motivo}\n**Moderador:** {interaction.user.mention}",
                color=discord.Color.red()
            )
            await interaction.response.send_message(embed=embed)
        except discord.Forbidden:
            await interaction.response.send_message("❌ Não tenho permissão para banir esse usuário.", ephemeral=True)

    @app_commands.command(name="unban", description="Remove o banimento de um usuário.")
    @app_commands.describe(usuario_id="ID do usuário que será desbanido", motivo="Motivo do desbanimento")
    @app_commands.checks.has_permissions(ban_members=True)
    async def unban(self, interaction: discord.Interaction, usuario_id: str, motivo: str = "Não informado"):
        try:
            user = await self.bot.fetch_user(int(usuario_id))
            await interaction.guild.unban(user, reason=motivo)
            embed = discord.Embed(
                title="✅ Usuário Desbanido",
                description=f"**Usuário:** {user.mention}\n**ID:** `{user.id}`\n**Motivo:** {motivo}\n**Moderador:** {interaction.user.mention}",
                color=discord.Color.green()
            )
            await interaction.response.send_message(embed=embed)
        except (ValueError, discord.NotFound):
            await interaction.response.send_message("❌ Usuário não encontrado na lista de banidos.", ephemeral=True)
        except discord.Forbidden:
            await interaction.response.send_message("❌ Não tenho permissão para desbanir.", ephemeral=True)

    @ban.error
    @unban.error
    async def erro_permissao(self, interaction: discord.Interaction, error):
        if isinstance(error, app_commands.errors.MissingPermissions):
            await interaction.response.send_message("❌ Você não tem permissão para usar isso.", ephemeral=True)

async def setup(bot):
    await bot.add_cog(Moderacao(bot))
