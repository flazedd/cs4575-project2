Get-ChildItem -Filter "*.Dockerfile" | ForEach-Object {
    $dockerfile = $_.FullName
    $imageName = $_.BaseName  # Extracts filename without extension
    docker build -t $imageName -f $dockerfile .
}
