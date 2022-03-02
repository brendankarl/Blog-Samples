using namespace System.Net

# Input bindings are passed in via param block.
param($Request, $TriggerMetadata)

$PAT = $Env:PAT # The Personal Access Token (PAT) is stored as an Application Setting (named "PAT") within the function app
$Headers = @{Authorization="Bearer " + $PAT} 
$BaseURL = "https://api.starlingbank.com/api/v2/"

# Retrieve default account uid (I'm being lazy, I have a single account)
function Get-AccountUID {
    $Response = Invoke-WebRequest -Uri ($BaseURL + "accounts") -Method Get -Headers $Headers
    $AccountUID = $Response | ConvertFrom-Json
    return $AccountUID.accounts[0].accountUid

}
# Retrieve the space uid for the first space (I'm being lazy, I have a single Savings Space)
function Get-SpaceUID {
    $Response = Invoke-WebRequest -Uri ($BaseURL + "account" + "/" + (Get-AccountUID) + "/savings-goals") -Method Get -Headers $Headers
    $Spaces = $Response | ConvertFrom-Json
    return $Spaces.savingsGoalList[0].savingsGoalUid
}

Write-Host "PowerShell HTTP trigger function processed a request."

# If the merchant looks like McDonalds then invoke the burger tax!
if ($Request.body.content.counterPartyName -like "mcdonalds*")
    {
        Write-Host "You spent money at " $($Request.body.content.counterPartyName) ", invoking burger tax..."
        # Calculate the burger tax - this is 20% of the transaction amount (rounded up to the nearest penny)
        $TaxAmount = [math]::ceiling($Request.body.content.amount.minorUnits * 0.20)
        $Body = "Burger tax:" + " " + "£" + ($TaxAmount /100)
        Write-Host $Body
        # Create the JSON body for the transaction
        $JSON = @"
{
    "amount": {
      "currency": "GBP",
      "minorUnits": $TaxAmount
    }
  }
"@
        # Transfer the burger tax calculated to the space returned by Get-SpaceUID
        $Transfer = Invoke-WebRequest -Uri ($BaseURL + "account/" + (Get-AccountUID) + "/savings-goals/" + (Get-SpaceUID) + "/add-money/" + ((New-Guid).Guid)) -Method Put -ContentType "application/json" -Headers $Headers -Body $JSON
    }
# It's not McDonalds.....so all is good!
else 
    {
        $Body = "You spent money at " + $($Request.body.content.counterPartyName)
        Write-Host $Body
    }

# Associate values to output bindings by calling 'Push-OutputBinding'.
Push-OutputBinding -Name Response -Value ([HttpResponseContext]@{
    StatusCode = [HttpStatusCode]::OK
    Body = $Body
})
