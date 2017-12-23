@echo off
set exnum=%1
set id=%2
set cfile=%3
call "%VS140COMNTOOLS%/VsDevCmd.bat"
cd "%HOMEDRIVE%%HOMEPATH%/Desktop/C_exercises/%exnum%/%id%"
echo COMPILING: %cfile%
cl %cfile%
