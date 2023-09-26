Find-PackageProvider -Name 'Nuget' -ForceBootstrap -IncludeDependencies
Install-Script -Name Get-WindowsAutoPilotInfo -Force
powershell -ExecutionPolicy Unrestricted Get-WindowsAutoPilotInfo -OutputFile ("C:\" + ($env:computername) + "-AutopilotHWID.csv")
