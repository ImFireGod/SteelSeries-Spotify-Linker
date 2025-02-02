import os
import sys
import ctypes
import subprocess
import shutil
import json
import winreg

from version import __version__
from src.UserPreferences import UserPreferences

APPLICATION_NAME = "Spotify Linker"
PUBLISHER = "Firewe"

def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False
    
def request_admin():
    if not is_admin():
        print("You need to run this script as an administrator.")
        ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)
        sys.exit(1)

def abort_installation():
    input("Press Enter to exit...")
    sys.exit(1)

def ask_installation_path():
    installation_path = os.path.join(os.environ['ProgramFiles'], "SpotifyLinker")
    print(f"Default installation path : {installation_path}")
    response = input("Do you want to change the installation path? (y/N) ").strip().lower()

    if response == "y":
        while True:  # Équivalent de do-while
            installation_path = input("Enter the installation path (absolute path required): ").strip()

            if not os.path.isabs(installation_path):
                print("Please enter an absolute path.")
                continue

            if os.path.exists(installation_path) and os.path.isdir(installation_path):
                if os.listdir(installation_path):
                    create_new_dir = input("The directory is not empty. Do you want to create a 'SpotifyLinker' subdirectory? (Y/n) ").strip().lower()
                    if create_new_dir == "n":
                        print("Please choose an empty directory.")
                        continue
                    else:
                        installation_path = os.path.join(installation_path, "SpotifyLinker")
                        os.makedirs(installation_path, exist_ok=True)
                        print(f"Created new directory: {installation_path}")
                        break


                print(f"Using existing directory: {installation_path}")
                break
            else:
                try:
                    os.makedirs(installation_path)
                    print(f"Created new directory: {installation_path}")
                    break
                except OSError as e:
                    print(f"Error creating directory: {e}")
                    print("Please enter a valid path.")
    else:
        if os.path.exists(installation_path) and os.listdir(installation_path):
            clean_dir = input("The directory is not empty. Do you want to clean it? (y/N) ").strip().lower()
            if clean_dir == "y":
                try:
                    shutil.rmtree(installation_path)
                    os.makedirs(installation_path, exist_ok=True)
                    print(f"Cleaned and created new directory: {installation_path}")
                except OSError as e:
                    print(f"Error cleaning directory: {e}")
                    abort_installation()
            else:
                print("Installation aborted.")
                abort_installation()
        else:
            try:
                os.makedirs(installation_path, exist_ok=True)
            except OSError as e:
                print(f"Error creating directory: {e}")
                abort_installation()
    
        print(f"Using default directory: {installation_path}")
    return installation_path

def copy_files(installation_path):
    src_files = ['main.py', 'version.py', 'launcher.exe', 'requirements.txt', 'uninstall.exe']
    src_dirs = ['src', 'assets', 'fonts']

    try: 
        for file in src_files:
            shutil.copy(file, installation_path)
            print(f"Copied {file} to {installation_path}")

        for directory in src_dirs:
            dest_dir = os.path.join(installation_path, directory)
            shutil.copytree(directory, dest_dir, ignore=shutil.ignore_patterns('__pycache__'))
            print(f"Copied {directory} to {dest_dir}")
    except OSError as e:
        print(f"Error copying files: {e}")
        abort_installation()


    print("Files copied successfully.")

def setup_venv(target_dir):
    venv_dir = os.path.join(target_dir, 'venv')
    if not os.path.exists(venv_dir):
        print("Creating virtual environment...")
        subprocess.run([sys.executable, '-m', 'venv', venv_dir], check=True)
    
    print("Installing dependencies...")
    subprocess.run([os.path.join(venv_dir, 'Scripts', 'pip'), 'install', '-r', 'requirements.txt'], check=True)

def create_user_preferences():
    config_dir = os.path.join(os.getenv('APPDATA'), 'SpotifyLinker')
    config_file = os.path.join(config_dir, 'config.json')

    if not os.path.exists(config_dir):
        os.makedirs(config_dir)

    if os.path.exists(config_file):
        return
    
    # Create a config with default values
    user_preferences = UserPreferences.DEFAULT

    try:
        configure_now = input("Do you want to configure the Spotify API now? (Y/n) ").strip().lower()
        if configure_now == "n":
            print("Warning: You will need to configure the Spotify API later")
        else:
            user_preferences["spotify_client_id"] = input("Enter your Spotify Client ID: ").strip()
            user_preferences["spotify_client_secret"] = input("Enter your Spotify Client Secret: ").strip()
            user_preferences["spotify_redirect_uri"] = input("Enter your Spotify Redirect URI: ").strip()
            user_preferences["local_port"] = input("Enter the local port (default: 2408): ").strip() or 2408

        with open(config_file, 'w') as f:
            json.dump(user_preferences, f, indent=4)

    except Exception as e:
        print(f"Error creating user preferences: {e}")
        abort_installation()

