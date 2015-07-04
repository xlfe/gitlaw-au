# gitlaw

New Zealand has done it : https://github.com/wombleton/gitlaw-nz
Germany has done it : http://bundestag.github.io/gesetze/

Ever wondered what it would look like if Australian Legislation was on Github?

Well - gitlaw-au is my 2015 #govhack project

### Howto print the text of some legislation

This only works with the new stuff in DocX format - pretty useless as the majority appears to be either PDF, DOC, or RTF

```
import legislation
l = legislation.Legislation('C2015A00061') #Biosecurity Act 2015
l.text()
```


