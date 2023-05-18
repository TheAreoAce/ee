import discord
import datetime
from discord.ext import commands

start_time = datetime.datetime.now()

@commands.command()
async def KGEG(ctx):
    await ctx.send("https://freeimage.host/i/HgBwPKx Check Out More Here: https://chartfox.org/KGEG")

@commands.command()
async def about(ctx):
    await ctx.send("**About us:** We are a community passionate for Microsoft Flight Simulator!")

@commands.command()
@commands.has_permissions(ban_members=True)
async def ban(ctx, member: discord.Member, *, reason=None):
    await member.ban(reason=reason)
    await ctx.send(f'{member.name} has been banned.')
    if reason:
        try:
            await member.send(f"You have been banned from {ctx.guild.name}.\nReason: {reason}")
        except discord.HTTPException:
            pass

@ban.error
async def ban_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("You don't have permission to use this command.")

@commands.command()
@commands.has_permissions(ban_members=True)
async def unban(ctx, member_id: int):
    banned_users = await ctx.guild.bans()
    for ban_entry in banned_users:
        if ban_entry.user.id == member_id:
            await ctx.guild.unban(ban_entry.user)
            await ctx.send(f'{ban_entry.user.name} has been unbanned.')
            return
    await ctx.send("User not found in the ban list.")

@unban.error
async def unban_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("You don't have permission to use this command.")

@commands.command()
async def uptime(ctx):
    current_time = datetime.datetime.now()
    uptime = current_time - start_time
    await ctx.send(f"Bot uptime: ``{uptime}``")

@commands.command()
@commands.has_permissions(kick_members=True)
async def mute(ctx, member: discord.Member, *, reason=None):
    if member.id not in user_mutes:
        user_mutes[member.id] = 1
    else:
        user_mutes[member.id] += 1

    await ctx.send(f'{member.name} has been muted. Total mutes: {user_mutes[member.id]}')

    if user_mutes[member.id] >= mute_threshold:
        timeout_end = datetime.datetime.now() + timeout_duration
        timeout_duration_str = str(timeout_duration).split('.')[0]
        await member.add_roles(discord.utils.get(ctx.guild.roles, name="Muted"))
        await ctx.send(f'{member.name} has reached the mute threshold and has been muted for {timeout_duration_str}.')
        await member.send(f'You have been muted in {ctx.guild.name} for {timeout_duration_str}.\nReason: {reason}\nYou will be automatically unmuted after the mute duration.')

        # Schedule the automatic unmuting
        await asyncio.sleep(timeout_duration.total_seconds())
        await member.remove_roles(discord.utils.get(ctx.guild.roles, name="Muted"))
        await ctx.send(f'{member.name} has been unmuted after the mute duration.')

@mute.error
async def mute_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("You don't have permission to use this command.")

@commands.command()
async def membercount(ctx):
    guild = ctx.guild
    total_members = guild.member_count
    online_members = len([member for member in guild.members if member.status != discord.Status.offline])
    bot_members = len([member for member in guild.members if member.bot])
    human_members = total_members - bot_members

    embed = discord.Embed(
        title="Member Count",
        color=discord.Color.blue()
    )
    embed.add_field(name="Total Members", value=str(total_members))
    embed.add_field(name="Online Members", value=str(online_members))
    embed.add_field(name="Human Members", value=str(human_members))
    embed.add_field(name="Bot Members", value=str(bot_members))

    await ctx.send(embed=embed)

def setup(bot):
    bot.add_command(KGEG)
    bot.add_command(about)
    bot.add_command(ban)
    bot.add_command(unban)
    bot.add_command(uptime)
    bot.add_command(mute)
    bot.add_command(membercount)
