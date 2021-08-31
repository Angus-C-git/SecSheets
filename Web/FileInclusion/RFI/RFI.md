# Remote File Inclusion (RFI)

Remote file inclusion is a category of exploit where an attacker can manipulate a web application into including a remote file. This file may be uploaded by the attacker or included through some other means like a URL or a rich text like form or 'sandbox'.


## Arbitrary File Upload

+ RFI from an arbitrary file upload is a typical exploitation strategy that occurs when a web application    
  + Does not perform backend validation of file uploads 
  + Employees simplistic whitelisting 
  + Employees simplistic blacklisting
  + Employees front end validation
+ RFI can often lead to 
  + Remote code execution 
  + XXS
  + XXE
  + Phishing vectors

### Filter Bypasses

+ These may be used in naming files to be uploaded or included in a web application
+ A typical payload within these files may be a webshell or command injection payload

`general_file.payloadFileType.ExpectedFileType`

`profile_image.php.jpeg`

`profile_image.php.png`

`profile_image.php%20.png`