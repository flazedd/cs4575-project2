# Get all Dockerfiles
Get-ChildItem -Filter "*.Dockerfile" | ForEach-Object {
    $imageName = $_.BaseName  # Extracts the filename without extension
    Write-Host "Running image: $imageName with GPU support"
    # Run the container interactively to display its output
    docker run --gpus all --volume $PSScriptRoot\volume:/app:rw --interactive $imageName
    # docker run --gpus all --volume "${PWD}\volume:/app:rw" --interactive $imageName
}