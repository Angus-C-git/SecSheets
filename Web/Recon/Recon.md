Web Application: Enumeration/Recon
============================

## Overview

+ Recon and enumeration is about getting a bigger picture of a target
+ Recon and enumeration are critical prerequisites to getting a successful exploit
+ Knowing the technologies the target employees allows an attacker to eliminate false positives, more accurately test for vulnerabilities and saves time in the long run

## Passive Recon

### Target Validation/Identification

#### WHOIS

+ Grab whois record for target

`whois domain.com`

#### nslookup

+ Translate domain names into IP addresses

`nslookup domain.com`

#### dnsrecon

+ DNS record enumeration, subdomain enumeration

`dnsrecon -d domain.com`

### Subdomain Enumeration

#### dig

+ DNS walk, DNS records

`dig domain.com any`

#### Nmap

##### Basic Scan

`nmap domain.com`

##### Server Finger Printing

`nmap -p 80,443 -A t4 (target_ip)`

#### Sublist3r

+ Subdomain discovery, Subdomain bruteforce, OSINT discovery

`python sublist3r.py -d domain.com`

#### Bluto

+ Domain enumeration, api enumeration

`bluto -d domain.com`

#### [crt.sh](https://crt.sh/)

+ Certificate search


### Fingerprinting

+ Nmap
+ Wappalyzer {Browser Extension}
+ BuiltWith {Browser Extension}
+ Netcat

### Data Breaches

+ Does target related material appear in data breaches
+ [haveibeenpawned](https://haveibeenpwned.com/)
+ [weleakinfo](http://weleakinfo.com/) ~ Seized by Feds
+ [hunter.io](https://hunter.io/)

### Maintaining Scope

#### URL Regex For Burp

In Scope:

`.*\.domain\.com$`

Exclusion:

+ Remove from scope option in burp settings

## Active Recon

### Spidering/Crawling

#### Burp Suite

+ Domain -> Scan -> Crawl

#### Zap Proxy

+ Quickstart -> Domain -> Attack

#### Manual Spidering/Crawling

+ Move through the website as a developer
+ How can you break it?

### Basic Vulnerability Scanning

#### Nikto Vuln Scanner

+ On real world targets will rarely find anything

`nikto -h https://www.domain.com`

### SSL/TLS Verification/Validation

~ Note: Very rare

+ Check the integrity of SSL/TLS ciphers

#### Nmap Script

`nmap -p 443 --script=ssl-enum-ciphers (target_ip)`

### Directory Discovery

#### Dirbuster

`dirb domain wordlist`


#### Manual Discovery

+ Common dirs
+ Target specific directories, guess possible strings

#### Source Inclusion/Console Data

+ Developer data
+ Source comments
+ Console.logs
+ JavaScript function exposure
+ Removed functionality

#### DRY && Wet Principles

+ Broken form validation
+ Broken front end checks

#### UI Bypasses

+ Editing front-end DOM elements to bypass UI barriers
	+ `pattern={1-9}` -> delete
	+ `type="email"` -> `type="text"`
+ Forging/editing requests

