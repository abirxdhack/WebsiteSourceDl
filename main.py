import os
import re
import aiohttp
import asyncio
from concurrent.futures import ThreadPoolExecutor
from urllib.parse import urljoin, urlparse
from bs4 import BeautifulSoup
import zipfile
import shutil
from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram.enums import ParseMode, ChatType
from config import API_ID, API_HASH, BOT_TOKEN

# Initialize the app and user clients
app = Client(
    "app_session",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN
)

# Directory to save the downloaded files temporarily
DOWNLOAD_DIRECTORY = "./downloads/"

# Ensure the download directory exists
if not os.path.exists(DOWNLOAD_DIRECTORY):
    os.makedirs(DOWNLOAD_DIRECTORY)

class URLDownloader:
    """Download the webpage components based on the input URL."""
    
    def __init__(self, img_flg=False, link_flg=True, script_flg=True):
        self.soup = None
        self.img_flg = img_flg
        self.link_flg = link_flg
        self.script_flg = script_flg
        self.link_type = ('css', 'js')
        
    async def fetch(self, session, url):
        async with session.get(url) as response:
            return await response.read()
        
    async def save_page(self, url, page_folder='page'):
        """Save the web page components based on the input URL and directory name."""
        try:
            # Ensure the URL has a scheme
            if not urlparse(url).scheme:
                url = "https://" + url

            async with aiohttp.ClientSession() as session:
                response = await self.fetch(session, url)
                self.soup = BeautifulSoup(response, "html.parser")  # Use html.parser if lxml is not available
                if not os.path.exists(page_folder):
                    os.mkdir(page_folder)
                
                tasks = []
                if self.link_flg:
                    tasks.append(self._soup_find_and_save(session, url, page_folder, 'link', 'href'))
                if self.script_flg:
                    tasks.append(self._soup_find_and_save(session, url, page_folder, 'script', 'src'))
                
                await asyncio.gather(*tasks)
                
                with open(os.path.join(page_folder, 'page.html'), 'wb') as file:
                    file.write(self.soup.prettify('utf-8'))
                
                zip_path = self._zip_folder(page_folder, url)
                return zip_path
        except Exception as e:
            print(f"> save_page(): Create files failed: {str(e)}")
            return None

    async def _soup_find_and_save(self, session, url, page_folder, tag_to_find='link', inner='href'):
        """Save specified tag_to_find objects in the page_folder."""
        page_folder = os.path.join(page_folder, tag_to_find)
        if not os.path.exists(page_folder):
            os.mkdir(page_folder)
        
        tasks = []
        for res in self.soup.findAll(tag_to_find):
            if res.has_attr(inner):
                tasks.append(self._download_resource(session, url, res, page_folder, inner))
                
        await asyncio.gather(*tasks)
    
    async def _download_resource(self, session, url, res, page_folder, inner):
        """Download and save a resource."""
        try:
            filename = re.sub(r'\W+', '.', os.path.basename(res[inner]))
            if inner == 'href' and (not any(ext in filename for ext in self.link_type)):
                return

            file_url = urljoin(url, res.get(inner))
            file_path = os.path.join(page_folder, filename)

            res[inner] = os.path.join(os.path.basename(page_folder), filename)
            if not os.path.isfile(file_path):
                content = await self.fetch(session, file_url)
                if content:
                    with open(file_path, 'wb') as file:
                        file.write(content)
        except Exception as exc:
            print(exc)

    def _zip_folder(self, folder_path, url):
        """Zip the folder."""
        sanitized_url = re.sub(r'\W+', '_', url)
        zip_name = f"Smart_Tool_{sanitized_url}.zip"
        zip_path = os.path.join("downloads", zip_name)

        with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for root, dirs, files in os.walk(folder_path):
                for file in files:
                    file_path = os.path.join(root, file)
                    arcname = os.path.relpath(file_path, start=folder_path)
                    zipf.write(file_path, arcname)
        return zip_path

    def _remove_folder(self, folder_path):
        """Remove a folder and its contents."""
        shutil.rmtree(folder_path)

