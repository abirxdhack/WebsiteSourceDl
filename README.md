# 🌐 Web Source Downloader Bot 🤖

[![Pyrogram](https://img.shields.io/badge/Pyrogram-v2blue)](https://docs.pyrogram.org/)
[![Python](https://img.shields.io/badge/Python-3.9+-brightgreen)](https://www.python.org/downloads/release/python-390/)
[![License](https://img.shields.io/badge/License-MIT-yellow)](https://opensource.org/licenses/MIT)
[![Stars](https://img.shields.io/github/stars/abirxdhack/WebsiteSourceDl?style=social)](https://github.com/abirxdhack/WebsiteSourceDl/stargazers)
[![Forks](https://img.shields.io/github/forks/abirxdhack/WebsiteSourceDl?style=social)](https://github.com/abirxdhack/WebsiteSourceDl/network/members)
[![Issues](https://img.shields.io/github/issues/abirxdhack/WebsiteSourceDl)](https://github.com/abirxdhack/WebsiteSourceDl/issues)

Welcome to the **Web Source Downloader Bot**! This bot allows you to download the source code of any webpage effortlessly, including HTML, CSS, JS, images, fonts, and media.

## ✨ Features

- 📥 **Download Full Website Source**: Fetch complete source code including HTML, CSS, JS, images, fonts, and media files.
- 📂 **Organized Download**: Files are organized into folders and zipped for easy access.
- 🔒 **Works in Private and Group Chats**: Use the bot in private chats, groups, or supergroups.
- ⚡ **Large Archive Support**: Supports archives up to **50 MB**.
- 🛠️ **Flexible Commands**: Use commands with prefixes `,`, `.`, `/`, `!`, or `#`.
- 📢 **Updates Channel**: Stay updated via the official channel.

## 🚀 Usage

1. **Start the Bot**: Send the `,start`, `.start`, `/start`, `!start`, or `#start` command to see the welcome message and available options.
2. **Download Source Code**: Use the `,ws <URL>`, `.ws <URL>`, `/ws <URL>`, `!ws <URL>`, or `#ws <URL>` command (or similarly for `websource`) to download the source code of a webpage.

### Example

To download the source code of `https://example.com`, use the following command:

```
/ws https://example.com
```

## 📢 Stay Updated

Stay updated with our channel:

- 🔄 [Updates Channel](https://t.me/abirxdhackz)

## 👨‍💻 Developer

- [My Dev](https://t.me/7303810912)

## 🛠️ Setup

### Prerequisites

- Python 3.9+
- Pyrogram
- A Telegram Bot Token

### Installation

1. **Clone the repository**:
    ```sh
    git clone https://github.com/abirxdhack/WebsiteSourceDl.git
    cd WebsiteSourceDl
    ```

2. **Edit The `config.py` file**:
    ```python
    API_ID = "your_api_id"
    API_HASH = "your_api_hash"
    BOT_TOKEN = "your_bot_token"
    COMMAND_PREFIX = [",", ".", "/", "!", "#"]
    UPDATES_CHANNEL_URL = "t.me/abirxdhackz"
    ```

3. **Install Modules**
   ```
   pip3 install -r requirements.txt
   ```
   
4. **Run the bot**:
    ```sh
    python3 main.py
    ```

## Configuration

1. Open the `config.py` file in your favorite text editor.
2. Replace the placeholders for `API_ID`, `API_HASH`, `BOT_TOKEN`, `COMMAND_PREFIX`, and `UPDATES_CHANNEL_URL` with your actual values:
   - **`API_ID`**: Your API ID from [my.telegram.org](https://my.telegram.org).
   - **`API_HASH`**: Your API Hash from [my.telegram.org](https://my.telegram.org).
   - **`BOT_TOKEN`**: The token you obtained from [@BotFather](https://t.me/BotFather).
   - **`COMMAND_PREFIX`**: List of command prefixes `[",", ".", "/", "!", "#"]`.
   - **`UPDATES_CHANNEL_URL`**: Set to `t.me/abirxdhackz`.

## Deploy the Bot

```sh
git clone https://github.com/abirxdhack/WebsiteSourceDl
cd WebsiteSourceDl
pip3 install -r requirements.txt
python3 main.py
```

