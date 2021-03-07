from redbot.core import commands, Config
from redbot.core.utils.chat_formatting import humanize_list
import discord
import asyncio
import random
import aiohttp

class AutoAvatar(commands.Cog):
    """automatically changes bot avatar"""

    def __init__(self, bot):
        self.bot = bot
        self.config = Config.get_conf(self, identifier=696969696969494)
        default_global = { "avatars": [ 'https://avatars.githubusercontent.com/u/23690422?s=400&v=4'] }
        self.config.register_global(**default_global)
        self.avatar_task = asyncio.create_task(self.wait_for_avatar())

    def cog_unload(self):
        self.avatar_task.cancel()

    async def wait_for_avatar(self):
        await self.bot.wait_until_red_ready()
        while True:
            try:
                await self.change_avatar()
                await asyncio.sleep(10800)
            except asyncio.CancelledError:
                break
    
    async def change_avatar(self):
        all_avatars = await self.config.avatars()
        new_avatar = random.choice(all_avatars)
        async with aiohttp.ClientSession() as session:
            async with session.get(new_avatar) as request:
                avatar = await request.read()
        await self.bot.user.edit(avatar=avatar)

    @commands.command()
    @commands.is_owner()
    async def addavatar(self, ctx, link: str):
        all_avatars = await self.config.avatars()
        if link.startswith('https://'):
            pass
        else:
            if link.startswith('http://'):
                pass
            else: 
                await ctx.send("That doesn't look like a valid link!")
                return
        if link not in all_avatars:
            all_avatars.append(link)
            await self.config.avatars.set(all_avatars)
            await ctx.send(f"Okay, I've added {link} to list of avatars.")
        else:
            await ctx.send(f"{link} was already in my list of avatars, did you mean to remove it?")

    @commands.command()
    @commands.is_owner()
    async def removeavatar(self, ctx, link: str):
        all_avatars = await self.config.avatars()
        if link in all_avatars:
            all_avatars.remove(link)
            await self.config.avatars.set(all_avatars)
            await ctx.send(f"Okay, I've removed {link} from my list of avatars.")
        else:
            await ctx.send(f"{link} wasn't in my list of avatars, did you mean to add it?")

    @commands.command()
    @commands.is_owner()
    async def listavatars(self, ctx):
        all_avatars = await self.config.avatars()
        if not all_avatars:
            await ctx.send("Nothing. This might cause some errors, yikes!")
        paginator = discord.ext.commands.help.Paginator()
        for obj in all_avatars:
            paginator.add_line(obj)
        await ctx.send('List of all bot avatars:')
        for page in paginator.pages:
            await ctx.send(page)

    @commands.command()
    async def submitavatar(self, ctx, link: str):
        if link.startswith('https://'):
            pass
        else:
            if link.startswith('http://'):
                pass
            else: 
                await ctx.send("That doesn't look like a valid link!")
                return
        channel = self.bot.get_channel(818239460004855888)
        await channel.send(f"Someone has submitted a new avatar! Here's the link: {link}")
        await ctx.send("Thanks for the submission! It'll be taken into consideration.")