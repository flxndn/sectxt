#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
from abc import ABCMeta, abstractmethod

#-------------------------------------------------------------------------------
class RichText:
#-------------------------------------------------------------------------------
	format=""
	items=[]

	def __init__(self, base, format=""):
		self.items = []
		self.format = format
		aux=[]
		if type(base).__name__ != 'str':
			aux = base
		else:
			vector=[['TXT', base]]
			for v in vector:
				if v[0]=='TXT':
					first=first_element(v[1])
					if first != None:
						aux.extend(first.vectorInContext())
					else:
						aux.extend(parse_quotation(v[1]))
				else:
					aux.append(v)

		self.items= self.vector2items(aux)

	def vector2items(self, aux):
		items=[]
		in_symbol= False
		for v in aux:
			if in_symbol :
				if v[0] == 'SYM' and v[1] == subformat:
					subelement=RichText(subvector, subformat)
					items.append(subelement)
					in_symbol = False
				else:
					subvector.append(v)
			else:
				if v[0] == 'SYM':
					in_symbol = True
					subvector = []
					subformat = v[1]
				else:
					items.append(v)
		return items

	def __str__(self):
		res= "<RichText format=\""+self.format+"\">"
		for item in self.items:
			if not isinstance(item, list):
				res +=str(item)
			elif item[0] == 'TXT':
				res += item[1]
			elif item[0] == 'RT_Link':
				res += "<a href=\""+item[2]+"\">"+str(item[1])+"</a>"
			else:
				res+=str(item)
		res += "</RichText>"
		return res

	def __repr__(self):
		return str(self)
#-------------------------------------------------------------------------------
class RT_Element:
#-------------------------------------------------------------------------------
	context=''
	init=0
	end=0
	text=''
	url=''

	__metaclass__=ABCMeta
	def __init__(self, context, init):
		self.context = context
		self.init = init 

	def properties(self):
		return {'init':str(self.init),'end':str(self.end),'context':self.context,'url':self.url,'text':self.text}

	def vectorInContext(self):
		v=[]
		if self.init > 0 :
			v.extend(parse_quotation(self.context[0:self.init]))
		v_element = self.vector()
		if v_element != None :
			v.append(v_element)
		final_text=self.context[self.end+self.separatorWidth:]
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
class RT_Image(RT_Element):
#-------------------------------------------------------------------------------
	url2=''
	separatorWidth=2

	def __init__(self, context, init):
		super(RT_Image, self).__init__(context, init)
		position_separator=self.context.find('|', self.init)
		self.url=self.context[self.init+self.separatorWidth:position_separator]
		
		self.end=self.context.find('}}', position_separator)
		position_next_bar=self.context.find('|', position_separator+1)
		if position_next_bar != -1 and position_next_bar < self.end:
			self.text=RichText(self.context[position_separator+1:position_next_bar])
			self.url2=self.context[position_next_bar+1:self.end]
		else:
			text=self.context[position_separator+1:self.end]
			self.text=RichText(text)
	
	def properties(self):
		p={'url2':self.url2}
		p.update(super(RT_Image, self).properties())
		return p
	
	def vector(self):
		v=super(RT_Image, self).vector()
		if self.url2 != None:
			v.append(self.url2)
		return v

	def __str__(self):
		return "<img src=\""+self.url+"\" link=\""+self.url2+"\">"+str(self.txt)+"</img>";
#-------------------------------------------------------------------------------
class RT_Link(RT_Element):
#-------------------------------------------------------------------------------
	separatorWidth=2

	def __init__(self, context, init):
		super(RT_Link, self).__init__(context, init)
		position_separator=self.context.find(' ', self.init)
		self.url=self.context[self.init+self.separatorWidth:position_separator]
		
		self.end=self.context.find(']]', position_separator)

		text=self.context[position_separator+1:self.end]
		self.text=RichText(text)

	def __str__(self):
		return "<a href=\""+self.url+"\">"+str(self.txt)+"</a>";
