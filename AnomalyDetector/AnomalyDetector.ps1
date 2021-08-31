$JSON = @"
{ 
    "series": [
    ],
   "maxAnomalyRatio": 0.25,
   "sensitivity": 95,
   "granularity": "hourly"
  }
"@
$NonJSON = $JSON | ConvertFrom-Json

$Output = Get-Content ./SpeedTestAnomaly.csv
Foreach ($Line in $Output)
{
  $DL = $Line.split(",")[2]  
  $Date = $Line.split(",")[0]
  $Add = New-Object -TypeName psobject -Property @{timestamp = $Date;value = $DL}
  $NonJSON.series += $Add
}

$JSON = $NonJSON | ConvertTo-Json

$AnomalyURI = "https://PREFIX.cognitiveservices.azure.com/anomalydetector/v1.0/timeseries/entire/detect"
$APIKey = "KEY"

$Result = Invoke-RestMethod -Method Post -Uri $AnomalyURI -Header @{"Ocp-Apim-Subscription-Key" = $apiKey} -Body $JSON -ContentType "application/json" -ErrorAction Stop

$i = 0
Foreach ($Anomaly in $Result.isAnomaly)
{
  if ($Anomaly -eq "True") 
  {
    Write-Host "Expected Value: " $Result.expectedValues[$i] "Actual Value: " $NonJSON.series[$i] -ForegroundColor Red
  }
  else 
  {
    Write-Host "Expected Value: " $Result.expectedValues[$i] "Actual Value: " $NonJSON.series[$i] -ForegroundColor Green
  }
  
  $i ++
}
