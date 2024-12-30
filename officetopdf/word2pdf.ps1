# Set variables
$OfficeToPDF = "$PSScriptRoot\OfficeToPDF.exe"
$SourceDir = "$PSScriptRoot\投标文件"
$OutputDir = "$PSScriptRoot\pdf"
$ErrorLog = @()

Write-Output "Input folder path: $SourceDir"
Write-Output "Output folder path: $OutputDir"

# If old PDF directory exists, remove it and its contents
if (Test-Path $OutputDir) {
    Write-Output "Removing old PDF directory: $OutputDir"
    Remove-Item -Path $OutputDir -Recurse -Force
}

# Create output directory
Write-Output "Creating new PDF directory: $OutputDir"
New-Item -ItemType Directory -Path $OutputDir | Out-Null

# Define recursive function to process folders and convert files
function ConvertToPDF {
    param(
        [Parameter(Mandatory=$true, ValueFromPipeline=$true)]
        [string]$SourceFolder
    )

    Write-Output "Processing folder: $SourceFolder"

    # Get all .docx and .doc files in current folder
    $files = Get-ChildItem -LiteralPath $SourceFolder -Include *.docx, *.doc -File

    foreach ($file in $files) {
        Write-Output "Found file: $($file.FullName)"

        # Build output file path and name
        $relativePath = $file.FullName.Substring($SourceDir.Length)
        $outputFile = Join-Path -Path $OutputDir -ChildPath $relativePath.Replace(".docx", ".pdf").Replace(".doc", ".pdf")

        Write-Output "Output file path: $outputFile"

        # Ensure output folder exists
        $outputFolder = Split-Path -Path $outputFile
        if (-not (Test-Path $outputFolder)) {
            Write-Output "Creating output folder: $outputFolder"
            New-Item -ItemType Directory -Path $outputFolder | Out-Null
        }

        # Execute conversion
        Write-Output "Converting file: $($file.FullName) -> $outputFile"
        try {
            & $OfficeToPDF $file.FullName $outputFile /bookmarks
            if ($LASTEXITCODE -ne 0) {
                throw "Conversion failed"
            }
            Write-Output "Conversion complete: $($file.FullName) -> $outputFile"
        } catch {
            Write-Output "Error converting file: $($file.FullName)"
            $ErrorLog += "Error converting file: $($file.FullName) -> $outputFile"
            $ErrorLog += $_.Exception.Message
        }
    }

    # Recursively process subfolders
    $folders = Get-ChildItem -LiteralPath $SourceFolder -Directory
    foreach ($folder in $folders) {
        ConvertToPDF $folder.FullName
    }

    Write-Output "Folder processing complete: $SourceFolder"
}

# Call recursive function to start conversion
Write-Output "Starting conversion process..."
ConvertToPDF $SourceDir

Write-Output "Conversion complete!"

# Output error summary
if ($ErrorLog.Count -gt 0) {
    Write-Output "Errors encountered during conversion:"
    foreach ($error in $ErrorLog) {
        Write-Output $error
    }
} else {
    Write-Output "No errors encountered."
}
