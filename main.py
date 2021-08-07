import discord
import os
from bot import Bot
from hidden import Hidden
from user_information import User_information
import youtube_dl
import asyncio

bot = Bot(Hidden().token())
client = bot.connect()


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


@client.command()
async def join(ctx):
    voiceChannel = discord.utils.get(ctx.guild.voice_channels, name='Geral')
    await voiceChannel.connect()

# ALTERAÇÕES NO PLAY
@client.command()
async def play(ctx, url : str):
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)

    song_there = os.path.isfile('song.mp3')
    
    playlist = []
    playlist.append(url)

    # CRIAR UMA CLASSE, PARA ARMAZENAR O NAME, DURATION E AS MUSICAS
    def name(ydl):
        info = ydl.extract_info(playlist[0])
        name = info['title']
        return name
    async def duration(ydl):
        info = ydl.extract_info(playlist[0])
        duration = info['duration']
        await asyncio.sleep(duration)

    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }]
    }

    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        title = name(ydl)
        ydl.download([playlist[0]])

    try:
        if voice.is_playing():
            with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                await duration(ydl) # USAR O TIME OU O DATETIME, PARA FAZER CALCULOS DO TEMPO REAL QUE ESTA TOCANDO A MUSICA
 
        if song_there:
            os.remove('song.mp3')
            
    except PermissionError:
        await ctx.send("Error")
        return

    for file in os.listdir("./"):
        if file.startswith(title):
            os.rename(file, "song.mp3")

    voice.play(discord.FFmpegPCMAudio("song.mp3"))


@client.command()
async def leave(ctx):
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
    if voice.is_connected():
        await voice.disconnect()
    else:
        await ctx.send("The bot is not connected to a voice channel.")


@client.command()
async def pause(ctx):
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
    if voice.is_playing():
        voice.pause()
    else:
        await ctx.send("Currently no audio is playing.")


@client.command()
async def resume(ctx):
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
    if voice.is_paused():
        voice.resume()
    else:
        await ctx.send("The audio is not paused.")


@client.command()
async def stop(ctx):
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
    voice.stop()














bot.run()