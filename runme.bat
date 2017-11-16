@echo off
set exnum=%1
call python test_script.py %exnum% > ex%exnum%.log
exit