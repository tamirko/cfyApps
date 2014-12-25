param (
    [string]$name = $(throw "-name is required."),
    [string]$ip = $(throw "-ip is required.")
)

Write-Host `n adding host $name with $ip