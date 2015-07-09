# gitlaw

Ever wondered what it would look like if Australian Legislation was available in git / Github?

* [New Zealand has done it](https://github.com/wombleton/gitlaw-nz)
* [Germany has done it](http://bundestag.github.io/gesetze/)

gitlaw-au is my 2015 #govhack project

I didn't quite make it for GovHack.... oh well!

### Status

[x] Get a list of all current acts and their ComLawID [acts_current.txt](https://github.com/xlfe/gitlaw-au/blob/master/acts_current.txt)
[x] Get a list of all the RTF/DOC/DOCx versions and volumes of those acts [details_current.json](https://github.com/xlfe/gitlaw-au/blob/master/details_current.txt)
[x] Download all the relevant RTF/DOC/DOCx files [Amazon S3](https://s3.amazonaws.com/gitlaw-au/gitlaw-au-current-2015-07-05.tar.gz)
[ ] Extract structure of documents and convert to Markdown (in progress)
[ ] Access historical / series of act for history

### Howto print the text of some legislation

This only works with the new stuff in DocX format - pretty useless as the majority appears to be either PDF, DOC, or RTF

```
import legislation
l = legislation.Legislation('C2015A00061') #Biosecurity Act 2015
l.text()
```


