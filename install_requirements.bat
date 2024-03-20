@ECHO off

python -m venv mine_env

call mine_env/scripts/activate.bat
pip install -r requirements.txt

echo @ECHO off >> run.bat
echo call mine_env/scripts/activate.bat >> run.bat
echo python main.py >> run.bat