#-------------------------------------------------------------------------------
def first_element(text):
#-------------------------------------------------------------------------------
	#import pdb; pdb.set_trace()
	i_link=text.find('[[');
	i_image=text.find('{{');
	if i_link == -1 and i_image == -1:
		return None
	elif i_link == -1 :
		return RT_Image(text, i_image)
	elif i_image == -1 :
		return RT_Link(text, i_link)
	elif i_image < i_link:
		return RT_Image(text, i_image)
	else:
		return RT_Link(text, i_link)
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
	vector=parse_quotation_simple(text)
	vret=vector_expand_bold_italics(vector)
	return vret

#-------------------------------------------------------------------------------
def parse_quotation_simple(text):
#-------------------------------------------------------------------------------
	simbols = [["'''''", "_bold_italics_"],
				["'''", "_bold_"],
				["''", "_italics_"]]
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
def vector_expand_bold_italics(vector):
	bold=False
	italics=False
	count=0
	aux=[]
	for v in vector:
		if v[0] != 'SYM' or v[1]!='_bold_italics_':
			aux.append(v)
		else:
			first_bold=True
			if bold and not italics:
				first_bold = True
			elif italics and not bold:
				first_bold = False
			elif bold and italics:
				for i in range(count-1, 0, -1):
					if vector[i][1] == '_bold_':
						first_bold = True
						break
					if vector[i][1] == '_italics_':
						first_bold = False
						break
					if vector[i][1] == '_bold_italics_':
						first_bold = False
						break;
			else:
				for i in range(count+1, len(vector)-1):
					if vector[i][1] == '_bold_':
						first_bold = False
						break
					if vector[i][1] == '_italics_':
						first_bold = True
						break
					if vector[i][1] == '_bold_italics_':
						first_bold = True
						break; 

			if first_bold:
				aux.extend([['SYM','_bold_'], ['SYM', '_italics_']])
			else:
				aux.extend([['SYM','_italics_'], ['SYM', '_bold_']])

		if v[1] == '_bold_':
			bold = not bold
		elif v[1] == '_italics_':
			italics = not italics
		elif v[1] == '_bold_italics_':
			bold = not bold
			italics = not italics

		count+=1
	return aux
#-------------------------------------------------------------------------------
#-------------------------------------------------------------------------------
def main():
#-------------------------------------------------------------------------------
	tests={
	'simple_italics' : "''italics'' text",
	'quotation_1' : "Texto en ''italics con la ultima palabra en '''bold''''''.",
	'quotation_2' : "'''''combinada'' bold''' ''italics''.",
	'link' : "go to [[en.wikipedia.org wikipedia]]",
	'italics_bolditalics_link_italics' : "Esta ''frase'' tiene '''''bold con italics''''', ''[[https://books.google.es/books?id=gPAM96Q_iToC Tiempo de silencio]]'', link en italics.",
	'imgWithtUrlSimple' : "{{url_img|before [[url_link text]] after [[url_link2 txtt2]] end}}",
	'imgWitht2Urls' : "begin {{img_src|[[url1 txt1]] and [[url2 txt2]]}} end {{img|kk}}",
	'imgWithtUrls1' : "{{https://i.ytimg.com/vi/FjCKwkJfg6Y/maxresdefault.jpg|'''[[https://en.wikipedia.org/wiki/Earth Earth]]''' and the [[https://en.wikipedia.org/wiki/Moon Moon]]}}",
	'image_simple' : "{{https://i.ytimg.com/vi/FjCKwkJfg6Y/maxresdefault.jpg|Earth and Moon}}",
	'urlWithImage' : "[[https://en.wikipedia.org/wiki/Earth%E2%80%93Moon%E2%80%93Earth_communication {{https://i.ytimg.com/vi/FjCKwkJfg6Y/maxresdefault.jpg|'''''Earth–Moon–Earth''' communication''}}]]",
	}

	textos= [ 
			'simple_italics',
			'quotation_1',
			'quotation_2',
			'italics_bolditalics_link_italics',
			'link',
			'imgWithtUrlSimple',
			'imgWitht2Urls',
			'imgWithtUrls1',
			'image_simple',
			'urlWithImage'
			]

	print "<test>"
	for texto in textos:
		print "<test id=\""+texto+"\">"
		print "<in>" + tests[texto] + "</in>"
		rtext=RichText(tests[texto])
		print "<out>" + str(rtext) +"</out>"
		print "</test>"
	print "</test>"
#-------------------------------------------------------------------------------
#-------------------------------------------------------------------------------
main()
