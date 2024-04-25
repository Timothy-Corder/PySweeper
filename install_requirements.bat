@ECHO off

python --version 2>NUL
if errorlevel 1 goto:install_python

:: Once done, exit the batch file -- skips executing the errorNoPython section
goto:install_program

:install_python
python
goto :install_program

:install_program
echo Creating mine_env... (Python environment)
python -m venv mine_env

echo Entering environment...
call mine_env/scripts/activate.bat

echo Installing Tkinter...
pip install -r requirements.txt

echo @ECHO off >> run.bat
echo call mine_env/scripts/activate.bat >> run.bat
echo python main.py >> run.bat

echo Successfully created run.bat. Only use that to open the program from now on.
ren install_requirements.bat installed.true
call run.bat