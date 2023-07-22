@REM double-clickable run vintt4. need to input your conda env where you installed the program
@echo off

set CONDA_ENV=web

cd %~dp0
call conda activate %CONDA_ENV%
uvicorn vintt4_main:app --host 0.0.0.0 --port 4301 --log-level warning