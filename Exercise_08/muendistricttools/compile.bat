@echo off
rem — initialize OSGeo4W/Qt5/Python environments
call "C:\OSGeo4W\bin\o4w_env.bat"
call "C:\OSGeo4W\bin\qt5_env.bat"
call "C:\OSGeo4W\bin\py3_env.bat"
@echo on

rem — compile the Qt resource file into Python
pyrcc5 -o resources.py resources.qrc
