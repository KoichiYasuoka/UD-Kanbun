import setuptools
with open("README.md","r") as r:
  long_description=r.read()
URL="https://github.com/KoichiYasuoka/UD-Kanbun"

setuptools.setup(
  name="udkanbun",
  version="0.9.1",
  description="Tokenizer POS-tagger and Dependency-parser for Classical Chinese",
  long_description=long_description,
  long_description_content_type="text/markdown",
  url=URL,
  author="Koichi Yasuoka",
  author_email="yasuoka@kanji.zinbun.kyoto-u.ac.jp",
  license="MIT",
  keywords="udpipe mecab nlp",
  packages=setuptools.find_packages(),
  install_requires=["ufal.udpipe>=1.2.0","mecab-python3>=0.996"],
  python_requires=">=3.6",
  package_data={
    "udkanbun":["./ud-kanbun.udpipe","./mecab-kanbun/*"],
  },
  classifiers=[
    "License :: OSI Approved :: MIT License",
    "Programming Language :: Python :: 3",
    "Operating System :: OS Independent",
    "Natural Language :: Classical Chinese",
    "Topic :: Text Processing :: Linguistic",
  ],
  project_urls={
    "UDPipe":"http://ufal.mff.cuni.cz/udpipe",
    "ud-kanbun":"https://corpus.kanji.zinbun.kyoto-u.ac.jp/gitlab/Kanbun/ud-kanbun",
    "Source":URL,
    "Tracker":URL+"/issues",
  }
)
