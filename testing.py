#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
from abc import ABCMeta, abstractmethod

#-------------------------------------------------------------------------------
class Element:
#-------------------------------------------------------------------------------
	__metaclass__=ABCMeta
	def __init__(self, origin, init):
		self.origin = origin
		self.init = init 

	def __str__(self):
		return type(self).__name__+"::"+ str(self.properties())

	def properties(self):
		return {'init':str(self.init),'end':str(self.end),'origin':self.origin,'url':self.url,'text':self.text}

	def vectorInContext(self):
		v=[]
		if self.init > 0 :
			v.extend(parse_quotation(self.origin[0:self.init]))
		v_element = self.vector()
		if v_element != None :
			v.append(v_element)
		final_text=self.origin[self.end+self.separatorWidth:]
		if len(final_text) > 0 :
			next_element = first_element(final_text)
			if next_element != None:
				v.extend(next_element.vectorInContext())
			else:
				v.extend(parse_quotation(final_text))
		return v

	def vector(self):
		return [type(self).__name__, self.text, self.url]
#-------------------------------------------------------------------------------
class Image(Element):
#-------------------------------------------------------------------------------
	separatorWidth=2

	def __init__(self, origin, init):
		super(Image, self).__init__(origin, init)
		position_separator=self.origin.find('|', self.init)
		self.url=self.origin[self.init+self.separatorWidth:position_separator]
		
		self.end=self.origin.find('}}', position_separator)
		position_next_bar=self.origin.find('|', position_separator+1)
		if position_next_bar != -1 and position_next_bar < self.end:
			self.text=self.origin[position_separator+1:position_next_bar]
			self.url2=self.origin[position_next_bar+1:self.end]
		else:
			text=self.origin[position_separator+1:self.end]
			included=first_element(text)
			if included != None:
				self.text=included.vectorInContext()
			else:
				self.text=text
			self.url2=None
	
	def properties(self):
		p={'url2':self.url2}
		p.update(super(Image, self).properties())
		return p
	
	def vector(self):
		v=super(Image, self).vector()
		if self.url2 != None:
			v.append(self.url2)
		return v
		
#-------------------------------------------------------------------------------
class Link(Element):
#-------------------------------------------------------------------------------
	separatorWidth=2
	def __init__(self, origin, init):
		super(Link, self).__init__(origin, init)
		position_separator=self.origin.find(' ', self.init)
		self.url=self.origin[self.init+self.separatorWidth:position_separator]
		
		self.end=self.origin.find(']]', position_separator)

		text=self.origin[position_separator+1:self.end]
		included=first_element(text)
		if included != None:
			self.text=included.vectorInContext() 
		else:
			self.text = text
#-------------------------------------------------------------------------------
def first_element(text):
#-------------------------------------------------------------------------------
	i_link=text.find('[[');
	i_image=text.find('{{');
	if i_link == -1 and i_image == -1:
		return None
	elif i_link == -1 :
		return Image(text, i_image)
	elif i_image == -1 :
		return Link(text, i_link)
	elif i_image < i_link:
		return Image(text, i_image)
	else:
		return Link(text, i_link)
#-------------------------------------------------------------------------------
def parse_elements(vector):
#-------------------------------------------------------------------------------
	aux=[]
	for v in vector:
		if v[0]=='TXT':
			first=first_element(v[1])
			if first != None:
				aux.extend(first.vectorInContext())
			else:
				aux.extend(parse_quotation(v[1]))
		else:
			aux.append(v)
	vector=aux
	return vector
#-------------------------------------------------------------------------------
def search_replace(texto, caracteres, nombre):
#-------------------------------------------------------------------------------
	vector=[]
	fragments=texto.split(caracteres);
	for (i, t) in enumerate(fragments):
		if i>0:
			vector.append(['SYM',nombre])
		if len(t) > 0:
			vector.append(['TXT',t])

	return vector
#-------------------------------------------------------------------------------
def parse_quotation(text):
#-------------------------------------------------------------------------------
	simbols = [["'''''", "_bold_italic_"],
				["'''", "_bold_"],
				["''", "_italic_"]]
	vector=[['TXT', text]]
	for simbol in simbols: 
		aux=[]
		for v in vector:
			if v[0]=='TXT':
				aux.extend(search_replace(v[1], simbol[0], simbol[1]));
			else:
				aux.append(v)
		vector=aux
	return vector
#-------------------------------------------------------------------------------
def vector_formatter(vector, offset=""):
#-------------------------------------------------------------------------------
	for v in vector:
		object_class=v[0]
		content=v[1:]
		print offset+object_class[:3].upper()
		if object_class == 'TXT':
			print offset+"  text=",content[0]
		if object_class == 'SYM':
			print offset+"  symbol=",content[0]
		if object_class == 'Image' or object_class == 'Link':
			if isinstance(content[0], list):
				vector_formatter(content[0], offset+"    ")
			else:
				print offset+"  text=",content[0]
			print offset+"  url=", content[1]
		
#-------------------------------------------------------------------------------
#-------------------------------------------------------------------------------
def main():
#-------------------------------------------------------------------------------
	simple_italic="''italic'' text"
	italic_bolditalic_link_italic="Esta ''frase'' tiene '''''bold con italic''''', ''[[https://books.google.es/books?id=gPAM96Q_iToC Tiempo de silencio]]'', link en italic."
	quotation_1="Texto en ''italic con la ultima palabra en '''bold''''''."
	quotation_2="'''''combinada'' bold''' ''italic''."
	imgWithtUrlSimple="{{url_img|before [[url_link text]] after [[url_link2 txtt2]] end}}";
	imgWitht2Urls="begin {{img_src|[[url1 txt1]] and [[url2 txt2]]}} end {{img|kk}}";
	imgWithtUrls1="{{https://i.ytimg.com/vi/FjCKwkJfg6Y/maxresdefault.jpg|'''[[https://en.wikipedia.org/wiki/Earth Earth]]''' and the [[https://en.wikipedia.org/wiki/Moon Moon]]}}";
	image_simple="{{https://i.ytimg.com/vi/FjCKwkJfg6Y/maxresdefault.jpg|Earth and Moon}}";
	urlWithImage="[[https://en.wikipedia.org/wiki/Earth%E2%80%93Moon%E2%80%93Earth_communication {{https://i.ytimg.com/vi/FjCKwkJfg6Y/maxresdefault.jpg|'''''Earth–Moon–Earth''' communication''}}]]";

	textos= [ 
			simple_italic,
			italic_bolditalic_link_italic,
			quotation_1,
			#quotation_2,
			#imgWithtUrlSimple,
			imgWitht2Urls,
			#imgWithtUrls1,
			#image_simple,
			#urlWithImage 
			]

	for texto in textos:
		vector=parse_elements([['TXT',texto]])
		print "In:  " + texto
		vector_formatter(vector)
#-------------------------------------------------------------------------------
#-------------------------------------------------------------------------------
main()
