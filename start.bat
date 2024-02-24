if exist %~dp0\venv\Scripts\activate (
    %~dp0\venv\Scripts\activate && python %~dp0\main.py
) else (
    python %~dp0\main.py
)