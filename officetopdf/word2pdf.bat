@echo off
setlocal EnableDelayedExpansion

:: Set variables
set "OfficeToPDF=%~dp0OfficeToPDF.exe"
set "SourceDir=%~dp0投标文件"
set "OutputDir=%~dp0pdf"
set "ErrorLog=%temp%\ErrorLog.txt"

echo Input folder path: %SourceDir%
echo Output folder path: %OutputDir%

:: If old PDF directory exists, remove it and its contents
if exist "%OutputDir%" (
    echo Removing old PDF directory: %OutputDir%
    rmdir /s /q "%OutputDir%"
)

:: Create output directory
echo Creating new PDF directory: %OutputDir%
mkdir "%OutputDir%"

:: Define function to convert files
:ConvertToPDF
set "SourceFolder=%~1"
echo Processing folder: %SourceFolder%

:: Get all .docx and .doc files in current folder
for %%f in ("%SourceFolder%\*.docx" "%SourceFolder%\*.doc") do (
    echo Found file: %%f

    :: Build output file path and name
    set "relativePath=%%~f"
    set "relativePath=!relativePath:%SourceDir%=!"
    set "outputFile=%OutputDir%!relativePath:.docx=.pdf!"
    set "outputFile=!outputFile:.doc=.pdf!"

    echo Output file path: !outputFile!

    :: Ensure output folder exists
    set "outputFolder=!outputFile!\.."
    if not exist "!outputFolder!" (
        echo Creating output folder: !outputFolder!
        mkdir "!outputFolder!"
    )

    :: Execute conversion
    echo Converting file: %%f -> !outputFile!
    "%OfficeToPDF%" "%%f" "!outputFile!" /bookmarks
    if errorlevel 1 (
        echo Error converting file: %%f
        echo Error converting file: %%f -> !outputFile! >> "%ErrorLog%"
        echo Conversion failed >> "%ErrorLog%"
    ) else (
        echo Conversion complete: %%f -> !outputFile!
    )
)

:: Process subfolders
for /d %%d in ("%SourceFolder%\*") do (
    if exist "%%d\*" (
        call :ConvertToPDF "%%d"
    )
)

echo Folder processing complete: %SourceFolder%
goto :eof

:: Call function to start conversion
echo Starting conversion process...
call :ConvertToPDF "%SourceDir%"

echo Conversion complete!

:: Output error summary
if exist "%ErrorLog%" (
    echo Errors encountered during conversion:
    type "%ErrorLog%"
) else (
    echo No errors encountered.
)

:: Clean up
if exist "%ErrorLog%" del "%ErrorLog%"

endlocal
