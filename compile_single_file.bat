@echo off
set exnum=%1
set id=%2
set cfile=%3
call "C:/Program Files (x86)/Microsoft Visual Studio 14.0/Common7/Tools/VsDevCmd.bat"
cd "C:/Users/noamg/Desktop/C_exercises/%exnum%/%id%"
echo COMPILING: %cfile%
cl %cfile%
