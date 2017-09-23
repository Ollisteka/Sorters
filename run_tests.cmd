@echo off
coverage erase
coverage run -m unittest discover
coverage report -m
pause