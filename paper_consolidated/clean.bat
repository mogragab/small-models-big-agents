@echo off
REM ===========================================================================
REM  clean.bat  --  delete LaTeX build artefacts (keeps paper.pdf and sources)
REM ===========================================================================
setlocal EnableExtensions
cd /d "%~dp0"

echo Cleaning build artefacts in "%CD%" ...

for %%E in (aux bcf bbl blg log out run.xml fls fdb_latexmk synctex.gz toc lof lot) do (
  if exist "paper.%%E" del /q "paper.%%E"
)
if exist "sections\*.aux" del /q "sections\*.aux"
if exist "partials\*.aux" del /q "partials\*.aux"

echo Done. (paper.pdf, paper.tex, bibliography.bib and figures were kept.)
"%SystemRoot%\System32\timeout.exe" /t 2 /nobreak >nul 2>nul
exit /b 0
