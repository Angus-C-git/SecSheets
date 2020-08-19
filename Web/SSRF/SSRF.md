# Server Side Request Forgery {SSRF}

# Overview


## Anatomy Of A Modern Web Application

![SSRF Diagram](./images/SSRF_diaggram.png)

## SSRF Conceputally

+ A SSRF exploit abuses the nature of web application systems, like most sytems, to be hardened to external traffic but relatively unprotected internally
+ Exploiting a SSRF vulnerability allows an attacker to leverage the trusted nature of the internally facing web application against itself in order to retrive and access resources which ordinarly they could not reach without privillaged authentication or internal network access

## Sources Of SSRF Vulnrabilities

+ SSRF vulnrabilities typically arise when web applications allow users to include URL or URI based content as part of a function of the application
+ At a less abstract level SSRF vulnrabilities can arise when: 
	+ Blacklists and whitelists are used to protect against SSRF
	+ The web application has a open redirect vulnrability
	+ The web application has a XXE vulnrability 

# SSRF Vectors

## SSRF Against the Host

## SSRF Against Internal Systems

## SSRF Via Referer Header

## Blind SSRF

# SSRF WAF && Filter Bypasses

## Blacklists

## Whitelists

## Open Redirects
