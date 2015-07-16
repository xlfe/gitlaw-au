# gitlaw-au

Ever wondered what it would look like if Australian Legislation was available in git / Github?

* [New Zealand has done it](https://github.com/wombleton/gitlaw-nz)
* [Germany has done it](http://bundestag.github.io/gesetze/)

gitlaw-au is my 2015 #govhack project

I didn't quite make it for GovHack.... oh well!

### Browse current acts in Markdown (As of 5 July 2015)

[A](https://github.com/xlfe/gitlaw-au/blob/master/acts/current/a/)
[B](https://github.com/xlfe/gitlaw-au/blob/master/acts/current/b/)
[C](https://github.com/xlfe/gitlaw-au/blob/master/acts/current/c/)
[D](https://github.com/xlfe/gitlaw-au/blob/master/acts/current/d/)
[E](https://github.com/xlfe/gitlaw-au/blob/master/acts/current/e/)
[F](https://github.com/xlfe/gitlaw-au/blob/master/acts/current/f/)
[G](https://github.com/xlfe/gitlaw-au/blob/master/acts/current/g/)
[H](https://github.com/xlfe/gitlaw-au/blob/master/acts/current/h/)
[I](https://github.com/xlfe/gitlaw-au/blob/master/acts/current/i/)
[J](https://github.com/xlfe/gitlaw-au/blob/master/acts/current/j/)
[K](https://github.com/xlfe/gitlaw-au/blob/master/acts/current/k/)
[L](https://github.com/xlfe/gitlaw-au/blob/master/acts/current/l/)
[M](https://github.com/xlfe/gitlaw-au/blob/master/acts/current/m/)
[N](https://github.com/xlfe/gitlaw-au/blob/master/acts/current/n/)
[O](https://github.com/xlfe/gitlaw-au/blob/master/acts/current/o/)
[P](https://github.com/xlfe/gitlaw-au/blob/master/acts/current/p/)
[Q](https://github.com/xlfe/gitlaw-au/blob/master/acts/current/q/)
[R](https://github.com/xlfe/gitlaw-au/blob/master/acts/current/r/)
[S](https://github.com/xlfe/gitlaw-au/blob/master/acts/current/s/)
[T](https://github.com/xlfe/gitlaw-au/blob/master/acts/current/t/)
[U](https://github.com/xlfe/gitlaw-au/blob/master/acts/current/u/)
[V](https://github.com/xlfe/gitlaw-au/blob/master/acts/current/v/)
[W](https://github.com/xlfe/gitlaw-au/blob/master/acts/current/w/)
[X](https://github.com/xlfe/gitlaw-au/blob/master/acts/current/x/)
[Y](https://github.com/xlfe/gitlaw-au/blob/master/acts/current/y/)
[Z](https://github.com/xlfe/gitlaw-au/blob/master/acts/current/z/)

### Status

Text is extracted, but there's still some weird formatting and additional style info,
and still missing much of the structure (no table conversion is attempted)

- [x] Get a list of all current acts and their ComLawID [acts_current.txt](https://github.com/xlfe/gitlaw-au/blob/master/src/acts_current.txt)
- [x] Get a list of all the RTF/DOC/DOCx versions and volumes of those acts [details_current.json](https://github.com/xlfe/gitlaw-au/blob/master/src/details_current.txt)
- [x] Download all the relevant RTF/DOC/DOCx files [Amazon S3](https://s3.amazonaws.com/gitlaw-au/gitlaw-au-current-2015-07-05.tar.gz)
- [ ] Extract structure of documents and convert to Markdown (in progress)
 - [x] Read DOCx format and extract indent and font sizes
 - [x] Convert these to markdown indents and heading size
 - [ ] Extract table structures
 - [ ] Write to markdown using historical git commit based on date legislation came into force
- [ ] Access historical / series of act for history


### Files

* [spider.py](https://github.com/xlfe/gitlaw-au/blob/master/src/spider.py) Crawl legislation by year and get the ComLawID
* [download.py](https://github.com/xlfe/gitlaw-au/blob/master/src/download.py) Get the legislation detail form the ComLawID
* [convert.py](https://github.com/xlfe/gitlaw-au/blob/master/src/convert.py) The actual conversion to Markdown (messy!)