# ThreadPoolExecutor instance
executor = ThreadPoolExecutor(max_workers=5)  # You can adjust the number of workers

async def download_web_source(client: Client, message: Message):
    # Get the command and its arguments
    command_parts = message.text.split()

    # Check if the user provided a URL
    if len(command_parts) <= 1:
        await message.reply_text("**❌ Provide at least one URL.**", parse_mode=ParseMode.MARKDOWN, disable_web_page_preview=True)
        return

    url = command_parts[1]

    # Notify the user that the source code is being downloaded
    downloading_msg = await message.reply_text("**⚡️ Downloading Source Code...⌛️**", parse_mode=ParseMode.MARKDOWN, disable_web_page_preview=True)

    try:
        # Download the webpage components
        downloader = URLDownloader()
        page_folder = os.path.join("downloads", urlparse(url).netloc)
        
        # Run the save_page method in a separate thread
        loop = asyncio.get_event_loop()
        zip_path = await loop.run_in_executor(executor, asyncio.run, downloader.save_page(url, page_folder))

        if zip_path:
            # Send the zip file to the user
            if message.chat.type in [ChatType.SUPERGROUP, ChatType.GROUP] and not message.from_user:
                # In a group chat where user info is not available, link the group name with its URL
                group_name = message.chat.title
                group_url = f"https://t.me/{message.chat.username}" if message.chat.username else "Group"
                caption = (
                    f"**Source code Download**\n"
                    f"━━━━━━━━━━━━━━━━━━\n"
                    f"**Site:** {url}\n"
                    f"**Type:** HTML, CSS, JS\n"
                    f"━━━━━━━━━━━━━━━━━━\n"
                    f"**Source Downloaded By:** [{group_name}]({group_url})"
                )
            else:
                # In private chat or where user info is available
                user_full_name = f"{message.from_user.first_name} {message.from_user.last_name or ''}".strip()
                user_profile_link = f"https://t.me/{message.from_user.username}"
                caption = (
                    f"**Source code Download**\n"
                    f"━━━━━━━━━━━━━━━━━━\n"
                    f"**Site:** {url}\n"
                    f"**Type:** HTML, CSS, JS\n"
                    f"━━━━━━━━━━━━━━━━━━\n"
                    f"**Source Downloaded By:** [{user_full_name}]({user_profile_link})"
                )
            
            await client.send_document(
                chat_id=message.chat.id,
                document=zip_path,
                caption=caption,
                parse_mode=ParseMode.MARKDOWN
            )

            # Delete the zip file after sending
            os.remove(zip_path)

            # Delete the temporary files
            downloader._remove_folder(page_folder)

    except Exception as e:
        await message.reply_text(f"**❌ An error occurred: {str(e)}**", parse_mode=ParseMode.MARKDOWN, disable_web_page_preview=True)

    finally:
        # Delete the downloading message
        await downloading_msg.delete()

@app.on_message(filters.command(["ws"], prefixes=["/", "."]) & (filters.private | filters.group))
async def ws_command(client: Client, message: Message):
    # Run the download_web_source in the background to handle multiple requests simultaneously
    asyncio.create_task(download_web_source(client, message))

@app.on_message(filters.command(["start"], prefixes=["/", "."]) & filters.private)
async def start_command(client: Client, message: Message):
    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("🔄Update Channel", url="https://t.me/ModVipRM"), InlineKeyboardButton("🤚🏻Backup Channel", url="https://t.me/ModviprmBackup")],
        [InlineKeyboardButton("👮🏻‍♂️Proof Channel", url="https://t.me/Proofchannelch"), InlineKeyboardButton("My Dev👨‍💻", user_id=7303810912)]
    ])
    await message.reply_text(
        text="**Welcome to the Web Source Downloader Bot!**\n\n"
             "You can use this bot to download the source code of any webpage.\n\n"
             "**Example usage:**\n"
             "`/ws https://example.com`\n\n"
             "Stay updated with our channels:",
        reply_markup=keyboard,
        parse_mode=ParseMode.MARKDOWN
    )

if __name__ == "__main__":
    app.run()