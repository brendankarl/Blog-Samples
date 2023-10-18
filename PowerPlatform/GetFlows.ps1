$FilePath = "D:\FlowsExport.csv"
$Flows = Get-AdminFlow
"Name" + "," + "Enabled" + "," + "Connectors" | Out-File $FilePath

ForEach ($Flow in $Flows)
{
    $FlowInfo = Get-AdminFlow -FlowName $Flow.FlowName -EnvironmentName $Flow.EnvironmentName
    $Connectors = $FlowInfo.Internal.properties.connectionReferences
    $ConnectorDetails = ""
    $Connectors.PSObject.Properties | ForEach {
         $ConnectorDetails += $_.Value.DisplayName + " | "
    }
    ($Flow.DisplayName.Replace(","," ")) + "," + $Flow.Enabled + "," + $ConnectorDetails | Out-File $FilePath -Append
}
