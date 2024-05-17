# Nellus Place Bid

Login to Nellus and get a session token

Each minute it will loop through the list of items you want to bid on

It will get the item's end time

If it is at the last minute of that item's auction time, it will place a bid

The bid will be the max you have given for this item

Bonus:
* If there are multiple of the same items, loop through them as the auction closes and try to win
  just one.

## Test curl call
```
curl 'https://www.nellisauction.com/api/bids' --compressed -X POST -H 'User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:125.0) Gecko/20100101 Firefox/125.0' -H 'Accept: */*' -H 'Accept-Language: en-US,en;q=0.5' -H 'Accept-Encoding: gzip, deflate, br' -H 'Referer: https://www.nellisauction.com/p/Turtle-Beach-VelocityOne-Flight-Universal-Control-System---Xbox/28158447' -H 'sentry-trace: 5265aee88a884760abae7d80ecce5889-820a4fc02d38202d' -H 'baggage: sentry-environment=production,sentry-public_key=b61eb32f6d314323a9758b0f9c2dc18f,sentry-trace_id=5265aee88a884760abae7d80ecce5889' -H 'Content-Type: text/plain;charset=UTF-8' -H 'Origin: https://www.nellisauction.com' -H 'Connection: keep-alive' -H 'Cookie: _hp2_id.1530949394=%7B%22userId%22%3A%226298237846484060%22%2C%22pageviewId%22%3A%224248000194971377%22%2C%22sessionId%22%3A%228359260766406585%22%2C%22identity%22%3A%22335247%22%2C%22trackerVersion%22%3A%224.0%22%2C%22identityField%22%3Anull%2C%22isIdentified%22%3A1%2C%22oldIdentity%22%3Anull%7D; _ga_Z14LK6XFVL=GS1.1.1714854194.104.1.1714854355.35.0.2110276300; _ga=GA1.2.1077588269.1680055211; ap3c=IGQjm6v04uUxBNwFAGQjm6tCySscqjraLZkI4BE2ipeHLqGlAw; _fbp=fb.1.1680055211620.1687457433; __adroll_fpc=01bfe7516d68ab70bd390e8bd9ddfc0f-1680055211822; __ar_v4=LFQLVEFGUNHI5LHCJIWYHC%3A20240405%3A18%7CQSXTKNUYXNCWNFQAP2WPHK%3A20240416%3A126%7CXCWDW22TAVFONKHMZRMNJ5%3A20240416%3A126%7CEQNY52S66BH4VH6D3CIXQE%3A20240416%3A105%7CROHX3MYKRFDJBKQOP4VCKV%3A20240429%3A6; __shopping-location=eyJzaG9wcGluZ0xvY2F0aW9uIjp7ImlkIjoxLCJuYW1lIjoiTGFzIFZlZ2FzLCBOViJ9fQ%3D%3D.5%2Fa1O8WdIopRxccYrBEKJANvEtz2TUYr8e1T66SuEZE; _ga_W980Y9MV7E=GS1.2.1689178988.12.1.1689179314.60.0.0; _ga_Z14LK6XFVL=deleted; _ALGOLIA=anonymous-903c9f64-276c-4edf-85ef-36a5b329435f; _gcl_au=1.1.725496705.1711568089.1258129048.1714414584.1714414584; clientside-cookie=db826344c85a40cd4a131641d12fc27a21c0b5ac1db04949c8ab262cb00a136f7a58daa5c36b64fe3d8defb925ac63787bf9f214ee881ea076aaf621ae0f8652e9183e6e4cbf31f7d7c3c31c8ca3150c5dfc0f82ffca20af64a7e8e9be7cd3bff79b7a6f8decd5478f5ac66b9026f31e68df051ed25a33919b3a61d200111b4eadf8ee717edd271f20d49baaf20efddc310203c9afe9716cddc9da; _tt_enable_cookie=1; _ttp=-NiNE9r8P7uutYWpaQCYvi91pT9; __session=eyJ1c2VySWQiOjMzNTI0NywidXNlckF1dGhUb2tlbiI6ImV5SmhiR2NpT2lKSVV6STFOaUlzSW5SNWNDSTZJa3BYVkNKOS5leUpwWkNJNk16TTFNalEzTENKcFlYUWlPakUzTVRRME1UUTFPRFFzSW1WNGNDSTZNVGN4TnpBd05qVTROSDAub0owX0ptSGI1QThleURzQ1JaYndDWi1UM2w4ajBMTmlJUGtnTUlneXNwYyJ9.OqMWdhMHmYnc9FlX71Eh42rOw%2FPlF65IFU%2BSp73dLQw; __public=e30%3D.GcnILYfJMKY278FQnUClucHACfVuNPNrwhUHVleAYNQ; ap3pages=161; __navigation=eyJhdXRoUmVkaXJlY3QiOiIvIn0%3D.%2F%2FDloNKWkzcXKnazbtrGHl0vHeuuY%2FiSIu%2Bz%2FuNkiNM; _gid=GA1.2.898557541.1714773572; _hp2_ses_props.1530949394=%7B%22ts%22%3A1714854194926%2C%22d%22%3A%22www.nellisauction.com%22%2C%22h%22%3A%22%2F%22%7D; _gat=1; _rdt_uuid=1680055210654.58eb5c73-57da-416b-b3c0-f95d04186d00' -H 'Sec-Fetch-Dest: empty' -H 'Sec-Fetch-Mode: cors' -H 'Sec-Fetch-Site: same-origin' -H 'TE: trailers' --data-raw '{"productId":28158447,"bid":19}'
```





