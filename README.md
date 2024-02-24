# 🎵 SteelSeries Spotify Linker
![GitHub Downloads (all assets, all releases)](https://img.shields.io/badge/Windows-0078D6?style=for-the-badge&logo=windows&logoColor=white)
![GitHub License](https://img.shields.io/github/license/ImFireGod/SteelSeries-Spotify-Linker?style=for-the-badge)
![GitHub Downloads (all assets, all releases)](https://img.shields.io/github/downloads/ImFireGod/SteelSeries-Spotify-Linker/total?style=for-the-badge)

SteelSeries Spotify Linker is a project designed to display the current music playing on **Spotify** on a SteelSeries keyboard with an **OLED** display. Presently, it supports only **128x40 displays** (e.g., Apex Pro).
<br/>
<br/>

<div align="center">
  <img src="https://github.com/ImFireGod/SteelSeries-Spotify-Linker/assets/49344172/9f96c4bd-a123-436b-ace1-f7f5de4f0be0" alt="player_preview.gif">
  &nbsp&nbsp&nbsp
  <img src="https://github.com/ImFireGod/SteelSeries-Spotify-Linker/assets/49344172/a006d08a-f802-4603-8d5f-e2a62e9a83ef" alt="timer_preview.gif">
</div>

## ✨ Features
- Retrieves the currently playing music on Spotify via the API.
- Automatically updates the OLED display with the current track information.
- Features automatic scrolling titles, a progress bar, and displays elapsed time and duration.
- Clock display if no music is playing or if music has been paused for too long (configurable)
- Different clock display modes (12-hour or 24-hour)

## 🛠️ Prerequisites
You'll need Python version 3.8 or higher, which can be installed from [here](https://www.python.org/downloads/).
You'll also need the [SteelSeries GG](https://fr.steelseries.com/gg/engine) software.

## 🚀 Installation
1. Download the [latest version](https://github.com/ImFireGod/SteelSeries-Spotify-Linker/releases/latest) of the program and extract the files.
2. Run `pip install -r requirements.txt` in the application folder (You can also use a [virtual environment](#ℹ%EF%B8%8F-setting-up-venv) if you prefer).
3. Rename the `.env.example` file to `.env`. To configure the application, refer to "[Spotify API configuration](CONFIGURE_SPOTIFY_API.md)" and "[Configuration](#-configuration)".
4. Launch the program `start.bat` in a terminal by executing `./start.bat`.
5. Check that everything is working properly.

**📄 <ins>Note :</ins> When you launch the program for the first time, a web page will open to authorize the spotify api to connect to your account.**
### ℹ️ How to launch the application at startup?
1. Press `Win + R` to open the "Run" dialog.
2. Create a new file with a `.vbs` extension (e.g. SpotifyLinker.vbs).
3. Copy and paste the code provided below into the file, making sure to replace "C:\Path\To\start.bat" path with the actual path to your `start.bat` file.
```VBS
Set WshShell = CreateObject("WScript.Shell")
WshShell.Run chr(34) & "C:\path\to\start.bat" & chr(34), 0
Set WshShell = Nothing
```

### ℹ️ Setting up `venv`
*It's not mandatory to use a virtual environment, but it can avoid problems of conflict with other programs.*<br/><br/>
💡 Before you begin, open a `PowerShell` session in **administrator mode** within the project directory.
1. If you are not in the application folder, go into with `cd C:\path\to\project`
2. Run `python -m venv venv` to create the virtual environment.
3. Activate the virtual environment by running `.\venv\Scripts\Activate.ps1`<br/>
> ⚠️ In case of permission issues, you might need to set the execution policy to unrestricted using `set-executionpolicy unrestricted`. You can revert to the default execution policy by simply running `set-executionpolicy restricted`.
4. Run `pip install -r requirements.txt`
5. You're all set! Run your application within the virtual environment using `./start.bat`.


## ⚙ Configuration
To configure the Spotify API, refer to [Spotify API configuration](CONFIGURE_SPOTIFY_API.md).
```ENV
[Configuration]
DATE_FORMAT=12        # Choose between 12-hour or 24-hour format
DISPLAY_SECONDS=true  # Set to 'true' to display seconds, 'false' to hide them
TIMER_THRESHOLD=2     # Set the number of seconds after which the clock will appear after pausing the song
SPOTIFY_FETCH_DELAY=2 # Represents the delay in seconds between each spotify API request
```
> ⚠️ You can reduce the time between requests to the Spotify API. But be careful, if you reduce it too much, the application may not work properly. The Spotify API could block it due to throughput limits. By default, this interval is set to 2 seconds to ensure that you never exceed this limit, but feel free to adjust it to suit your needs. For more information, please visit the [Spotify Rate Limits](https://developer.spotify.com/documentation/web-api/concepts/rate-limits).

## 📝 Information
Music display may take some time due to API limitations. Data is retrieved by default every 2 seconds via Spotify's API, so there may be a slight desynchronization.

## 📚 Sources
- [Spotify Web API](https://developer.spotify.com/documentation/web-api)
- [SteelSeries GameSense™ SDK](https://github.com/SteelSeries/gamesense-sdk)

## 📧 Contact & Support ❤
<div align="left">
  <a href="https://discordapp.com/users/391697907667042304">
    <img src="https://img.shields.io/badge/Discord-blue?style=for-the-badge&logo=discord&logoColor=white" alt="Discord"/>
  </a>&nbsp
  <a href="https://ko-fi.com/Y8Y7UU8SZ">
    <img src="https://img.shields.io/badge/Ko--fi-Support-019cde?logo=ko-fi&style=for-the-badge" alt="KoFi">
  </a>
</div>
