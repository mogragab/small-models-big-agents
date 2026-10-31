@echo off
REM ===========================================================================
REM  build.bat  --  build less-is-more.tex (ACM acmart, pdfLaTeX + BibTeX)
REM      pdflatex -> bibtex -> pdflatex -> pdflatex
REM ===========================================================================
setlocal EnableExtensions
cd /d "%~dp0"
set "JOB=less-is-more"

where pdflatex >nul 2>nul
if errorlevel 1 set "PATH=%LOCALAPPDATA%\Programs\MiKTeX\miktex\bin\x64;%PATH%"

echo [1/4] pdflatex (first pass)...
pdflatex -interaction=nonstopmode -synctex=1 "%JOB%.tex" >nul
echo [2/4] bibtex...
bibtex "%JOB%"
echo [3/4] pdflatex (second pass)...
pdflatex -interaction=nonstopmode -synctex=1 "%JOB%.tex" >nul
echo [4/4] pdflatex (final pass)...
pdflatex -interaction=nonstopmode -synctex=1 "%JOB%.tex" >nul

echo(
findstr /C:"There were undefined references" "%JOB%.log" >nul && echo   NOTE: undefined references remain.
for %%F in ("%JOB%.pdf") do echo   DONE.  %JOB%.pdf  (%%~zF bytes)
start "" "%JOB%.pdf"
