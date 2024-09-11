#!/bin/bash

# zip codes: 78204, 75001, 76006, 78015, 78052, 78504, 77007, 78736, 79424, 77573, 79707, 78557, 78566, 76701

# Make the cURL request and pipe the output to jq
response=$(curl -s curl 'https://www.heb.com/_next/data/b1e8f2d7917755260e55b9feb41c78deeca29925/store-locations.json?address=76701&page=13' --compressed -H 'User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:130.0) Gecko/20100101 Firefox/130.0' -H 'Accept: */*' -H 'Accept-Language: en-US,en;q=0.5' -H 'Accept-Encoding: gzip, deflate, br, zstd' -H 'Referer: https://www.heb.com/store-locations?address=79707&page=1' -H 'x-nextjs-data: 1' -H 'Connection: keep-alive' -H 'Cookie: visid_incap_2302070=7JknsoW3TUGO8oS29d4vfBmP4GYAAAAAQUIPAAAAAACIxSpxTTqiKtD+cNdkXIcm; incap_ses_173_2302070=NMjYEqePZHwUrYL/2J5mApbb4WYAAAAAm0w3Vh51DViR9yiIEZTnDQ==; HEB_AMP_DEVICE_ID=h-5e7e0e72-731c-423d-b62f-8eb5d07aa899; AWSALB=7xF5W9DWwoOxL8NLGMn1I/fzsI9hvUQ1q7n7BdQFFOuRDosnd71DVHLBPZJPhrLijtX3DI9rffLr1PgixJB0c8thhYh7YL4s9/r9igw8ZhJhGsiaafnMG0ljqNzC; AWSALBCORS=7xF5W9DWwoOxL8NLGMn1I/fzsI9hvUQ1q7n7BdQFFOuRDosnd71DVHLBPZJPhrLijtX3DI9rffLr1PgixJB0c8thhYh7YL4s9/r9igw8ZhJhGsiaafnMG0ljqNzC; DYN_USER_ID=18920109639; DYN_USER_CONFIRM=81117ae9dbcdb3db23123480032af38a; USER_SELECT_STORE=false; CURR_SESSION_STORE=92; sessionContext=curbside; JSESSIONID=YS8MORkX_uSYUiqTmSgcy8pN8xeeQYPKqDImXCn5; sst=hs:sst:LSGXErN2pelr1ziSw0uOy; sst.sig=odMXCM86qgpTHDnx8bGWVfnJZEvBZknQ092DJ2OIILg; AMP_760524e2ba=JTdCJTIyZGV2aWNlSWQlMjIlM0ElMjJoLTVlN2UwZTcyLTczMWMtNDIzZC1iNjJmLThlYjVkMDdhYTg5OSUyMiUyQyUyMnNlc3Npb25JZCUyMiUzQTE3MjYwNzgzMDEwMjIlMkMlMjJvcHRPdXQlMjIlM0FmYWxzZSUyQyUyMmxhc3RFdmVudFRpbWUlMjIlM0ExNzI2MDc4MzAxNDUyJTJDJTIybGFzdEV2ZW50SWQlMjIlM0EyMTElMkMlMjJwYWdlQ291bnRlciUyMiUzQTAlN0Q=; AMP_MKTG_760524e2ba=JTdCJTIycmVmZXJyZXIlMjIlM0ElMjJodHRwcyUzQSUyRiUyRnd3dy5nb29nbGUuY29tJTJGJTIyJTJDJTIycmVmZXJyaW5nX2RvbWFpbiUyMiUzQSUyMnd3dy5nb29nbGUuY29tJTIyJTdE; _ga_WKSH6HYPT4=GS1.1.1726078303.5.0.1726078303.0.0.0; _ga=GA1.1.733746279.1725992733; reese84=3:s/AOW9MvVXeJ0JQ3R32ujA==:XOZN73jcIbyWzMJ+EVFZUEwGzzLZMGwaYvS/Z5cgeWdzbeZnR7J5U6F7clHNlye6kDLwifsHO9FrGX+i62DVWZLIkxs+m25SbIjYEUjMbvEWmRJR552VQM3ZsIjehuaVdvq8s18EVb0M3hy5SWsS+vTxuxk0vfX1iu3m/8/cFAIqdM+R5DCbkg4yAwoURq3bmmm0YpDVe8IiGGWmvKCRLtIL8zo/0nZuIursk2PP0j5idUda6TgSzwRfZ+vhBEuvHNd37052azKNdhAX/Aul1p/Nlg2NApKWRvEnEWkRr/1L9jgwUc+l5x3WB8Rd8yVx8qGZZSXY2pPFwjS3cDOWcOP17bImgUJiFnsRcXsdwUjNR7IDTSKu8x3oJ6WTGWI+uqHCt4mXe+QjL8clQHNxPv5vk+uIUEuIL/BQStILE3jNW7U2REYtL+KtShpIGckPodfdqrO2tFfQs9t25WNFyf2Stifx8/HCFNhVbgZFg9w=:t1S+z74MpIlXKDkwayl7vGUy+lpDQlBtKgeNFN+DYIY=; OptanonConsent=isGpcEnabled=0&datestamp=Wed+Sep+11+2024+10%3A28%3A02+GMT-0700+(Pacific+Daylight+Time)&version=202405.2.0&browserGpcFlag=0&isIABGlobal=false&hosts=&consentId=d948b516-c432-4159-8050-1fd4e933811b&interactionCount=1&isAnonUser=1&landingPath=NotLandingPage&groups=C0004%3A1&AwaitingReconsent=false; _gcl_au=1.1.494519603.1725992734; incap_ses_415_2302070=+cCcUSVSlHZaLbJjcmDCBec84WYAAAAApuqf1WqG/QQHqQ8XB7DWWg==' -H 'Sec-Fetch-Dest: empty' -H 'Sec-Fetch-Mode: cors' -H 'Sec-Fetch-Site: same-origin' -H 'Priority: u=0')
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