```
curl 'https://www.nellisauction.com/api/bids' --compressed -X POST 

-H 'User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:125.0) Gecko/20100101 Firefox/125.0' 

-H 'Accept: */*' -H 'Accept-Language: en-US,en;q=0.5' 

-H 'Accept-Encoding: gzip, deflate, br' 

-H 'Referer: https://www.nellisauction.com/p/Turtle-Beach-VelocityOne-Flight-Universal-Control-System---Xbox/28158447' 

-H 'sentry-trace: 5265aee88a884760abae7d80ecce5889-820a4fc02d38202d' 

-H 'baggage: sentry-environment=production,sentry-public_key=b61eb32f6d314323a9758b0f9c2dc18f,sentry-trace_id=5265aee88a884760abae7d80ecce5889' 

-H 'Content-Type: text/plain;charset=UTF-8'

 -H 'Origin: https://www.nellisauction.com' 
 
 -H 'Connection: keep-alive' 
 
 -H 'Cookie: _hp2_id.1530949394=%7B%22userId%22%3A%226298237846484060%22%2C%22pageviewId%22%3A%224248000194971377%22%2C%22sessionId%22%3A%228359260766406585%22%2C%22identity%22%3A%22335247%22%2C%22trackerVersion%22%3A%224.0%22%2C%22identityField%22%3Anull%2C%22isIdentified%22%3A1%2C%22oldIdentity%22%3Anull%7D; _ga_Z14LK6XFVL=GS1.1.1714854194.104.1.1714854355.35.0.2110276300; _ga=GA1.2.1077588269.1680055211; ap3c=IGQjm6v04uUxBNwFAGQjm6tCySscqjraLZkI4BE2ipeHLqGlAw; _fbp=fb.1.1680055211620.1687457433; __adroll_fpc=01bfe7516d68ab70bd390e8bd9ddfc0f-1680055211822; __ar_v4=LFQLVEFGUNHI5LHCJIWYHC%3A20240405%3A18%7CQSXTKNUYXNCWNFQAP2WPHK%3A20240416%3A126%7CXCWDW22TAVFONKHMZRMNJ5%3A20240416%3A126%7CEQNY52S66BH4VH6D3CIXQE%3A20240416%3A105%7CROHX3MYKRFDJBKQOP4VCKV%3A20240429%3A6; __shopping-location=eyJzaG9wcGluZ0xvY2F0aW9uIjp7ImlkIjoxLCJuYW1lIjoiTGFzIFZlZ2FzLCBOViJ9fQ%3D%3D.5%2Fa1O8WdIopRxccYrBEKJANvEtz2TUYr8e1T66SuEZE; _ga_W980Y9MV7E=GS1.2.1689178988.12.1.1689179314.60.0.0; _ga_Z14LK6XFVL=deleted; _ALGOLIA=anonymous-903c9f64-276c-4edf-85ef-36a5b329435f; _gcl_au=1.1.725496705.1711568089.1258129048.1714414584.1714414584; clientside-cookie=db826344c85a40cd4a131641d12fc27a21c0b5ac1db04949c8ab262cb00a136f7a58daa5c36b64fe3d8defb925ac63787bf9f214ee881ea076aaf621ae0f8652e9183e6e4cbf31f7d7c3c31c8ca3150c5dfc0f82ffca20af64a7e8e9be7cd3bff79b7a6f8decd5478f5ac66b9026f31e68df051ed25a33919b3a61d200111b4eadf8ee717edd271f20d49baaf20efddc310203c9afe9716cddc9da; _tt_enable_cookie=1; _ttp=-NiNE9r8P7uutYWpaQCYvi91pT9; __session=eyJ1c2VySWQiOjMzNTI0NywidXNlckF1dGhUb2tlbiI6ImV5SmhiR2NpT2lKSVV6STFOaUlzSW5SNWNDSTZJa3BYVkNKOS5leUpwWkNJNk16TTFNalEzTENKcFlYUWlPakUzTVRRME1UUTFPRFFzSW1WNGNDSTZNVGN4TnpBd05qVTROSDAub0owX0ptSGI1QThleURzQ1JaYndDWi1UM2w4ajBMTmlJUGtnTUlneXNwYyJ9.OqMWdhMHmYnc9FlX71Eh42rOw%2FPlF65IFU%2BSp73dLQw; __public=e30%3D.GcnILYfJMKY278FQnUClucHACfVuNPNrwhUHVleAYNQ; ap3pages=161; __navigation=eyJhdXRoUmVkaXJlY3QiOiIvIn0%3D.%2F%2FDloNKWkzcXKnazbtrGHl0vHeuuY%2FiSIu%2Bz%2FuNkiNM; _gid=GA1.2.898557541.1714773572; _hp2_ses_props.1530949394=%7B%22ts%22%3A1714854194926%2C%22d%22%3A%22www.nellisauction.com%22%2C%22h%22%3A%22%2F%22%7D; _gat=1; _rdt_uuid=1680055210654.58eb5c73-57da-416b-b3c0-f95d04186d00' 
 
 -H 'Sec-Fetch-Dest: empty' 
 
 -H 'Sec-Fetch-Mode: cors'
 
  -H 'Sec-Fetch-Site: same-origin' 
  
  -H 'TE: trailers' --data-raw '{"productId":28158447,"bid":19}'
```



