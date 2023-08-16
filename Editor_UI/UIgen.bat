@echo off
for /r %%i in (*.ui) do (D:\software\anaconda\Scripts\pyuic5.exe %%i -o UI_%%~ni.py)
setlocal enabledelayedexpansion
for /r %%i in (*.py) do (set file_list=!file_list! %%i)
D:\software\anaconda\Scripts\pylupdate5.exe !file_list! -ts zh_CN.ts
exit
