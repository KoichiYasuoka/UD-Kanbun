import setuptools
with open("README.md","r") as r:
  long_description=r.read()
URL="https://github.com/KoichiYasuoka/UD-Kanbun"

import subprocess
try:
  d=subprocess.check_output(["swig","-version"])
  install_requires=["ufal.udpipe>=1.2.0","mecab-python3>=0.996.3"]
except:
  install_requires=["ufal.udpipe>=1.2.0","mecab-python3==0.996.2"]
try:
  d=subprocess.check_output(["mecab-config","--libs-only-L"])
  install_requires=["ufal.udpipe>=1.2.0","fugashi>=0.1.8"]
except:
  pass

setuptools.setup(
  name="udkanbun",
  version="1.6.3",
  description="Tokenizer POS-tagger and Dependency-parser for Classical Chinese",
  long_description=long_description,
  long_description_content_type="text/markdown",
  url=URL,
  author="Koichi Yasuoka",
  author_email="yasuoka@kanji.zinbun.kyoto-u.ac.jp",
  license="MIT",
  keywords="udpipe mecab nlp",
  packages=setuptools.find_packages(),
  install_requires=install_requires,
  python_requires=">=3.6",
  package_data={
    "udkanbun":["./*.js","./ud-kanbun.udpipe","./mecab-kanbun/*"],
  },
  entry_points={
    "console_scripts":["udkanbun=udkanbun.cli:main"],
  },
  classifiers=[
    "License :: OSI Approved :: MIT License",
    "Programming Language :: Python :: 3",
    "Operating System :: OS Independent",
    "Topic :: Text Processing :: Linguistic",
  ],
  project_urls={
    "ud-kanbun":"https://corpus.kanji.zinbun.kyoto-u.ac.jp/gitlab/Kanbun/ud-kanbun",
    "Source":URL,
    "Tracker":URL+"/issues",
  }
)
