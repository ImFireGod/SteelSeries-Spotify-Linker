#include <windows.h>
#include <iostream>
#include <string>

#define DEBUG_PREFIX "[DEBUG] "

/**
 * Retrieves the directory path of the executable.
 * @return The absolute path to the directory containing the executable.
 */
std::string GetExecutablePath()
{
    char buffer[MAX_PATH];
    GetModuleFileName(NULL, buffer, MAX_PATH);
    std::string path(buffer);
    return path.substr(0, path.find_last_of("\\/"));
}

/**
 * Checks if a file exists at the given path.
 * @param path The file path to check.
 * @return True if the file exists, false otherwise.
 */
bool FileExists(const std::string& path)
{
    DWORD attrib = GetFileAttributes(path.c_str());
    return (attrib != INVALID_FILE_ATTRIBUTES && !(attrib & FILE_ATTRIBUTE_DIRECTORY));
}

/**
 * Launches the Python script from the virtual environment.
 * @param debugMode If true, allows output logging; otherwise, runs silently.
 * @return Handle to the created process, or NULL if creation failed.
 */
HANDLE LaunchPythonScript(bool debugMode)
{
    STARTUPINFO si;
    PROCESS_INFORMATION pi;
    ZeroMemory(&si, sizeof(si));
    si.cb = sizeof(si);
    ZeroMemory(&pi, sizeof(pi));

    // Get paths for the Python executable and script
    std::string exePath = GetExecutablePath();
    std::string pythonPath = exePath + "\\venv\\Scripts\\python.exe";
    std::string pythonScriptPath = exePath + "\\main.py";

    // Check if Python exists in the virtual environment
    if (!FileExists(pythonPath)) {
        MessageBox(NULL, "Can't find python.exe in venv folder. Please verify your installation.", "Error", MB_ICONERROR);
        return NULL;
    }

    // Construct the command to execute
    std::string command = "\"" + pythonPath + "\" \"" + pythonScriptPath + "\"";
    DWORD creationFlags = debugMode ? 0 : CREATE_NO_WINDOW;

    // Launch the Python script
    if (!CreateProcess(
        NULL,
        (LPSTR)command.c_str(),
        NULL, NULL,
        FALSE,
        creationFlags,
        NULL,
        exePath.c_str(),
        &si, &pi)) 
    {
        if (debugMode) std::cerr << DEBUG_PREFIX << "Error: Can't start python.\n";
        return NULL;
    }

    CloseHandle(pi.hThread);
    return pi.hProcess; // Return the process handle
}

/**
 * Windows entry point for the application.
 * Detects if "--debug" mode is enabled and runs the Python script accordingly.
 */
int WINAPI WinMain(HINSTANCE hInstance, HINSTANCE hPrevInstance, LPSTR lpCmdLine, int nCmdShow)
{
    std::string args(lpCmdLine);
    bool debugMode = (args.find("--debug") != std::string::npos);

    if (debugMode) {
        AllocConsole();
        freopen("CONOUT$", "w", stdout);
        freopen("CONOUT$", "w", stderr);
        std::cout << DEBUG_PREFIX << "Activated\n";
    }

    HANDLE hProcess = LaunchPythonScript(debugMode);
    
    if (hProcess != NULL) {
        // Wait for the Python process to finish
        WaitForSingleObject(hProcess, INFINITE);
        CloseHandle(hProcess);
    }

    if (debugMode) system("pause");
    return 0;
}