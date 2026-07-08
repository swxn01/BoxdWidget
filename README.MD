# BoxdWidget

Discord Widget to showcase your 4 favorite Letterboxd movies!

## Requirements

- [Python 3](https://www.python.org/)
- A Discord account with **Developer Mode** enabled





## Setup

### 1 . Clone and install

clone this repo and install the requirements
```bash, python
git clone https://github.com/swxn01/BoxdWidget
cd BoxdWidget
pip install -r requirements.txt
```

### 2. Install the Discord Widget Creator extension

This extension creates your Discord application and widget automatically.

1. Download or clone https://github.com/TheCreativeGod/Discord-Widgets-Extension
2. **Chrome / Edge / Brave**: `chrome://extensions` → Enable Developer Mode → Load unpacked → select the `chrome-extension/` folder
3. **Firefox**: `about:debugging#/runtime/this-firefox` → Load Temporary Add-on → select `firefox-extension/manifest.json`

### 3. Import the widget layout

1. Go to https://discord.com/developers/applications and reload the page once after installing the extension
2. Click the **Widget Creator** button in the bottom-right corner
3. Paste the full contents of **`widget-autoconfig.json`** from this repo
4. Click **Import** — the extension creates the application with the Boxdwidget layout and data fields preconfigured
5. Complete any captcha / 2FA if prompted

>
>

Once done, copy from the Developer Portal:
- **Application ID** → General Information page
- **Bot Token** → Bot page → Reset Token

And also don't forget to copy your Discord UserId from your profile popout


### 4. Configure  the`.env`

```env
LETTERBOXD_USERNAME=username
DISCORD_APPLICATION_ID=1572351531753974535
DISCORD_USER_ID=1524564396240108288
DISCORD_TOKEN=your_bot_token_here
```



### 5. Start the bot:

```bash
python main.py
```

### Credits:
https://github.com/BillMoney123/Overwidget for the HEAVY readme inspiration
https://github.com/TheCreativeGod/Discord-Widgets-Extension for the automatic widget config tool
