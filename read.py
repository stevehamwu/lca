#!/usr/bin/env python 
# -*- coding:utf-8 -*- 
with open('ir.txt', 'r', encoding='utf8') as f:
	text = f.readlines()
	print(text[1])