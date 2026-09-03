@echo off
REM ===========================================================================
REM  build.bat  --  one-click build for paper.tex
REM  Runs the full LuaLaTeX + Biber chain that TeXStudio keeps skipping:
REM      lualatex -> biber -> lualatex -> lualatex
REM  Double-click this file, or run it from a terminal in this folder.
REM ===========================================================================
setlocal EnableExtensions
cd /d "%~dp0"

set "JOB=paper"

REM --- make sure the MiKTeX tools are reachable even if PATH is incomplete ---
where lualatex >nul 2>nul
if errorlevel 1 set "PATH=%LOCALAPPDATA%\Programs\MiKTeX\miktex\bin\x64;%PATH%"
where lualatex >nul 2>nul
if errorlevel 1 (
  echo(
  echo   ERROR: lualatex not found. Install / repair MiKTeX, or add its
  echo          "miktex\bin\x64" folder to your PATH, then try again.
  echo(
  pause
  exit /b 1
)

echo(
echo ===========================================================================
echo   Building %JOB%.pdf   ^(LuaLaTeX + Biber^)
echo ===========================================================================

echo(
echo [1/4] lualatex (first pass)...
lualatex -interaction=nonstopmode -halt-on-error -synctex=1 "%JOB%.tex" >nul
if errorlevel 1 goto :texfail

echo [2/4] biber (resolve citations)...
biber "%JOB%"
if errorlevel 1 goto :biberfail

echo [3/4] lualatex (second pass)...
lualatex -interaction=nonstopmode -halt-on-error -synctex=1 "%JOB%.tex" >nul
if errorlevel 1 goto :texfail

echo [4/4] lualatex (final pass)...
lualatex -interaction=nonstopmode -halt-on-error -synctex=1 "%JOB%.tex" >nul
if errorlevel 1 goto :texfail

echo(
REM --- warn about any leftover undefined references ---
findstr /C:"There were undefined references" /C:"Citation" /C:"Reference " "%JOB%.log" | findstr /I "undefined" >nul
if not errorlevel 1 (
  echo   NOTE: the log still mentions undefined references. Details:
  findstr /I "undefined" "%JOB%.log"
  echo(
)

for %%F in ("%JOB%.pdf") do set "PDFSIZE=%%~zF"
echo ===========================================================================
echo   DONE.  %JOB%.pdf  (%PDFSIZE% bytes)
echo ===========================================================================
echo   Opening the PDF. If it will not rebuild next time, close the PDF
echo   viewer first (Adobe locks the file; SumatraPDF and browsers do not).
echo(
start "" "%JOB%.pdf"
"%SystemRoot%\System32\timeout.exe" /t 3 /nobreak >nul 2>nul
exit /b 0

:texfail
echo(
echo ---------------------------------------------------------------------------
echo   LaTeX ERROR.  Last 40 lines of %JOB%.log:
echo ---------------------------------------------------------------------------
powershell -NoProfile -Command "if (Test-Path '%JOB%.log') { Get-Content '%JOB%.log' -Tail 40 }"
echo(
pause
exit /b 1

:biberfail
echo(
echo ---------------------------------------------------------------------------
echo   BIBER ERROR.  Contents of %JOB%.blg:
echo ---------------------------------------------------------------------------
powershell -NoProfile -Command "if (Test-Path '%JOB%.blg') { Get-Content '%JOB%.blg' }"
echo(
pause
exit /b 1
