import asyncio
import os

import discord
from discord import app_commands
from discord.ext import commands
import generate

intents = discord.Intents.default()
intents.message_content = True
intents.voice_states = True

bot = commands.Bot(command_prefix="!", intents=intents)


@bot.event
async def on_ready():
    await bot.tree.sync()
    print(f"Logged in as {bot.user} and slash commands synced.")


# Join voice channel and play audio
@bot.tree.command(name="play", description="Generate and play music")
@app_commands.describe(query="Prompt for the music to generate")
async def play(interaction: discord.Interaction, query: str):
    voice_channel = interaction.user.voice.channel if interaction.user.voice else None
    if not voice_channel:
        await interaction.response.send_message("You need to be in a voice channel.", ephemeral=True)
        return
    # Connect to the voice channel
    vc = await voice_channel.connect()
    # Defer the response to allow time for processing
    await interaction.response.defer(thinking=True)

    # Call the generate function (slow part)
    # Run the blocking generation in a thread
    status, url, content = await asyncio.to_thread(
        generate.generate,
        query,
        bearer_token=os.getenv("RIFFUSION_TOKEN")
    )
    # Play the audio and disconnect after it's done
    vc.play(discord.FFmpegPCMAudio(url, executable="ffmpeg"), after=lambda e: print(f"Finished playing: {e}"))

    # Send the follow-up message once generation is done
    await interaction.followup.send(f"Now playing: https://www.riffusion.com/song/{status['id']}")
    # send content as txt file
    with open("llm-pass.txt", "w") as f:
        f.write(content)
    await interaction.followup.send(file=discord.File("llm-pass.txt"))


@bot.tree.command(name="stop", description="Stop the music")
async def stop(interaction: discord.Interaction):
    voice_channel = interaction.user.voice.channel if interaction.user.voice else None
    if not voice_channel:
        await interaction.response.send_message("You need to be in a voice channel.", ephemeral=True)
        return

    vc = discord.utils.get(bot.voice_clients, guild=interaction.guild)
    if vc and vc.is_connected():
        await vc.disconnect(force=True)
        await interaction.response.send_message("Stopped playing music.")
    else:
        await interaction.response.send_message("I'm not playing any music.", ephemeral=True)


# run the bot
bot.run(os.getenv("DISCORD_TOKEN"))
