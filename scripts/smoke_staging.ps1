param(
  [string]$BaseUrl = "http://localhost:8000"
)

$HealthUrl = "$BaseUrl/health/"

try {
  $response = Invoke-WebRequest -Uri $HealthUrl -UseBasicParsing -TimeoutSec 10
  if ($response.StatusCode -ne 200) {
    Write-Error "Healthcheck failed with status $($response.StatusCode)"
    exit 1
  }

  Write-Host "Healthcheck OK"
  Write-Host $response.Content
  exit 0
} catch {
  Write-Error "Smoke test failed: $_"
  exit 1
}
