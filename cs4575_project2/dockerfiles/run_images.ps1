# Get all Dockerfiles
Get-ChildItem -Filter "*.Dockerfile" | ForEach-Object {
    $imageName = $_.BaseName  # Extracts the filename without extension
    Write-Host "Running image: $imageName with GPU support"
    # Run the container interactively to display its output
    docker run --gpus all -it $imageName
}