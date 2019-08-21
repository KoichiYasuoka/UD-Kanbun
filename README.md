[![Current PyPI packages](https://badge.fury.io/py/udkanbun.svg)](https://pypi.org/project/udkanbun/)

# UD-Kanbun

Tokenizer, POS-Tagger, and Dependency-Parser for Classical Chinese Texts (漢文), working on [Universal Dependencies](https://universaldependencies.org/format.html).

## Basic usage

```py
>>> import udkanbun
>>> lzh=udkanbun.load()
>>> s=lzh("不入虎穴不得虎子")
>>> print(s)
# text = 不入虎穴不得虎子
1	不	不	ADV	v,副詞,否定,無界	Polarity=Neg	2	advmod	_	Gloss=not|SpaceAfter=No
2	入	入	VERB	v,動詞,行為,移動	_	0	root	_	Gloss=enter|SpaceAfter=No
3	虎	虎	NOUN	n,名詞,主体,動物	_	4	nmod	_	Gloss=tiger|SpaceAfter=No
4	穴	穴	NOUN	n,名詞,固定物,地形	Case=Loc	2	obj	_	Gloss=cave|SpaceAfter=No
5	不	不	ADV	v,副詞,否定,無界	Polarity=Neg	6	advmod	_	Gloss=not|SpaceAfter=No
6	得	得	VERB	v,動詞,行為,得失	_	2	parataxis	_	Gloss=get|SpaceAfter=No
7	虎	虎	NOUN	n,名詞,主体,動物	_	8	nmod	_	Gloss=tiger|SpaceAfter=No
8	子	子	NOUN	n,名詞,人,関係	_	6	obj	_	Gloss=child|SpaceAfter=No

>>> t=s[1]
>>> print(t.id,t.form,t.lemma,t.upos,t.xpos,t.feats,t.head.id,t.deprel,t.deps,t.misc)
1 不 不 ADV v,副詞,否定,無界 Polarity=Neg 2 advmod _ Gloss=not|SpaceAfter=No
```

`udkanbun.load()` has only one option `udkanbun.load(MeCab=False)`.  By default, the UD-Kanbun pipeline uses MeCab for tokenizer and POS-tagger, then uses UDPipe for dependency-parser. With the option `MeCab=False` the pipeline uses UDPipe for all through the processing.


## Installation

Binary wheel is available for Linux, and is installed by default when you use `pip`:

```sh
pip install udkanbun
```

## Author

Koichi Yasuoka (安岡孝一)

## References

* 安岡孝一: 四書を学んだMeCab＋UDPipeはセンター試験の漢文を読めるのか, 東洋学へのコンピュータ利用, 第30回研究セミナー (2019年3月8日), pp.3-110.
