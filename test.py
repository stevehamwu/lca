#!/usr/bin/env python 3.5
# -*- coding:utf-8 -*- 
import jieba as jb
import jieba.analyse
import math
import sys
str = '《窃读记》的作者的作品'
words = jb.cut(str)
for word in words:
	print(word)