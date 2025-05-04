import discord
from discord import app_commands
from discord.ext import tasks
from googleapiclient.discovery import build
import google.auth
from google.auth import exceptions

intents = discord.Intents.default()
intents.members = True
client = discord.Client(intents=intents, reconnect=True)
tree = app_commands.CommandTree(client)

TOKEN = "Your BOT-TOKEN"
YOUTUBE_API_KEY = "Your Youtube-API-Key"
CHANNEL_ID = "Channel id of the channel you want to inform the video about."
YOUTUBE_CHANNEL_ID = "Channel id of the youtube channel you wish to inform"
GOOGLE_APPLICATION_CREDENTIALS = "./google_cloud.json"

try:
    credentials, project = google.auth.load_credentials_from_file(GOOGLE_APPLICATION_CREDENTIALS)
    youtube_client = build("youtube", "v3", credentials=credentials)
except exceptions.DefaultCredentialsError as e:
    print(f"An authentication error has occurred.: {e}")
    exit(1)

youtube = build('youtube', 'v3', developerKey=YOUTUBE_API_KEY)
latest_video_url = None

@client.event
async def on_ready():
    global latest_video_url
    await tree.sync()
    video_title, video_url, video_thumbnail = get_video()
    latest_video_url = video_url
    check_new_videos_setup.start()
    print(f"We have logged in as {client.user}")

def get_video():
    try:
        response = youtube_client.search().list(
            part="snippet",
            channelId=YOUTUBE_CHANNEL_ID,
            order="date",
            maxResults=1,
            type="video"
        ).execute()

        video_id = response['items'][0]['id']['videoId']
        video_title = response['items'][0]['snippet']['title']
        video_thumbnail = response['items'][0]['snippet']['thumbnails']['high']['url']
        video_url = f"https://www.youtube.com/watch?v={video_id}"

        return video_title, video_url, video_thumbnail
    except Exception as e:
        print(f"Error fetching YouTube video: {e}")
        return None, None, None

@tasks.loop(minutes=60)
async def check_new_videos_setup():
    await check_new_video()
    
async def check_new_video():
    global latest_video_url

    try:
        response = youtube_client.search().list(
            part="snippet",
            channelId=YOUTUBE_CHANNEL_ID,
            order="date",
            maxResults=1,
            type="video"
        ).execute()

        # Extract video details
        video_id = response['items'][0]['id']['videoId']
        video_url = f"https://www.youtube.com/watch?v={video_id}"

        # Check if this is a new video (by comparing URLs)
        if video_url != latest_video_url:
            channel = client.get_channel(int(CHANNEL_ID))
            
            await channel.send(f"{video_url} A new video has been released!:tada:")

            # Update the latest video URL
            latest_video_url = video_url
        else:
            print("No new video.")

    except Exception as e:
        print(f"An error has occurred.: {e}")

@tree.command(name="debug", description="For debugging")
async def debug(interaction: discord.Interaction, mode: str):
    global latest_video_url
    if mode == "youtube":
        await interaction.response.defer(ephemeral=True)

        video_title, video_url, video_thumbnail = get_video()

        await interaction.followup.send(
            f"Latest: {latest_video_url}\nNew_url: {video_url}\nNew_title: {video_title}\nNew_thumbnail: {video_thumbnail}",
            ephemeral=True
        )
    elif mode == "video":
        latest_video_url = None
        await check_new_video()
        await interaction.response.send_message("The latest video URL has been reset.",ephemeral=True)
    else:
        channel = client.get_channel(int(CHANNEL_ID))
        await channel.send(f"{mode} A new video has been released!:tada:")
        await interaction.response.send_message("The specified video was submitted!",ephemeral=True)

client.run(TOKEN)
