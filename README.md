# 🎵 SteelSeries Spotify Linker
![GitHub Downloads (all assets, all releases)](https://img.shields.io/badge/Windows-0078D6?style=for-the-badge&logo=windows&logoColor=white)
![GitHub License](https://img.shields.io/github/license/ImFireGod/SteelSeries-Spotify-Linker?style=for-the-badge)
![GitHub Downloads (all assets, all releases)](https://img.shields.io/github/downloads/ImFireGod/SteelSeries-Spotify-Linker/total?style=for-the-badge)

SteelSeries Spotify Linker is a project designed to display the current music playing on **Spotify** on a SteelSeries keyboard with an **OLED** display. Presently, it supports only **128x40 displays** (e.g. Apex Pro).
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
- Displays a clock if no music is playing or if the music has been paused for too long (configurable)
- Different clock display modes (12-hour or 24-hour)
- Easily configurable via the system tray menu

## 🛠️ Prerequisites
You'll need Python version 3.8 or higher, which can be installed from [here](https://www.python.org/downloads/). <br>You'll also need the [SteelSeries GG](https://fr.steelseries.com/gg/engine) software.

## 🚀 Installation
1. Download the [latest version](https://github.com/ImFireGod/SteelSeries-Spotify-Linker/releases/latest) of the program and extract the files.
2. Run `install.bat` to start the installation prompt and set up your Spotify credentials.<br>For detailed instructions, refer to "[Spotify API configuration](CONFIGURE_SPOTIFY_API.md)".
3. You can now launch the application from the Windows Startup menu.

**📄 <ins>Note :</ins> When you launch the program for the first time, a web page will open to authorize the Spotify API to connect to your account.**

> ⚠️ If you want to uninstall the application, don't forget to exit it first using the button in the system tray.

#### ℹ️ Additional Installation Information  

If you haven't configured your Spotify credentials, an error message will appear when launching the application. **Do not close it immediately!**  

1. Open the **system tray menu** (located in the bottom-right corner of the taskbar).
2. Click on **"Open configuration"** to access the settings file and enter your Spotify credentials.
3. Close the error message.  
4. Restart the application. 


### 🐛 Debug Mode

A debug mode is available in the software folder `launcher_debug` (by default, the installation path is `C:\Program Files\SpotifyLinker`). This will allow you to view the output for troubleshooting purposes.

## ⚙ Configuration
The configuration file is stored in `%APPDATA%/SpotifyLinker`.
To configure the Spotify API, refer to [Spotify API configuration](CONFIGURE_SPOTIFY_API.md).
```JS
{
  ...
  "date_format": 12,        // Choose between 12-hour or 24-hour format
  "display_seconds": true,  // Set to 'true' to display seconds, 'false' to hide 
  "timer_threshold": 2,     // Set the number of seconds after which the clock will appear after pausing the song
  "spotify_fetch_delay": 2, // Represents the delay in seconds between each spotify API request
  "extended_font": true,    // Support for special characters (Japanese)
  "display_timer": true,
  "display_player": true
}
```
> ⚠️ You can reduce the time between requests to the Spotify API. But be careful, if you reduce it too much, the application may not work properly. The Spotify API may block it due to rate limits. By default, this interval is set to 2 seconds to ensure that you never exceed this limit, but feel free to adjust it to suit your needs. For more information, please visit the [Spotify Rate Limits](https://developer.spotify.com/documentation/web-api/concepts/rate-limits).

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
