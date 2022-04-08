$i = 0
while ($i -eq 0)
{
    $Time = Get-Date
    $SpeedTest = speedtest-cli --simple
    $Time.ToString() + "," + $SpeedTest[0].split(" ")[1] + "," + $SpeedTest[1].split(" ")[1] + "," + $SpeedTest[2].split(" ")[1]  >> "/etc/speedtest/logs/SpeedTest.csv"
    Start-Sleep -Seconds 300
}
