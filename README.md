# gitlaw

Ever wondered what it would look like if Australian Legislation was on Github?

Well - gitlaw-au is my 2015 #govhack project

### Howto print the text of some legislation

```
import legislation
l = legislation.Legislation('C2015A00061') #Biosecurity Act 2015
l.text()
```
