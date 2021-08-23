from bot import Bot
from hidden import Hidden
from user_information import User_information
import DiscordUtils
import discord

bot = Bot(Hidden().token())
client = bot.connect()

music = DiscordUtils.Music()

@client.event
async def on_ready():
    print('Tamo on')
    print(client.get_guild(869709006439075890).members)

@client.command()
async def avatar(ctx, user_reference=''):
    if user_reference == '':
        user_reference = ctx.author.id

        user = User_information(ctx,user_reference)
        user_id = await client.fetch_user(user_reference)

        await ctx.send(embed=user.avatar(user_id))
    else:
        try:

            user = User_information(ctx,user_reference)
            user_id = await client.fetch_user(user.user_id)
            await ctx.send(embed=user.avatar(user_id)) 

        except:
            await ctx.send('Esse usuário não existe no servidor.')


# @client.command()
# async def join(ctx):
#     await ctx.author.voice.channel.connect() #Joins author's voice channel

@client.command()
async def leave(ctx):
    await ctx.voice_client.disconnect()

@client.command()
async def play(ctx, *, url):

    try:
        player = music.get_player(guild_id=ctx.guild.id)

        if not player:
            player = music.create_player(ctx, ffmpeg_error_betterfix=True)
    except DiscordUtils.NotConnectedToVoice:
        await ctx.author.voice.channel.connect()  
        player = music.get_player(guild_id=ctx.guild.id)

        if not player:
            player = music.create_player(ctx, ffmpeg_error_betterfix=True)

    
    if not ctx.voice_client.is_playing():
        await player.queue(url, search=True)

        song = await player.play()
        await ctx.send(f"Playing {song.name}")
    else:
        song = await player.queue(url, search=True)
        await ctx.send(embed=discord.Embed(
            title=f"Adicionado {song.name}",
            url = song.url,
            color = 0x690FC3,
            description = f'Duração: {song.duration}\nCanal: [{song.channel}]({song.channel_url})'
            ).set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url
            ).set_thumbnail(url=song.thumbnail
            ).set_footer(text=f"Música adicionada para a lista | Loop: {'✅' if song.is_looping else '❌'}", icon_url=ctx.guild.icon.url if ctx.guild.icon is not None else "https://cdn.discordapp.com/embed/avatars/1.png"))


@client.command()
async def pause(ctx):
    player = music.get_player(guild_id=ctx.guild.id)
    song = await player.pause()
    await ctx.send(f"Paused {song.name}")

@client.command()
async def resume(ctx):
    player = music.get_player(guild_id=ctx.guild.id)
    song = await player.resume()
    await ctx.send(f"Resumed {song.name}")

@client.command()
async def stop(ctx):
    player = music.get_player(guild_id=ctx.guild.id)
    await player.stop()
    await ctx.send("Stopped")

@client.command()
async def loop(ctx):
    player = music.get_player(guild_id=ctx.guild.id)
    song = await player.toggle_song_loop()
    if song.is_looping:
        await ctx.send(f"Enabled loop for {song.name}")
    else:
        await ctx.send(f"Disabled loop for {song.name}")

@client.command()
async def queue(ctx):
    player = music.get_player(guild_id=ctx.guild.id)
    await ctx.send(f"{', '.join([song.name for song in player.current_queue()])}")

@client.command(aliases=['np','tocando'])
async def nowplaying(ctx):
    player = music.get_player(guild_id=ctx.guild.id)
    song = player.now_playing()
    await ctx.send(song.name)

@client.command()
async def skip(ctx):
    player = music.get_player(guild_id=ctx.guild.id)
    data = await player.skip(force=True)
    if len(data) == 2:
        await ctx.send(f"Skipped from {data[0].name} to {data[1].name}")
    else:
        await ctx.send(f"Skipped {data[0].name}")

@client.command()
async def volume(ctx, vol):
    player = music.get_player(guild_id=ctx.guild.id)
    song, volume = await player.change_volume(float(vol) / 100) # volume should be a float between 0 to 1
    await ctx.send(f"Changed volume for {song.name} to {volume*100}%")

@client.command()
async def remove(ctx, index):
    player = music.get_player(guild_id=ctx.guild.id)
    song = await player.remove_from_queue(int(index))
    await ctx.send(f"Removed {song.name} from queue")


bot.run()