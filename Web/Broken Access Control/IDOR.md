# Insecure Direct Object Refrences (IDOR)

## Overview

IDOR vulnerabilities are a common class of access control vulnerability in web applications which occur when the web application uses client controlled parameters/inputs to refer to objects directly.

IDOR vulnerabilities can often lead to exposure of private or restricted information, or the ability to modify unintended records in the database.


## Breakdown of IDOR Vulnerability


![IDOR Diagram](./images/IDOR_Diagram.png)



Here the web application uses a vulnerable configuration to retrive a users private profile data via their profile id (14), which is passed as a parameter in the request sent to the backend. Since the server makes no attempt to validate if the user attempting to access the resource is the legitimate user an attacker could simply enumerate the profile_overview parameter to leak user data.   