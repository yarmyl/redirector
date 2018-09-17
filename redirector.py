#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from sys import stdin
import re
import time
import argparse
import os
import inspect

"""Парсим аргументы"""
def createParser ():
	parser = argparse.ArgumentParser()
	parser.add_argument('--url', nargs='?') #url для редиректа
	return parser

"""Класс дерева поиска"""
class TreeSearch:
	__arr = []
	def __init__(self, file):
		file_desc = open(file, 'r')
		dom_list = []
		for dom in file_desc:
			dom_list.append(dom[:-1].split('.'))
		file_desc.close()
		self.__arr = recursion(dom_list)
	def __del__(self):
		pass
	def get(self):
		return self.__arr
	def search(self, str):
		slov = 0
		for dom in str.split('.')[::-1]:
			slov = self.__arr.get(dom) if not slov else slov.get(dom)
			if type(slov) == list:
				if not slov:
					return 1
			elif type(slov) == dict:
				if not slov:
					return 1
			elif type(slov) == str:
				return 1
		return 0

"""Рекурсия для инициализации словаря"""
def recursion(dom):
	i = 0
	res = {}
	if type(dom) == list and len(dom) > 0: 
		if type(dom[0]) == list and len(dom[0]) > 0:
			temp = dom[i]
			ind = temp.pop(0)
			temp = [temp]
			while i+1 < len(dom):
				i += 1
				if ind == dom[i][0]:
					buff = dom[i]
					ind = buff.pop(0)
					temp.append(buff)
				else:
					res.update({ind: recursion(temp)})
					temp = dom[i]
					ind = temp.pop(0)
					temp = [temp]
			res.update({ind: recursion(temp)})
		else:
			temp = dom
			ind = temp.pop(0)
			if temp:
				res.update({ind: recursion(temp)})
			else:
				res = ind
	else:
		res = []
	return res

def main():
	parser = createParser()
	namespace = parser.parse_args()
	url = namespace.url if namespace.url else "http://127.0.0.1/"
	redirect_url = "302:" + url
	dom_file = get_script_dir() + 'dom.list'
	url_file = get_script_dir() + 'url.list'
	white_list_file = get_script_dir() + 'white_dom.list'
	while 1:
		hold_time = time.time()
		d = TreeSearch(dom_file)
		w = TreeSearch(white_list_file)
		deny_http = open(url_file, 'r')
		deny_list = []
		for line in deny_http:
			deny_list.append(line[0:-1])
		deny_http.close()
		while hold_time + 60 * 10 > time.time():
			try:
				str = input()
			except:
				return 0
			if (str != ""):
				url = str.split(' ', 1)[0]
				if (re.match('http://', url)):
					dom = url[7:].split('/')[0]
					n = dom.find(':')
					dom = dom if n == -1 else dom[:n]
					if w.search(dom):
						for rule in deny_list:
							if re.search(rule, url):
								url = redirect_url + url
								break
						print(url)
					else:
						url = redirect_url + dom if d.search(dom) else url
						print(url)
				else:
					print(url)
		del d
		del w
		
def get_script_dir(follow_symlinks=True):
	path = inspect.getabsfile(get_script_dir)
	if follow_symlinks:
		path = os.path.realpath(path)
	return os.path.dirname(path)
	
if __name__ == "__main__":
	main()