## Posting a bid
I am already logged in and did a bid and copied the cURL in the browser:

```
curl 'https://www.nellisauction.com/api/bids' --compressed -X POST -H 'User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:125.0) Gecko/20100101 Firefox/125.0' -H 'Accept: */*' -H 'Accept-Language: en-US,en;q=0.5' -H 'Accept-Encoding: gzip, deflate, br' -H 'Referer: https://www.nellisauction.com/p/Thrustmaster-Racing-Wheel-TX-Servo-Base-for-Xbox-Series-X-S-One/28158068' -H 'sentry-trace: a4f579b37d4f4f70ba8e87d9967b8e24-bf858076a6c1fb23' -H 'baggage: sentry-environment=production,sentry-public_key=b61eb32f6d314323a9758b0f9c2dc18f,sentry-trace_id=a4f579b37d4f4f70ba8e87d9967b8e24' -H 'Content-Type: text/plain;charset=UTF-8' -H 'Origin: https://www.nellisauction.com' -H 'Connection: keep-alive' -H 'Cookie: _hp2_id.1530949394=%7B%22userId%22%3A%226298237846484060%22%2C%22pageviewId%22%3A%226431414796660460%22%2C%22sessionId%22%3A%228556576604245312%22%2C%22identity%22%3A%22335247%22%2C%22trackerVersion%22%3A%224.0%22%2C%22identityField%22%3Anull%2C%22isIdentified%22%3A1%2C%22oldIdentity%22%3Anull%7D; _ga_Z14LK6XFVL=GS1.1.1714860913.105.1.1714865035.60.0.1430690782; _ga=GA1.2.1077588269.1680055211; ap3c=IGQjm6v04uUxBNwFAGQjm6tCySscqjraLZkI4BE2ipeHLqGlAw; _fbp=fb.1.1680055211620.1687457433; __adroll_fpc=01bfe7516d68ab70bd390e8bd9ddfc0f-1680055211822; __ar_v4=LFQLVEFGUNHI5LHCJIWYHC%3A20240405%3A19%7CQSXTKNUYXNCWNFQAP2WPHK%3A20240416%3A132%7CXCWDW22TAVFONKHMZRMNJ5%3A20240416%3A132%7CEQNY52S66BH4VH6D3CIXQE%3A20240416%3A110%7CROHX3MYKRFDJBKQOP4VCKV%3A20240429%3A6; __shopping-location=eyJzaG9wcGluZ0xvY2F0aW9uIjp7ImlkIjoxLCJuYW1lIjoiTGFzIFZlZ2FzLCBOViJ9fQ%3D%3D.5%2Fa1O8WdIopRxccYrBEKJANvEtz2TUYr8e1T66SuEZE; _ga_W980Y9MV7E=GS1.2.1689178988.12.1.1689179314.60.0.0; _ga_Z14LK6XFVL=deleted; _ALGOLIA=anonymous-903c9f64-276c-4edf-85ef-36a5b329435f; _gcl_au=1.1.725496705.1711568089.275232904.1714861143.1714862902; clientside-cookie=db826344c85a40cd4a131641d12fc27a21c0b5ac1db04949c8ab262cb00a136f7a58daa5c36b64fe3d8defb925ac63787bf9f214ee881ea076aaf621ae0f8652e9183e6e4cbf31f7d7c3c31c8ca3150c5dfc0f82ffca20af64a7e8e9be7cd3bff79b7a6f8decd5478f5ac66b9026f31e68df051ed25a33919b3a61d200111b4eadf8ee717edd271f20d49baaf20efddc310203c9afe9716cddc9da; _tt_enable_cookie=1; _ttp=-NiNE9r8P7uutYWpaQCYvi91pT9; __public=e30%3D.GcnILYfJMKY278FQnUClucHACfVuNPNrwhUHVleAYNQ; ap3pages=166; __navigation=eyJhdXRoUmVkaXJlY3QiOiIvIn0%3D.%2F%2FDloNKWkzcXKnazbtrGHl0vHeuuY%2FiSIu%2Bz%2FuNkiNM; _gid=GA1.2.898557541.1714773572; __session=eyJ1c2VySWQiOjMzNTI0NywidXNlckF1dGhUb2tlbiI6ImV5SmhiR2NpT2lKSVV6STFOaUlzSW5SNWNDSTZJa3BYVkNKOS5leUpwWkNJNk16TTFNalEzTENKcFlYUWlPakUzTVRRNE5qSTVNRE1zSW1WNGNDSTZNVGN4TnpRMU5Ea3dNMzAuQzBSTXp4LXd0WTI3eXgxdE43OVN3R1Y0cGxRSGZEVHcwT3hiYUtjU2g4VSJ9.ioZKnQGlto2s6iPwH%2BrbjHXkU1b%2F6IjdDXcBJx51kyc; _hp2_ses_props.1530949394=%7B%22ts%22%3A1714863144591%2C%22d%22%3A%22www.nellisauction.com%22%2C%22h%22%3A%22%2Fdashboard%2Fauctions%2Fall%22%7D; _rdt_uuid=1680055210654.58eb5c73-57da-416b-b3c0-f95d04186d00' -H 'Sec-Fetch-Dest: empty' -H 'Sec-Fetch-Mode: cors' -H 'Sec-Fetch-Site: same-origin' -H 'TE: trailers' --data-raw '{"productId":28158068,"bid":23}'
```