def create_shortcut(installation_path):
    script_path = os.path.join(installation_path, "launcher.exe")
    shortcut_path = os.path.join(os.environ['APPDATA'], "Microsoft", "Windows", "Start Menu", "Programs", "SpotifyLinker.lnk")
    icon_path = os.path.join(installation_path, "assets", "icon.ico")

    # Créer le raccourci principal
    powershell_command = f'$WshShell = New-Object -comObject WScript.Shell; $Shortcut = $WshShell.CreateShortcut("{shortcut_path}"); $Shortcut.TargetPath = "{script_path}"; $Shortcut.IconLocation = "{icon_path}"; $Shortcut.Save()'
    subprocess.run(["powershell", "-Command", powershell_command], check=True)

    # Créer le raccourci de débogage
    debug_shortcut_path = os.path.join(installation_path, "launcher_debug.lnk")
    debug_powershell_command = f'$WshShell = New-Object -comObject WScript.Shell; $Shortcut = $WshShell.CreateShortcut("{debug_shortcut_path}"); $Shortcut.TargetPath = "{script_path}"; $Shortcut.Arguments = "--debug"; $Shortcut.IconLocation = "{icon_path}"; $Shortcut.Save()'
    subprocess.run(["powershell", "-Command", debug_powershell_command], check=True)

    print(f"Debug shortcut created at {debug_shortcut_path}")

    return shortcut_path

def add_to_startup(shortcut_path):
    startup_dir = os.path.join(os.getenv('APPDATA'), 'Microsoft\\Windows\\Start Menu\\Programs\\Startup')
    startup_shortcut = os.path.join(startup_dir, "SpotifyLinker.lnk")

    if os.path.exists(startup_shortcut):
        os.unlink(startup_shortcut)

    os.symlink(shortcut_path, startup_shortcut)

    print(f"Added shortcut to startup: {startup_shortcut}")

def add_to_startup_registry(installation_path):
    run_key = r"SOFTWARE\Microsoft\Windows\CurrentVersion\Run"
    info_key = r"SOFTWARE\SpotifyLinker"
    try:
        # Ajouter au démarrage
        reg_run = winreg.OpenKey(winreg.HKEY_CURRENT_USER, run_key, 0, winreg.KEY_SET_VALUE)
        winreg.SetValueEx(reg_run, "SpotifyLinker", 0, winreg.REG_SZ, 
                          os.path.join(installation_path, "launcher.exe"))
        winreg.CloseKey(reg_run)

        # Ajouter des informations supplémentaires
        reg_info = winreg.CreateKey(winreg.HKEY_CURRENT_USER, info_key)
        winreg.SetValueEx(reg_info, "Name", 0, winreg.REG_SZ, APPLICATION_NAME)
        winreg.SetValueEx(reg_info, "Publisher", 0, winreg.REG_SZ, PUBLISHER)
        winreg.SetValueEx(reg_info, "Version", 0, winreg.REG_SZ, __version__)
        winreg.CloseKey(reg_info)

        print("Added to startup registry with additional information.")
    except Exception as e:
        print(f"Error adding to startup registry: {e}")

    add_to_startup_registry()

def add_to_registry(installation_path):
    uninstall_exe = os.path.join(installation_path, "uninstall.exe")
    icon_path = os.path.join(installation_path, "assets", "icon.ico")

    key = r"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall\SpotifyLinker"
    try:
        reg = winreg.CreateKey(winreg.HKEY_LOCAL_MACHINE, key)
        winreg.SetValueEx(reg, "DisplayName", 0, winreg.REG_SZ, APPLICATION_NAME)
        winreg.SetValueEx(reg, "UninstallString", 0, winreg.REG_SZ, uninstall_exe)
        winreg.SetValueEx(reg, "InstallLocation", 0, winreg.REG_SZ, installation_path)
        winreg.SetValueEx(reg, "Publisher", 0, winreg.REG_SZ, "Firewe")
        winreg.SetValueEx(reg, "DisplayVersion", 0, winreg.REG_SZ, __version__)
        winreg.SetValueEx(reg, "EstimatedSize", 0, winreg.REG_DWORD, 35000)
        winreg.SetValueEx(reg, "DisplayIcon", 0, winreg.REG_SZ, icon_path)
        winreg.CloseKey(reg)
        print("Added to registry.")
    except Exception as e:
        print(f"Error adding to registry: {e}")

if __name__ == "__main__":
    request_admin()
    print("Welcome to SpotifyLinker installation !\n")

    # Select installation path
    installation_path = ask_installation_path()
    
    # Copy source files to installation path
    print("Copying files...")
    copy_files(installation_path)
    
    # Setup virtual environment and install dependencies
    print("Setting up virtual environment...")
    setup_venv(installation_path)

    # Create user preferences
    print("Creating user preferences...")
    create_user_preferences()

    # Create shortcut
    shortcut = create_shortcut(installation_path)
    print(f"Shortcut created at {shortcut}")

    # Ask to add to startup
    add_to_startup(shortcut)
    add_startup = input("Do you want to add SpotifyLinker to startup? (Y/n) ").strip().lower()
    if add_startup == "y":
        add_to_startup_registry()

    # Add to registry
    print("Adding to registry...")
    add_to_registry(installation_path)

    print("Installation completed !")
    input("Press Enter to exit...")