#!/bin/bash

# zip codes: 78204, 75001, 76006, 78015, 78052, 78504, 77007, 78736, 79424, 77573, 79707

# Make the cURL request and pipe the output to jq
response=$(curl -s 'https://www.heb.com/_next/data/d705541efbe361849bbe86a9e25faf10935f27b3/store-locations.json?address=79707&page=2' --compressed -H 'User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:130.0) Gecko/20100101 Firefox/130.0' -H 'Accept: */*' -H 'Accept-Language: en-US,en;q=0.5' -H 'Accept-Encoding: gzip, deflate, br, zstd' -H 'Referer: https://www.heb.com/store-locations?address=78204&page=1' -H 'x-nextjs-data: 1' -H 'Connection: keep-alive' -H 'Cookie: visid_incap_2302070=7JknsoW3TUGO8oS29d4vfBmP4GYAAAAAQUIPAAAAAACIxSpxTTqiKtD+cNdkXIcm; incap_ses_173_2302070=ToVyUExbISFyIBb62J5mAg/X4GYAAAAATdkFBFHKmApEuU/Y04I5Mw==; HEB_AMP_DEVICE_ID=h-5e7e0e72-731c-423d-b62f-8eb5d07aa899; AWSALB=2MgfGdttf+T23lpp++Req2bTapYA2tTa98uUPCGFd+bQCVhJJB7rk7mZYQ6DGOaqxpXZIWbx8lNvNmqSJvkpaJGC8D3IIgeJzQVwmC4bPXnWaeOGSrkm8mrjl/zX; AWSALBCORS=2MgfGdttf+T23lpp++Req2bTapYA2tTa98uUPCGFd+bQCVhJJB7rk7mZYQ6DGOaqxpXZIWbx8lNvNmqSJvkpaJGC8D3IIgeJzQVwmC4bPXnWaeOGSrkm8mrjl/zX; DYN_USER_ID=18917909691; DYN_USER_CONFIRM=6974ef810870a2f08b7c935addf38edc; USER_SELECT_STORE=false; CURR_SESSION_STORE=92; sessionContext=curbside; JSESSIONID=o5-yrGvweJHuv3jyrRieVsWT2XTRax4OzZgSFJvz; sst=hs:sst:LSGXErN2pelr1ziSw0uOy; sst.sig=odMXCM86qgpTHDnx8bGWVfnJZEvBZknQ092DJ2OIILg; AMP_760524e2ba=JTdCJTIyZGV2aWNlSWQlMjIlM0ElMjJoLTVlN2UwZTcyLTczMWMtNDIzZC1iNjJmLThlYjVkMDdhYTg5OSUyMiUyQyUyMnNlc3Npb25JZCUyMiUzQTE3MjYwMTExNTQwMDIlMkMlMjJvcHRPdXQlMjIlM0FmYWxzZSUyQyUyMmxhc3RFdmVudFRpbWUlMjIlM0ExNzI2MDExNzAyMzU3JTJDJTIybGFzdEV2ZW50SWQlMjIlM0E1NSUyQyUyMnBhZ2VDb3VudGVyJTIyJTNBMCU3RA==; AMP_MKTG_760524e2ba=JTdCJTdE; _ga_WKSH6HYPT4=GS1.1.1726011154.2.1.1726011704.0.0.0; _ga=GA1.1.733746279.1725992733; reese84=3:6H4nGN/k7vmBzdcPU8Sexw==:aT+pj0bnIVFg7fCSDRz3ymBdkgm1xgKUXLCnFe7/H/4sQW62vObNyZb5fqR5QWA/TjNj+u7pr677kNInzyyBgC+NbCJVjLvKK9refeyJJwYPYaj+slpl6qkLNjHaxEnr1klC2BeK8duFQvg2fEMlXbnZxHIwMPsNLbmHwoE4ZAKNt705IqsqSmN3IycC6Cx9DRI8+fpvArLOfivaKnZ3CgN/c+yMe4eOLaI0yCq+L5VqF2CW71+WsvLSwAJjBaFjZA1QPuTKJmhXe7JkcUwkQpNoZf/Q/sdzyoCj06qrAXROA/CyW3LDLfrtvkX5yCkk5PVQdPByA18zWCn2ZdFK/o80RpzuStgYtv4gl9+juHheCpoZ6dwzR5LVsa4rI2xh6/H1zFy7coLI197WH5CMRLFyK1Z/KATE27EW9ZaMo38+e+l5o+a5JnsIg50EMQzXfyJBQ8CgUl3QCPjGLJKy9EGUCnOKqts7V70lwVINRPw=:tuhXvBS1k7Ywq+8kJb7NjNei5hK8Si4FLEXNj2N3iRU=; OptanonConsent=isGpcEnabled=0&datestamp=Tue+Sep+10+2024+16%3A40%3A04+GMT-0700+(Pacific+Daylight+Time)&version=202405.2.0&browserGpcFlag=0&isIABGlobal=false&hosts=&consentId=d948b516-c432-4159-8050-1fd4e933811b&interactionCount=1&isAnonUser=1&landingPath=NotLandingPage&groups=C0004%3A1&AwaitingReconsent=false; _gcl_au=1.1.494519603.1725992734' -H 'Sec-Fetch-Dest: empty' -H 'Sec-Fetch-Mode: cors' -H 'Sec-Fetch-Site: same-origin' -H 'Priority: u=0' -H 'TE: trailers')
data=$(echo "$response" | jq -r '.pageProps.currentPageStores')

# Print the extracted data
# echo "$data"

# semi working 
echo $data | jq -r '.[] | .store.name, .store.storeNumber, .store.address.streetAddress, .store.address.locality, .store.address.region, .store.address.postalCode'

# for i in "$(echo $data | jq -r .[])"; do
#     name=$(echo $i | jq -r '.store.name, .store.storeNumber')
#     # storeNumber=$(echo $i | jq -r .store.storeNumber)
#     # streetAddress=$(echo $i | jq -r .store.address.streetAddress)
#     # input_string="$name, $storeNumber, $streetAddress |"
#     # output_string=$(echo "$input_string" | tr -d '\n')
#     # echo "$output_string"
#     # echo "---"
#     # exit 0
#     echo $name
# done