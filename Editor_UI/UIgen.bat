@echo off
for /r %%i in (*.ui) do (D:\software\anaconda\Scripts\pyuic5.exe %%i -o UI_%%~ni.py)
