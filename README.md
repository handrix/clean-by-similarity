基于文本相似度的新文本据清洗脚本
===
这东西写的太**了，毫无效率可言，决定于本周，即2017年9月9日重构。
====
安装
---
```shell
// elasticsearch
// on mac
brew install elasticsearch
// on centos/ubuntu
sudo yum/apt-get install elasticsearch

// python lib
pip install -r requestments.txt
```

使用
--
```shell
python3 shell.py -i /path/to/input/json/

```

备注
---
- 不再赘述每个参数的含义，具体使用方法请
```shell
python3 shell.py -h
```
