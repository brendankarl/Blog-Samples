# Authenticate
$ClientId = "" 
$AuthTenant = ""
$GraphScopes = "LearningProvider.ReadWrite","LearningContent.ReadWrite.All"
Connect-MgGraph -ClientId $clientId -TenantId $authTenant -Scopes $graphScopes -UseDeviceAuthentication

# Return Learning Providers
$uri = "https://graph.microsoft.com/beta/employeeExperience/learningProviders"
$lps = Invoke-MgGraphRequest -Method GET -uri $uri
$lps.value

# Add a Learning Provider
$params = @{
        "displayName" = "Brendan's Tech Ramblings"
        "squareLogoWebUrlForDarkTheme" = "https://brendankarl.files.wordpress.com/2021/05/cropped-myavatar.png"
        "longLogoWebUrlForDarkTheme" = "https://brendankarl.files.wordpress.com/2021/05/cropped-myavatar.png"
        "squareLogoWebUrlForLightTheme" = "https://brendankarl.files.wordpress.com/2021/05/cropped-myavatar.png"
        "longLogoWebUrlForLightTheme" = "https://brendankarl.files.wordpress.com/2021/05/cropped-myavatar.png"
        "isEnabled" = $true
        "loginWebUrl" = ""
}

$uri = "https://graph.microsoft.com/beta/employeeExperience/learningProviders"
Invoke-MgGraphRequest -Method POST -uri $uri -Body $params 

# Retrieve the ID of a custom Learning Provider
$uri = "https://graph.microsoft.com/beta/employeeExperience/learningProviders"
$lps = Invoke-MgGraphRequest -Method GET -uri $uri
$lpid = $lps.value.id

# Update a Learning Provider
$params = @{
        "displayName" = "Acme"
        "squareLogoWebUrlForDarkTheme" = "https://brendankarl.files.wordpress.com/2021/05/cropped-myavatar.png"
        "longLogoWebUrlForDarkTheme" = "https://brendankarl.files.wordpress.com/2021/05/cropped-myavatar.png"
        "squareLogoWebUrlForLightTheme" = "https://brendankarl.files.wordpress.com/2021/05/cropped-myavatar.png"
        "longLogoWebUrlForLightTheme" = "https://brendankarl.files.wordpress.com/2021/05/cropped-myavatar.png"
        "isEnabled" = $true
        "loginWebUrl" = "http://localhost"
}

$uri = "https://graph.microsoft.com/beta/employeeExperience/learningProviders/" + $lpid
Invoke-MgGraphRequest -Method PATCH -uri $uri -Body $params 

# Remove a Learning Provider
$uri = "https://graph.microsoft.com/beta/employeeExperience/learningProviders/" + $lpid
Invoke-MgGraphRequest -Method DELETE -uri $uri

# Add Learning Content
$params = @{
        "title" = "Burger Tax - using an Azure Function to Stay Healthy!"
        "description" = "Find out how I used the Starling Bank developer API and an Azure Function to tax myself whenever I buy junk food!"
        "contentWebUrl" = "https://youtu.be/z909tjuDKlY"
        "thumbnailWebUrl" = "https://brendankarl.files.wordpress.com/2022/09/maxresdefault-1.jpg"
        "languageTag" = "en-us"
        "numberOfPages" = "1"
        "format" = "Video"
        "createdDateTime" = "2022-07-16"
}

$uri = "https://graph.microsoft.com/beta/employeeExperience/learningProviders/" + $lpid + "/learningContents(externalId='BurgerTax')"
Invoke-MgGraphRequest -Method PATCH -uri $uri -Body $params 

# Remove Learning Content
$uri = "https://graph.microsoft.com/beta/employeeExperience/learningProviders/" + $lpid + "/learningContents(externalId='BurgerTax')"
Invoke-MgGraphRequest -Method DELETE -uri $uri

# List Learning Content
$uri = "https://graph.microsoft.com/beta/employeeExperience/learningProviders/" + $lpid + "/LearningContents"
$content = Invoke-MgGraphRequest -Method GET -uri $uri
$content.value
