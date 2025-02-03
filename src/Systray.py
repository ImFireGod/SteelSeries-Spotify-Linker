import logging
import os
import atexit
from threading import Thread
from PIL import Image
from pystray import MenuItem as Item, Icon, Menu

from src.utils import fetch_app_data_path, fetch_content_path

logger = logging.getLogger("Systray")
systray_thread = None

def exit_app(icon):
    icon.stop()

    # Remove lock file on exit
    lock_file_path = fetch_app_data_path('.lock')
    if os.path.exists(lock_file_path):
        os.unlink(lock_file_path)

    logger.info("Disabled systray")
    os._exit(0)

def enable_spotify_linker(icon):
    icon.manager.enabled = not icon.manager.enabled
    icon.update_menu()

def toggle_clock(icon):
    if not icon.manager.user_preferences.valid:
        return
    
    icon.manager.display_clock = not icon.manager.display_clock
    icon.manager.user_preferences.save_preferences()
    icon.update_menu()

def toggle_player(icon):
    if not icon.manager.user_preferences.valid:
        return
    
    icon.manager.display_player = not icon.manager.display_player
    icon.manager.user_preferences.save_preferences()
    icon.update_menu()

def open_config(icon):
    os.startfile(icon.manager.user_preferences.config_path)

def run_systray_async(display_manager):
    global systray_thread
    if systray_thread:
        return

    menu = (
        Item("Enable Spotify Linker", enable_spotify_linker, checked=lambda item: display_manager.enabled),
        Item("Display Clock", toggle_clock, checked=lambda item: display_manager.display_clock, enabled=lambda item: display_manager.enabled),
        Item("Display Player", toggle_player, checked=lambda item: icon.manager.display_player, enabled=lambda item: display_manager.enabled),
        Menu.SEPARATOR,
        Item("Open data folder", lambda item: os.startfile(fetch_app_data_path())),
        Item("Open configuration", open_config),
        Item("Update configuration", display_manager.update_config),
        Menu.SEPARATOR,
        Item("Exit", exit_app)
    )

    icon = Icon("name", Image.open(fetch_content_path("./assets/icon.png")), "Spotify Linker", menu)
    icon.manager = display_manager

    logger.info("Enabled systray")
    systray_thread = Thread(target=icon.run, daemon=True)
    systray_thread.start()

    atexit.register(lambda: exit_app(icon))
