#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
from abc import ABCMeta, abstractmethod

#-------------------------------------------------------------------------------
class Element:
#-------------------------------------------------------------------------------
	__metaclass__=ABCMeta
	@abstractmethod
	def parse(self): 
		pass

	def __init__(self, origin, init):
		self.origin = origin
		self.init = init 

	def __str__(self):
		return type(self).__name__+"::"+ str(self.properties())

	def properties(self):
		return {'init':str(self.init),'end':str(self.end),'origin':self.origin,'url':self.url,'text':self.text}
#-------------------------------------------------------------------------------
class Image(Element):
#-------------------------------------------------------------------------------
	def parse(self):
		pass 

	def __init__(self, origin, init):
		super(Image, self).__init__(origin, init)
		position_vertica_bar=self.origin.find('|', self.init)
		self.url=self.origin[self.init+2:position_vertica_bar]
		
		self.end=self.origin.find('}}', position_vertica_bar)
		position_next_bar=self.origin.find('|', position_vertica_bar+1)
		if position_next_bar != -1 and position_next_bar < self.end:
			self.text=self.origin[position_vertica_bar+1:position_next_bar]
			self.url2=self.origin[position_next_bar:self.end]
		else:
			self.text=self.origin[position_vertica_bar+1:self.end]
			self.url2=None
	
	def properties(self):
		p={'url2':self.url2}
		p.update(super(Image, self).properties())
		return p
		
#-------------------------------------------------------------------------------
class Url(Element):
#-------------------------------------------------------------------------------
	def parse(self):
		pass 
#-------------------------------------------------------------------------------
def firstElement(text):
#-------------------------------------------------------------------------------
	i_url=text.find('[[');
	i_img=text.find('{{');
	if i_url == -1 and i_img == -1:
		return None
	elif i_url == -1:
		return Image(text, i_img)
	elif i_img < i_url:
		return Image(text, i_img)
	else:
		return Url(text, i_url)
#-------------------------------------------------------------------------------
def buscar(texto, caracteres, nombre):
#-------------------------------------------------------------------------------
	vector=[]
	trozos=texto.split(caracteres);
	for (i, t) in enumerate(trozos):
		if i>0:
			vector.append(['sym',nombre])
		if len(t) > 0:
			vector.append(['txt',t])

	return vector
#-------------------------------------------------------------------------------
def parserelements(vector):
#-------------------------------------------------------------------------------
	aux=[]
	for v in vector:
		if v[0]=='txt':
			first=firstElement(v[1])
			print first
		else:
			aux.append(v)
	vector=aux
	return vector
#-------------------------------------------------------------------------------
def parsercomillas(vector):
#-------------------------------------------------------------------------------
	simbols = [["'''''", "_bold_italic_"],
				["'''", "_bold_"],
				["''", "_italic_"]]
	for simbol in simbols: 
		aux=[]
		for v in vector:
			if v[0]=='txt':
				aux.extend(buscar(v[1], simbol[0], simbol[1]));
			else:
				aux.append(v)
		vector=aux
	return vector
#-------------------------------------------------------------------------------
#-------------------------------------------------------------------------------
def main():
#-------------------------------------------------------------------------------
	cursiva_negritacursiva_enlace_cursiva="Esta ''frase'' tiene '''''negrita con cursiva''''', ''[[https://books.google.es/books?id=gPAM96Q_iToC Tiempo de silencio]]'', enlace en cursiva."
	problema_comillas="Texto en ''cursiva con la ultima palabra en '''negrita''''''."
	problema_comillas_inversas="'''''combinada'' negrita''' ''cursiva''."
	texto=problema_comillas
	
	imgWithtUrls="{{https://i.ytimg.com/vi/FjCKwkJfg6Y/maxresdefault.jpg|'''[[https://en.wikipedia.org/wiki/Earth Earth]''' and the [[https://en.wikipedia.org/wiki/Moon]]}}";
	urlWithImage="[[https://en.wikipedia.org/wiki/Earth%E2%80%93Moon%E2%80%93Earth_communication {{https://i.ytimg.com/vi/FjCKwkJfg6Y/maxresdefault.jpg|'''''Earth–Moon–Earth''' communication''}}]]";

	#vector=parsercomillas([['txt',problema_comillas_inversas+imgWithtUrls]]);
	#print(vector)

	image_simple="{{https://i.ytimg.com/vi/FjCKwkJfg6Y/maxresdefault.jpg|Earth and Moon}}";
	image_with_max="{{https://i.ytimg.com/vi/FjCKwkJfg6Y/minresdefault.jpg|Earth and Moon|https://i.ytimg.com/vi/FjCKwkJfg6Y/maxresdefault.jpg}}";
	vector=parserelements([['txt',image_simple]])
	vector=parserelements([['txt',image_with_max]])
	#print(vector)
#-------------------------------------------------------------------------------
#-------------------------------------------------------------------------------
main()
