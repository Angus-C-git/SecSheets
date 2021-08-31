# Server Side Request Forgery (SSRF)

Server Side Request Forgery (SSRF) is a exploit class which attacks the underlying host and surrounding internal infrastructure of a web application. When exploited it may give an attacker the ability to make requests as if they were come from one of the internal services, which may additionally allow the attacker to view/modify critical and protected data as well as move laterally through the internal network.

### Anatomy Of A Web Application

{{< image ref="images/SSRF_Diagram.png" >}}

### SSRF Conceptually

+ A SSRF exploit abuses the nature of web application systems, like most systems, to be hardened to external traffic but relatively unprotected internally
+ Exploiting a SSRF vulnerability allows an attacker to leverage the trusted nature of the internally facing web application against itself in order to retrieve and access resources on their behalf, which ordinarily they could not reach without privileged authentication or internal network access
+ Additionally it may be possible to utilise the web application to move laterally through the internal network to other infrastructure resulting in potential RCE

### Sources Of SSRF Vulnerabilities

+ SSRF vulnerabilities typically arise when web applications allow users to include URL or URI based content as part of a function of the application
+ At a less abstract level SSRF vulnerabilities can arise when: 
	+ Blacklists and whitelists are used to protect against SSRF
	+ The web application has a open redirect vulnerability
	+ The web application has a XXE vulnerability 

## Tooling

+ [SSRFmap](https://github.com/swisskyrepo/SSRFmap)

## SSRF Vectors

### SSRF Against the Host

+ Ultimately all web applications run on some kind of hardware at their core
+ From here layers of software build up to the web application that users interact with
+ However those lower layers do not always drop away from the user access level meaning that software running at a lower level can still be interacted with through the web application
+ It is this residual or unintended exposure of vestigial software layers which lead to host based SSRF vulnerabilities

#### Layers of a modern Web Application

{{< image ref="images/WebApp_Host_Diagram.png" >}}

#### Approach

+ To perform this kind of SSRF attack and attacker attempts to have the host fetch resources on their behalf exploiting the fact that the host is inherently trusted as a 'privileged actor'
+ For example if an attacker where to attempt to access a admin page through the front end web application in a standard fashion without authenticating the web application returns an admin login panel
+ However if an attacker can induce the web applications host itself to access the admin page the attacker will be presented with the admin dashboard

#### Finding Host Based SSRF Vectors

+ Whenever a web application makes a request to itself using a full URL path it may be possible to replay a modified version of the request to get an SSRF exploit

```
POST /product/stock HTTP/1.0
Content-Type: application/x-www-form-urlencoded
Content-Length: 118

stockApi=http://stock.weliketoshop.net:8080/product/stock/check%3FproductId%3D6%26storeId%3D1 
```  
~Request From Portswigger Lab~

+ Attacker replaces the `stockApi` parameter in the request body with `localhost` to access the admin page via the hosts perspective

```
POST /product/stock HTTP/1.0
Content-Type: application/x-www-form-urlencoded
Content-Length: 118

stockApi=http://localhost/admin 
```  

+ Additionally, host based SSRF may be found anywhere fully qualified  URLs are used to access or include resources
	+ Profile images via URLs
	+ Embedded content via URLs

#### General Payloads

`http://localhost/resource_from_host_perspective`

`http://127.0.0.1/resource_from_host_perspective`

`http://127.1/resource_from_host_perspective`

### SSRF Against Internal Systems

+ SSRF attacks against other hosts on the internal network exploit the trusted relationship between systems in a private network
+ In a SSRF against other internal systems an attacker attempts to access another host on the internal network as the web servers host machine

#### Approach

+ An attacker attempts to learn the internal network topology of a web applications backend
+ This may be done through a vulnerability chain which allows for internal network scanning like a XSS vulnerability or command injection
+ Or via enumerating the subnet range of the internal network
+ If an attacker receives a response on a particular IP they have likely discovered a internal host at that location

#### Finding Internal Systems SSRF

+ Similarly to host based SSRF an attacker looks for places within the web application where fully qualified urls are used to access and fetch resources
+ An attacker then replaces these requests with the private IP address of a known, guessed or enumerated host on the internal network
+ Since the internal host may not return a response that the web server understands in a way that allows it to display a meaningful response this kind of SSRF may be blind

## SSRF WAF && Filter Bypasses

+ If the web application attempts to prevent SSRF vectors via filtering or WAF rules it may be possible to circumvent these defenses using one or a combination of the work around bellow

### Blacklists

+ Where the web application runs requests against a list of ban strings or regex patterns
	+ `localhost`
	+ `127.`
	+ `::`

#### DNS Resolution to localhost

`http://localtest.me/`

#### Decimal

`http://21307064433/`

#### Hexadecimal

`http://0x7f000001/`

#### Octal

`http://0177.0.0.01/`

#### All IPs

`http://0.0.0.0/`

#### IPv6

`http://0:0:0:0:0:0:0:1`

### Whitelists

+ Where the web application only allows URLs which match a list of strings or regex patterns
	+ `https://the.domain.com`
	+ `https://125.63`

#### @ Bypass

`https://expected-host@localhost/`

#### URL Fragment

`https://localhost#expected-host`

### Open Redirects

+ If the web application contains an open redirect vulnerability it maybe be possible to leverage it to develop a SSRF exploit
+ An sufficient open redirect vulnerability would mean that even if the application is hardened against SSRF based vectors they can be negated by abusing the trust of the API 'host' that handles redirection

#### Approach


+ Consider a web application like an online shop which allows a user to cycle through products using a fully qualified URL to point to the next item but which also contains a redirection

`http://weliketoshop.net/product/nextProduct?currentProductId=1&path=/product?productId=2`

+ In this case the path parameter is vulnerable to an open redirect vulnerability which allows the attack to specify an internal IP address as the value of the path parameter

`http://weliketoshop.net/product/nextProduct?currentProductId=1&path=http://10.10.0.10/admin`

+ If an attacker submits this request with this modification the web application will make a trusted request to `10.10.0.10/admin` on behalf of the attacker

```
POST /product/stock HTTP/1.0
Content-Type: application/x-www-form-urlencoded
Content-Length: 118

stockApi=http://weliketoshop.net/product/nextProduct?currentProductId=6&path=http://10.10.0.10/admin 
```

~ Credits to portswiggers SSRF lab for the sample web application ~

## Resources

+ [Portswigger SSRF Labs](https://portswigger.net/web-security/ssrf)
+ [DZ Zone Open redirects](https://dzone.com/articles/what-is-an-open-redirection-vulnerability-and-how)