## Placing bid minimum curl

```
curl 'https://www.nellisauction.com/api/bids' --compressed -X POST -H 'User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:125.0) Gecko/20100101 Firefox/125.0' -H 'Accept: */*'  --data-raw '{"productId":28158068,"bid":26}'  -H 'Cookie: __session=eyJ1c2VySWQiOjMzNTI0NywidXNlckF1dGhUb2tlbiI6ImV5SmhiR2NpT2lKSVV6STFOaUlzSW5SNWNDSTZJa3BYVkNKOS5leUpwWkNJNk16TTFNalEzTENKcFlYUWlPakUzTVRRNE5qSTVNRE1zSW1WNGNDSTZNVGN4TnpRMU5Ea3dNMzAuQzBSTXp4LXd0WTI3eXgxdE43OVN3R1Y0cGxRSGZEVHcwT3hiYUtjU2g4VSJ9.ioZKnQGlto2s6iPwH%2BrbjHXkU1b%2F6IjdDXcBJx51kyc;'
```
* This is working



## Login HTML
```html
<div class="w-full flex flex-col max-w-lg p-4 mx-auto justify-between self-stretch bg-white sm:p-6"><h1 class="text-headline-md font-bold leading-snug text-center mb-7">LOGIN</h1>

<form method="post" action="/login" id="login">
    <input type="hidden" name="__rvfInternalFormId" value="login">
    
    <div class="flex flex-col gap-4"><div class="__input-wrapper __input-fixed-label">
        <div class="flex w-full"><div class="__form-input-container">
            
            <input name="email" id="email" type="email" placeholder="Enter your email address" class="__form-input __input-text-input" autocomplete="off" value="">
            <label class="bg-white">Email address</label></div></div></div>
            
            <div class="__input-wrapper __input-fixed-label"><div class="flex w-full"><div class="__form-input-container">
                
                <input name="password" id="password" type="password" placeholder="Enter your password" class="__form-input __input-text-input __password-input" autocomplete="off" value="">
                
                <label class="bg-white">Password</label></div><button type="button" class="__password-eye"><svg width="22" height="20" fill="#000" xmlns="http://www.w3.org/2000/svg" class="__icon-base __password-eye-primary"><path d="M11.005 4.5c2.76 0 5 2.24 5 5 0 .65-.13 1.26-.36 1.83l2.92 2.92c1.51-1.26 2.7-2.89 3.43-4.75-1.73-4.39-6-7.5-11-7.5-1.4 0-2.74.25-3.98.7l2.16 2.16c.57-.23 1.18-.36 1.83-.36Zm-10-2.73 2.74 2.74A11.804 11.804 0 0 0 .005 9.5c1.73 4.39 6 7.5 11 7.5 1.55 0 3.03-.3 4.38-.84l.42.42 2.93 2.92 1.27-1.27L2.275.5l-1.27 1.27Zm5.53 5.53 1.55 1.55c-.05.21-.08.43-.08.65 0 1.66 1.34 3 3 3 .22 0 .44-.03.65-.08l1.55 1.55c-.67.33-1.41.53-2.2.53-2.76 0-5-2.24-5-5 0-.79.2-1.53.53-2.2Zm4.31-.78 3.15 3.15.02-.16c0-1.66-1.34-3-3-3l-.17.01Z"></path></svg></button></div></div></div><div class="flex justify-between items-center my-5 px-1"><div><button type="button" role="checkbox" aria-checked="true" data-state="checked" value="on" class="flex items-center gap-x-2 group" id="rememberMe"><svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 448 512" width="20" height="20" class="fill-secondary group-hover:fill-burgundy-700"><path d="M64 32C28.7 32 0 60.7 0 96V416c0 35.3 28.7 64 64 64H384c35.3 0 64-28.7 64-64V96c0-35.3-28.7-64-64-64H64zM337 209L209 337c-9.4 9.4-24.6 9.4-33.9 0l-64-64c-9.4-9.4-9.4-24.6 0-33.9s24.6-9.4 33.9 0l47 47L303 175c9.4-9.4 24.6-9.4 33.9 0s9.4 24.6 0 33.9z"></path></svg><label for="rememberMe" class="cursor-pointer">Keep me logged in</label></button><input type="checkbox" aria-hidden="true" name="rememberMe" style="transform: translateX(-100%); position: absolute; pointer-events: none; opacity: 0; margin: 0px; width: 165.45px; height: 24px;" tabindex="-1" value="on" checked=""></div><a href="/forgot-password"><span class="font-semibold text-secondary hover:text-[#973333]">Forgot Password ?</span></a></div><button type="submit" class="__primary-button __primary-button-full-width">LOGIN</button>
</form></div>

```