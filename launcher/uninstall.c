#include <windows.h>
#include <stdio.h>
#include <shlobj.h>
#include <process.h>

#define MAX_PATH 260

/**
 * Removes a directory and its contents without prompting the user.
 * @param path The path to the directory to remove.
 * @return void
 */
void RemoveDirectorySilently(const char* path) {
    char cmd[MAX_PATH * 2];
    snprintf(cmd, sizeof(cmd), "cmd /c rmdir /s /q \"%s\" > nul 2>&1", path);
    system(cmd);
}

/**
 * Retrieves the installation path of SpotifyLinker from the registry.
 * @param installPath The buffer to store the installation path.
 * @param bufferSize The size of the buffer.
 * @return 1 if the installation path was successfully retrieved, 0 otherwise.
 */
int GetInstallPath(char* installPath, DWORD bufferSize) {
    HKEY hKey;
    LONG result = RegOpenKeyEx(HKEY_LOCAL_MACHINE,
        "SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\SpotifyLinker",
        0, KEY_READ, &hKey);

    if (result != ERROR_SUCCESS) return 0;

    DWORD dataType;
    result = RegQueryValueEx(hKey, "InstallLocation", NULL, &dataType, 
                             (LPBYTE)installPath, &bufferSize);
    
    RegCloseKey(hKey);
    return (result == ERROR_SUCCESS) && (dataType == REG_SZ);
}

/**
 * Finishes the uninstallation process by removing the installation directory,
 * registry keys, and the Start Menu shortcut.
 * @param installPath The path to the installation directory.
 * @return void
 */
void FinishUninstall(const char* installPath) {
    Sleep(1000);
    RemoveDirectorySilently(installPath);
    RegDeleteKey(HKEY_LOCAL_MACHINE, "SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\SpotifyLinker");
    printf("SpotifyLinker has been fully uninstalled.\n");
    
    if (GetFileAttributes(installPath) != INVALID_FILE_ATTRIBUTES) {
        printf("Error: Failed to remove the installation directory: %s\n", installPath);
        char message[MAX_PATH + 255];
        snprintf(message, sizeof(message), "SpotifyLinker could not be completely removed. Please delete the remaining files manually. (%s)", installPath);
        MessageBox(NULL, message, "Uninstall Incomplete", MB_OK | MB_ICONWARNING);
    } else {
        char startMenuPath[MAX_PATH];
        if (SUCCEEDED(SHGetFolderPath(NULL, CSIDL_STARTMENU, NULL, 0, startMenuPath))) {
            strcat(startMenuPath, "\\Programs\\SpotifyLinker.lnk");
            DeleteFile(startMenuPath);
            printf("SpotifyLinker shortcut has been removed from the Start Menu.\n");
            MessageBox(NULL, "SpotifyLinker has been successfully uninstalled.", "Uninstall Complete", MB_OK | MB_ICONINFORMATION);
        }
    }
}

int main(int argc, char* argv[]) {
    char installPath[MAX_PATH] = {0};
    char appDataPath[MAX_PATH];
    char tempPath[MAX_PATH];
    char selfPath[MAX_PATH];

    if (argc > 1 && strcmp(argv[1], "--finish") == 0) {
        FinishUninstall(argv[2]);
        return 0;
    }

    if (SUCCEEDED(SHGetFolderPath(NULL, CSIDL_APPDATA, NULL, 0, appDataPath))) {
        strcat(appDataPath, "\\SpotifyLinker");
        RemoveDirectorySilently(appDataPath);
        printf("SpotifyLinker configuration has been removed.\n");
    }

    if (!GetInstallPath(installPath, sizeof(installPath))) {
        printf("SpotifyLinker is not installed on this system.\n");
        system("pause");
        return 1;
    }

    GetTempPath(MAX_PATH, tempPath);
    GetModuleFileName(NULL, selfPath, MAX_PATH);

    char tempUninstaller[MAX_PATH];
    snprintf(tempUninstaller, sizeof(tempUninstaller), "%stemp_uninstaller.exe", tempPath);

    if (CopyFile(selfPath, tempUninstaller, FALSE)) {
        char command[MAX_PATH * 3];
        snprintf(command, sizeof(command), "\"%s\" --finish \"%s\"", tempUninstaller, installPath);

        STARTUPINFO si = {sizeof(si)};
        PROCESS_INFORMATION pi;
        if (CreateProcess(NULL, command, NULL, NULL, FALSE, 0, NULL, NULL, &si, &pi)) {
            CloseHandle(pi.hProcess);
            CloseHandle(pi.hThread);
            printf("Uninstallation... Please wait.\n");
        } else {
            printf("Error while executing the uninstaller.\n");
            system("pause");
        }
    } else {
        printf("Error while copying the uninstaller.\n");
        system("pause");
    }

    return 0;
}
