#!/usr/bin/python
# -*- coding: utf-8 -*-

import re, sys, getopt
from textwrap import dedent

def notImplemented():
	print "Not implemented yet."

def tabulate(input):
	aux=""
	input = input.rstrip('\n')
	if input != "":
		aux = re.sub( re.compile("^",re.MULTILINE), "\t", input)
	return aux

class Element:
	"""Base class for the elements of the Line."""

class NoParsed(Element):
	"""Base class for all the elements of the Paragraphs that are not suited 
	for parsing."""
	def parseHyperlinks(self):
		return [self]
	def parseImages(self):
		return [self]
	def parseStrongtext(self):
		return [self]
	def parseEmphasized(self):
		return [self]

class Hyperlink(NoParsed):
	"""Hyperlink.
		title + url """
	def __init__(self,url,title):
		self.url = url
		self.title = title

	def toString(self):
		return "[[%s %s]]" % (self.url,self.title)

	def toHTML(self):
		return "<a href=\"%s\">%s</a>" % (self.url,self.title)

	def toMarkdown(self):
		return "[%s](%s)" % (self.title, self.url)

	def toXML(self):
		return self.toHTML()

	def toDokuWiki(self):
		return self.toString()

	def toWikipedia(self):
		return "[%s %s]" % (self.url,self.title)

	def toArticle(self):
		return "<ulink url=\"%s\"><citetitle>%s</citetitle></ulink>" % (self.url,self.title)

	def toLatex(self):
		return self.title+"\\footnote{"+self.url+"}"
		
class Strongtext(NoParsed):
	"""Strongtext.
		text """
	def __init__(self,text):
		self.text = text

	def toString(self):
		return "'''%s'''" % (self.text)

	def toHTML(self):
		return "<strong>%s</strong>" % (self.text)

	def toMarkdown(self):
		return  "**%s**" % (self.text)

	def toXML(self):
		return self.toHTML()

	def toDokuWiki(self):
		return  "**%s**" % (self.text)

	def toWikipedia(self):
		return "'''%s'''" % (self.text)

	def toArticle(self):
		return "<emphasis>%s</emphasis>" % (self.text)

	def toLatex(self):
		#TODO
		return self.text

class Emphasized(NoParsed):
	"""Emphasized.
		text """
	def __init__(self,text):
		self.text = text

	def toString(self):
		return "''%s''" % (self.text)

	def toHTML(self):
		return "<em>%s</em>" % (self.text)

	def toMarkdown(self):
		return  "*%s*" % (self.text)

	def toXML(self):
		return self.toHTML()

	def toDokuWiki(self):
		return  "%s" % (self.text)

	def toWikipedia(self):
		return "''%s''" % (self.text)

	def toArticle(self):
		return "<emphasis>%s</emphasis>" % (self.text)

	def toLatex(self):
		#TODO
		return self.text

class Image(NoParsed):
	def __init__(self,url):
		self.url = url

	def toString(self):
		return "{{%s}}" % (self.url)

	def toHTML(self):
		return "<img src=\"%s\" />" % (self.url)

	def toMarkdown(self):
		return "![Alternative text](%s)" % (self.url)

	def toXML(self):
		return "<image url=\"%s\" />" % (self.url)

	def toDokuWiki(self):
		return self.toString()

	def toWikipedia(self):
		return "[file:%s]" % (self.url)

	def toArticle(self):
		return "<mediaobject><imageobject><imagedata fileref=\"%s\"/></imageobject></mediaobject>" % (self.url)

	def toLatex(self):
		# TODO: ir the url is actualy an url then change includegraphics with
		#       \write18{wget http://www.some-site.com/path/to/image.png}
		#		\includegraphics{image.png}

		# TODO: less code for images

		return '''\\begin{figure}[ht!]
		\\centering
		\\includegraphics[width=90mm]{'''+self.url+'''}
		\\label{overflow}
		\\end{figure}
		'''

class ImageTitled(Image):
	def __init__(self,url,title):
		self.url = url
		self.title = title

	def toString(self):
		return "{{%s|%s}}" % (self.url, self.title)

	def toHTML(self):
		return "<img src=\"%s\" alt=\"%s\" title=\"%s\"/>" % (self.url, 
															self.title, 
															self.title)
	def toMarkdown(self):
		return "![%s](%s)" % (self.title, self.url)

	def toXML(self):
		return "<image url=\"%s\" title=\"%s\"/>" % (self.url,
															self.title )
	def toWikipedia(self):
		return "[file:%s %s]" % (self.url, self.title)

	def toArticle(self):
		return "<mediaobject><imageobject><imagedata fileref=\"%s\"/></imageobject> <textobject> <phrase>%s</phrase> </textobject></mediaobject>" % (self.url, self.title)
	
	def toLatex(self):
		return '''\\begin{figure}[ht!]
		\\centering
		\\includegraphics[width=90mm]{'''+self.url+'''}
		\\caption{'''+self.title+'''}
		\\label{overflow}
		\\end{figure}
		'''

class ImageBig(ImageTitled):
	def __init__(self,url,title,urlBig):
		self.url = url
		self.title = title
		self.urlBig = urlBig

	def toString(self):
		return "{{%s|%s|%s}}" % (self.url, self.title, self.urlBig)

	def toHTML(self):
		return """<a href="%s"><img src="%s" alt="%s" title="%s"/></a>""" % (self.urlBig, self.url, self.title, self.title )

	def toMarkdown(self):
		#FIXME: it doesn't use the urlBig
		return "![%s](%s)" % (self.title, self.url)

	def toXML(self):
		return "<image url=\"%s\" title=\"%s\" urlbig=\"%s\"/>" % (self.url,
													self.title,
													self.urlBig )
	def toArticle(self):
		return "<mediaobject><imageobject><imagedata fileref=\"%s\"/></imageobject> <textobject> <phrase>%s</phrase> </textobject></mediaobject>" % (self.urlBig, self.title)

	def toLatex(self):
		return '''\\begin{figure}[ht!]
		\\centering
		\\includegraphics[width=90mm]{'''+self.urlBig+'''}
		\\caption{'''+self.title+'''}
		\\label{overflow}
		\\end{figure}
		'''

class PlainText(Element):
	"""PlainText"""
	def __init__(self,text):
		self.text = text
	def toString(self):
		return self.text

	def toHTML(self):
		return self.toString()

	def toMarkdown(self):
		return self.toString()

	def toXML(self):
		return self.toString()

	def toDokuWiki(self):
		return self.toString()

	def toWikipedia(self):
		return self.toString()

	def toArticle(self):
		return self.toString()

	def toLatex(self):
		return self.toString()

	def parseHyperlinks(self):
		texts = re.split("\[\[|\]\]",self.text)
		counter = 0
		elements = []
		for text in texts:
			if counter % 2 == 0:
				elements.append( PlainText(text) )
			else:
				url,title = re.split(" *[\| ] *",text,1)
				elements.append( Hyperlink(url,title) )
			counter+=1
		return elements

	def parseStrongtext(self):
		texts = re.split("'''",self.text)
		counter = 0
		elements = []
		for text in texts:
			if counter % 2 == 0:
				elements.append( PlainText(text) )
			else:
				elements.append( Strongtext(text) )
			counter+=1
		return elements

	def parseEmphasized(self):
		texts = re.split("''",self.text)
		counter = 0
		elements = []
		for text in texts:
			if counter % 2 == 0:
				elements.append( PlainText(text) )
			else:
				elements.append( Emphasized(text) )
			counter+=1
		return elements

	def parseImages(self):
		texts = re.split("\{\{|\}\}",self.text)
		counter = 0
		elements = []
		for text in texts:
			if counter % 2 == 0:
				elements.append( PlainText(text) )
			else:
				parameters = re.split(" *\| *",text)
				
				image = None
				if len(parameters) == 3:
					image = ImageBig( *parameters )
				elif len(parameters) == 2:
					image = ImageTitled( *parameters)
				else:
					image = Image( *parameters )

				elements.append( image )
			counter+=1
		return elements

	def toLatex(self):
		return self.toString()

class Elements(list):
	"""Elements in a line.
	*PlainText
	*Hyperlink"""

	def __init__(self, elements=None ):
		if elements is None:
			elements = []
		self = elements

	def toString(self):
		txt = ""
		for element in self:
			txt += element.toString()
		return txt

	def toHTML(self):
		txt = ""
		for element in self:
			txt += element.toHTML()
		return txt

	def toMarkdown(self):
		txt = ""
		for element in self:
			txt += element.toMarkdown()
		return txt

	def toXML(self):
		txt = ""
		for element in self:
			txt += element.toXML()
		return txt

	def toDokuWiki(self):
		txt = ""
		for element in self:
			txt += element.toDokuWiki()
		return txt

	def toWikipedia(self):
		txt = ""
		for element in self:
			txt += element.toWikipedia()
		return txt

	def toArticle(self):
		txt = ""
		for element in self:
			txt += element.toArticle()
		return txt

	def toLatex(self):
		txt = ""
		for element in self:
			txt += element.toLatex()
		return txt

class Line:
	""" A line is an base class formed by one or more elements."""

	def __init__(self, elements=None ):
		if elements is None:
			elements = Elements()
		self.elements = elements

	def __init__(self, text="" ):
		self.elements = Elements()
		self.parse(text)

	def parse(self,txt):
		# Strongtext
		parsed = PlainText(txt).parseStrongtext()
		# Emphasidedtext
		aux=[]
		for element in parsed:
			aux.extend( element.parseEmphasized() )
		parsed=aux
		# Hyperlink
		aux=[]
		for element in parsed:
			aux.extend( element.parseHyperlinks() )
		parsed=aux
		# Images
		aux=[]
		for element in parsed:
			aux.extend( element.parseImages() )
		parsed=aux
		#
		self.elements.extend( parsed )

	def toString(self):
		return self.elements.toString()
		
	def toHTML(self):
		return self.elements.toHTML()

	def toMarkdown(self):
		return self.elements.toMarkdown()

	def toXML(self):
		return self.elements.toXML()

	def toDokuWiki(self):
		return self.elements.toDokuWiki()

	def toWikipedia(self):
		return self.elements.toWikipedia()

	def toArticle(self):
		return self.elements.toArticle()

	def toLatex(self):
		return self.elements.toLatex()

class Headline(Line):
	"""Line with the title of the section."""

class Paragraph(Line):
	"""Line suitable for paragraphs."""
	def toString(self):
		return self.elements.toString() + "\n"
		
	def toHTML(self):
		return "\t<p>"+self.elements.toHTML()+"</p>\n"

	def toMarkdown(self):
		return self.elements.toMarkdown() + "\n"

	def toXML(self):
		return "<p>"+self.elements.toXML()+"</p>"

	def toDokuWiki(self):
		return self.elements.toDokuWiki() + "\n"

	def toWikipedia(self):
		return self.elements.toWikipedia() + "\n"

	def toArticle(self):
		return "<section>"+self.elements.toArticle()+"</section>"

	def toLatex(self):
		return self.elements.toLatex() + "\n\n"

	@staticmethod
	def openNestingTagHTML():
		return ""

	@staticmethod
	def closeNestingTagHTML():
		return ""

	@staticmethod
	def openNestingLatex():
		return ""

	@staticmethod
	def closeNestingLatex():
		return ""

	@staticmethod
	def openNestingTagArticle():
		return ""

	@staticmethod
	def closeNestingTagArticle():
		return ""

	@staticmethod
	def type():
		return "p"

	@staticmethod
	def wikipediaReturn():
		return "\n\n"

class NestedLine(Line):
	"""Abstract Line for lines that must be enclosed between tags."""

	@staticmethod
	def wikipediaReturn():
		return "\n"

class ListElement(NestedLine):
	"""Line suitable for list elements."""
	def toString(self):
		return "-" + self.elements.toString()
		
	def toHTML(self):
		return "\t\t<li>"+self.elements.toHTML()+"</li>\n"

	def toMarkdown(self):
		# FIXME: it also works for unordered lists
		return "* "+ self.elements.toMarkdown()

	def toXML(self):
		return "<li>"+self.elements.toXML()+"</li>"

	def toDokuWiki(self):
		return "* " + self.elements.toDokuWiki()

	def toWikipedia(self):
		return "* " + "INI" + self.elements.toWikipedia() + "FIN"

	def toArticle(self):
		return "<listitem><para>"+self.elements.toArticle()+"</para></listitem>"

	def toLatex(self):
		return "\item "+self.elements.toLatex()+"\n"

	@staticmethod
	def openNestingTagHTML():
		return "\t\t<ul>\n"

	@staticmethod
	def closeNestingTagHTML():
		return "\t\t</ul>\n"

	@staticmethod
	def openNestingLatex():
		return "\\begin{itemize}\n"

	@staticmethod
	def closeNestingLatex():
		return "\\end{itemize}\n"

	@staticmethod
	def openNestingTagArticle():
		return "<itemizedlist>"

	@staticmethod
	def closeNestingTagArticle():
		return "</itemizedlist>"

	@staticmethod
	def type():
		return "ul"

class ListElementNumeric(ListElement):
	"""Line suitable for numeric list elements."""
	def toString(self):
		return "#" + self.elements.toString()
		
	def toDokuWiki(self):
		return "-" + self.elements.toString()

	def toWikipedia(self):
		return self.toString()

	def toArticle(self):
		return "<listitem><para>"+self.elements.toArticle()+"</para></list>"

	@staticmethod
	def openNestingTagHTML():
		return "\t\t<ol>\n"

	@staticmethod
	def closeNestingTagHTML():
		return "\t\t</ol>\n"

	@staticmethod
	def openNestingLatex():
		return "\\begin{enumerate}\n"

	@staticmethod
	def closeNestingLatex():
		return "\\end{enumerate}\n"

	@staticmethod
	def openNestingTagArticle():
		return "<orderedlist>"

	@staticmethod
	def closeNestingTagArticle():
		return "</orderedlist>"

	@staticmethod
	def type():
		return "ol"

class ListElementDefinitionTerm(NestedLine):
	"""Line suitable for list elements."""
	def toString(self):
		return "-" + self.elements.toString()
		
	def toHTML(self):
		return "\t\t<dt>"+self.elements.toHTML()+"</dt>\n"

	def toMarkdown(self):
		#FIXME
		return "* "+self.elements.toMarkdown()+"\n"

	def toXML(self):
		return "<dt>"+self.elements.toXML()+"</dt>"

	def toDokuWiki(self):
		return "* " + self.elements.toDokuWiki() #TODO: test

	def toWikipedia(self):
		return "; " + self.elements.toWikipedia()

	def toArticle(self):
		return "<listitem><para>"+self.elements.toArticle()+"</para></listitem>" #TODO: test

	def toLatex(self):
		return "\\item["+self.elements.toLatex()+"]\n"

	@staticmethod
	def openNestingTagHTML():
		return "\t\t<dl>\n"

	@staticmethod
	def closeNestingTagHTML():
		return "\t\t</dl>\n"

	@staticmethod
	def openNestingLatex():
		return "\\begin{description}\n"

	@staticmethod
	def closeNestingLatex():
		return "\\end{description}\n"

	@staticmethod
	def openNestingTagArticle():
		return "<itemizedlist>" #TODO: test

	@staticmethod
	def closeNestingTagArticle():
		return "</itemizedlist>" #TODO: test

	@staticmethod
	def type():
		return "dl"

class ListElementDefinitionDefinition(NestedLine):
	"""Line suitable for list elements."""
	def toString(self):
		return "::" + self.elements.toString()
		
	def toHTML(self):
		return "\t\t<dd>"+self.elements.toHTML()+"</dd>\n"

	def toMarkdown(self):
		#FIXME
		return "* "+self.elements.toMarkdown()+"\n"

	def toXML(self):
		return "<dd>"+self.elements.toXML()+"</dd>"

	def toDokuWiki(self):
		return "* " + self.elements.toDokuWiki() #TODO: test

	def toWikipedia(self):
		return ": " + self.elements.toWikipedia()

	def toArticle(self):
		return "<listitem><para>"+self.elements.toArticle()+"</para></listitem>" #TODO: test

	def toLatex(self):
		return self.elements.toLatex()+"\n"

	@staticmethod
	def openNestingTagHTML():
		return "\t\t<dl>\n"

	@staticmethod
	def closeNestingTagHTML():
		return "\t\t</dl>\n"

	@staticmethod
	def openNestingLatex():
		return "\\begin{description}\n"

	@staticmethod
	def closeNestingLatex():
		return "\\end{description}\n"

	@staticmethod
	def openNestingTagArticle():
		return "<itemizedlist>" #TODO: test

	@staticmethod
	def closeNestingTagArticle():
		return "</itemizedlist>" #TODO: test

	@staticmethod
	def type():
		return "dl"

class LiteralLine(NestedLine):
	"""Line suitable for literals."""
	def toString(self):
		return ">" + self.elements.toString()
		
	def toHTML(self):
		return self.elements.toHTML()+"\n"

	def toMarkdown(self):
		return "```\n"+ self.elements.toMarkdown()+"\n```\n"

	def toXML(self):
		return "<pre>"+self.elements.toHTML()+"</pre>"

	def toDokuWiki(self):
		return " " + self.toString()

	def toWikipedia(self):
		return ">" + self.toString()

	def toArticle(self):
		return self.elements.toArticle()

	def toLatex(self):
		return self.toString()[1:]+"\n"

	@staticmethod
	def openNestingTagHTML():
		return "\t\t<pre>"

	@staticmethod
	def closeNestingTagHTML():
		return "</pre>\n"

	@staticmethod
	def openNestingLatex():
		return "\\begin{verbatim}\n"

	@staticmethod
	def closeNestingLatex():
		return "\\end{verbatim}\n"

	@staticmethod
	def openNestingTagArticle():
		return "\t\t<programlisting>i\n<![CDATA[\n"

	@staticmethod
	def closeNestingTagArticle():
		return "\n]]>\n\t\t</programlisting>\n"

	@staticmethod
	def type():
		return "pre"

class LineFactory:
	@staticmethod
	def createLine( text ):
		text = re.sub("^\t*\* ", "", text )
		if   re.match(">", text):
			return LiteralLine( text[1:]  )
		elif re.match("-", text):
			if re.search("::", text):
				elements=text[1:].split('::')
				items=[]
				items.append(ListElementDefinitionTerm(elements[0]))
				del elements[0]
				while len(elements) > 0 :
					items.append(ListElementDefinitionDefinition(elements[0]))
					del elements[0]
				return items
			else:
				return ListElement( text[1:]  )
		elif re.match("#", text ):
			return ListElementNumeric( text[1:]  )
		else:
			return Paragraph( text ) 

class Section:
	"""The top class or this application."""

	def __init__(self, title="No title", paragraphs=None, subsections=None):
		self.title = title  
		if paragraphs is None:
			paragraphs = []
		self.paragraphs = paragraphs

		if subsections is None:
			subsections = []
		self.subsections = subsections

		self.lastParagraphOpen = False
		self.lastParagraphSpecial = False

		self.lastParagraph=None

	def toString(self):
		content=""
		p=[]
		for i in self.paragraphs:
			p.append(i.toString())

		s=[]
		for i in self.subsections:
			s.append(i.toString())

		aux = "* " \
				+ self.title.toString() \
				+ "\n" \
				+ tabulate( "\n".join(p) + "\n".join(s) )

		return aux.rstrip('\n')

	def toXML(self, level=0):
		paragraphs=""
		for i in self.paragraphs:
			paragraphs += i.toXML()
		if len(self.paragraphs) > 0:
			paragraphs = "<paragraphs>" + paragraphs + "</paragraphs>"

		subsections=""
		for i in self.subsections:
			subsections += i.toXML(level+1)
		if len(self.subsections) > 0:
			subsections = "<subsections>" + subsections + "</subsections>"

		version=""
		if level == 0:
			version="<?xml version=\"1.0\" encoding=\"UTF-8\" ?>\n"

		return ( version \
				+ "<section>" \
				+ "<title>" + self.title.toXML() +"</title>" \
				+ paragraphs \
				+ subsections \
				+ "</section>" )
	
	def toc(self, prePath, extra_divs):
		ret=''
		if self.subsections:
			ret = "<ul class=\"toc\">"
			for s in self.subsections:
				ret += "<li><a href=\"#%s\">%s</a></li>" % ( re.sub('"', '_', prePath + "/" +s.title.toHTML()), s.title.toHTML() )
			#ret += "<li><a href=\"#%s\">%s</a></li>" % ( prePath, "Subir" )
			ret += "</ul>"
			if extra_divs:
				ret += "<div class=\"toc_end\"></div>"
		return ret

	def toHTML(self, level = 1, path='', toc=False, extra_divs=True):
		path=path+"/"+str(self.title.toHTML())
		paragraphs=""
		for i in self.paragraphs:
			if self.lastParagraph is None:
				paragraphs += i.openNestingTagHTML()
			elif self.lastParagraph.type() != i.type():
				paragraphs += self.lastParagraph.closeNestingTagHTML()
				paragraphs += i.openNestingTagHTML()
			paragraphs += i.toHTML()
			self.lastParagraph = i
		if self.lastParagraph is not None:
			paragraphs += self.lastParagraph.closeNestingTagHTML()

		if paragraphs != "" and extra_divs:
			paragraphs="<div class=\"paragraphs\">\n" + paragraphs + "</div><!--class=paragraphs-->\n"

		subsections=""
		for i in self.subsections:
			subsections += i.toHTML( level + 1 , path, toc, extra_divs)

		if subsections != ""  and extra_divs:
			subsections="<div class=\"subsections\">\n" + subsections + "</div><!--class=subsections-->\n"

		if extra_divs:
			aux = "<div class=\"section\">\n"
		else: 
			aux = ""

		aux+= "<h%d><a name=\"%s\"></a>%s</h%d>\n" % (level, re.sub('"', '_', path), self.title.toHTML(), level)
		if toc:
			aux+= self.toc(path, extra_divs)

		aux+= paragraphs + subsections
		if extra_divs:
			aux+= "</div><!--class=section-->\n"
		return aux

	def toHTMLTOC(self, level = 1, path='', html_toc_max_level=0):
		path=path+"/"+str(self.title.toHTML())
		aux="<a href=\"#"+path+"\">"+self.title.toHTML()+"</a>";
		subsections=""

		if html_toc_max_level ==0 or level <= html_toc_max_level:
			for i in self.subsections:
				subsections += "<li>"+i.toHTMLTOC( level=level + 1 , path=path, html_toc_max_level=html_toc_max_level)+"</li>\n"
			if subsections != "":
				aux+="<ul>" + subsections + "</ul>\n";

		return aux

	def toDokuWiki(self, level = 5):
		if level<0:
			print "Error. Too many levels."
			sys.exit(2)
		paragraphs=""
		for i in self.paragraphs:
			paragraphs +=  i.toDokuWiki() + "\n\n"

		subsections=""
		for i in self.subsections:
			subsections += i.toDokuWiki( level - 1 )

		equals = "=" * level
		aux = "%s %s %s\n" % (equals,  self.title.toDokuWiki(), equals)
		aux+= paragraphs + subsections
		return aux

	def toMarkdown(self, level = 1):
		paragraphs=""
		for i in self.paragraphs:
			paragraphs +=  i.toMarkdown() + "\n"

		subsections=""
		for i in self.subsections:
			subsections += i.toMarkdown( level + 1 )

		equals = "#" * level
		aux = "%s %s\n" % (equals,  self.title.toMarkdown())
		aux+= paragraphs + subsections + "\n"
		return aux
	
	def toWikipedia(self, level = 1):
		if level>5:
			print "Error. Too many levels."
			sys.exit(2)
		paragraphs=""
		for i in self.paragraphs:
			paragraphs +=  i.toWikipedia() + i.wikipediaReturn()

		subsections=""
		for i in self.subsections:
			subsections += i.toWikipedia( level + 1 )

		equals = "=" * level
		aux = "%s %s %s\n" % (equals,  self.title.toDokuWiki(), equals)
		aux+= paragraphs + subsections
		return aux
	
	def toArticle(self, level=0):
		paragraphs=""
		for i in self.paragraphs:
			if self.lastParagraph is None:
				paragraphs += i.openNestingTagArticle()
			elif self.lastParagraph.type() != i.type():
				paragraphs += self.lastParagraph.closeNestingTagArticle()
				paragraphs += i.openNestingTagArticle()
			paragraphs += i.toArticle()
			self.lastParagraph = i
		if self.lastParagraph is not None:
			paragraphs += self.lastParagraph.closeNestingTagArticle()

		subsections=""
		for i in self.subsections:
			subsections += "<section>"+i.toArticle(level+1)+"</section>";

		version=""
		if level == 0:
			version="<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n<!DOCTYPE book PUBLIC \"-//OASIS//DTD DocBook XML V4.2//EN\" \"http://www.oasis-open.org/docbook/xml/4.5/docbookx.dtd\">\n"
			txt = version \
				+ "<article lang=\"es\">" \
				+ "<articleinfo>" \
				+ "<title>" + self.title.toArticle() +"</title>" \
				+ "<abstract>" + paragraphs +"</abstract>" \
				+ "</articleinfo>" \
				+ subsections \
				+ "</article>" 
		else: 
			txt = paragraphs + subsections

		return ( txt )

	def toLatex(self, level = 1):
		aux="" 
		section_name=""

		if level == 1:
			section_name="title"
			aux =dedent("""
				\\documentclass[a4paper,11pt]{article}
				\\usepackage[utf8]{inputenc}
				\\usepackage{eurosym}
				\\usepackage{graphicx}
				\\author{H.~Partl}
				""").strip()+"\n"
		elif level == 2:
			section_name="section"
		elif level == 3:
			section_name="subsection"
		elif level == 4:
			section_name="subsubsection"
		else:
			section_name="part"

		aux += "\\"+section_name+"{"+self.title.toString() +"}\n"
		
		if level == 1:
			aux +=dedent("""
				\\begin{document}
				\maketitle
				\\tableofcontents
				""").strip()+"\n"
		paragraphs=""
		for i in self.paragraphs:
			if self.lastParagraph is None:
				paragraphs += i.openNestingLatex()
			elif self.lastParagraph.type() != i.type():
				paragraphs += self.lastParagraph.closeNestingLatex()
				paragraphs += i.openNestingLatex()
			paragraphs += i.toLatex()
			self.lastParagraph = i
		if self.lastParagraph is not None:
			paragraphs += self.lastParagraph.closeNestingLatex()

		subsections=""
		for i in self.subsections:
			subsections += i.toLatex( level + 1 )

		if level == 1:
			aux+= "\\begin{abstract}\n" + paragraphs + "\\end{abstract}\n" + subsections
			aux +="\end{document}"
		else:
			aux+= paragraphs + subsections

		return aux

	def lastSubsection(self):
		count = len( self.subsections )
		if count == 0:
			return None 
		else:
			return self.subsections[ count - 1 ]

	def addTitle( self, line, depth = 0 ):
		text = re.sub("^\t*\* ", "", line)
		title = Headline( text )
		level = len(line) - len(text) - 2

		if level == 0:
			self.title = title
		else:
			if level == depth + 1:
				self.subsections.append( Section(title) )
			else:
				self.lastSubsection().addTitle(line, depth + 1 )
				
	def addParagraph(self, line, depth=0):
		text = re.sub("^\t*", "", line)

		if len(self.subsections) > 0:
			self.lastSubsection().addParagraph( line, depth + 1)
		else:
			if ( text == "" ):
				self.lastParagraphOpen = False
				self.lastParagraphSpecial = False
			else:
				"""
				We are in a section with no subsections. In the tree's end.

				For every line we can add it to the last paragraph or create a new paragraph.

				We make a new paragraph if:
				- There are no paragraphs.
				- Last line was blank
				- Actual line begins with an special character[>#-]
				- The actual line dosn't begin with a specia character but the last one did.
				"""
				if len(self.paragraphs) == 0 \
						or not self.lastParagraphOpen \
						or re.match("[>#-]",text) \
						or self.lastParagraphSpecial:
					paragraph = LineFactory.createLine( text )
					if isinstance(paragraph, list):
						self.paragraphs.extend( paragraph )
					else:
						self.paragraphs.append( paragraph )
					if re.match("[>#-]",text):
						self.lastParagraphSpecial = True
				else:
					text = "\n" + text
					self.paragraphs[ len(self.paragraphs) - 1 ].parse(text)

				#if len(self.paragraphs) > 0 and self.lastParagraphOpen:
					#text = "\n" + text
					#self.paragraphs[ len(self.paragraphs) - 1 ].parse(text)
				#else:
					#paragraph = LineFactory.createLine( text )
					#self.paragraphs.append( paragraph )

				self.lastParagraphOpen = True

	def parseLine(self, line=None):
		line = line.rstrip('\n')
		if re.match("^\t*\* ",line):
			self.addTitle(line)
		else:
			self.addParagraph(line)

	def parseText(self, text=None):
		self.parseLines(text.split("\n"))
		
	def parseLines(self, lines=None):
		for line in lines:
			self.parseLine( line )
		
	def parseFile(self,filename):
		f = open( filename, "r")
		self.parseLines( f.readlines() )
	
	def parseStdin(self):
		self.parseLines( sys.stdin);

	def filter(self,pattern):
		aux = None
		if re.search(pattern, self.title.toString() ) is not None:
			return self
		else:
			for subsection in self.subsections:
				aux = subsection.filter( pattern)
				if aux is not  None:
					return aux
		return None

def usage():

	print """* sectxt.py
	Sections converter
	
	* Usage
		> sectxt.py  -<format> [options] [file.sec]
		> sectxt.py -h
		
	* Description
		Reads standard input [or file.sec] parse it in sec format and outputs 
		the content in the selected format.

		For sec syntax read SYNTAX.SEC
	* Formats
		* -t, --txt
			Converts file.sec to text format (normalized).
		* -m, --html
			Converts file.sec to html format.

			This html is not a full html page.
		* -x, --xml
			Converts file.sec to XML format.
		* -d, --dokuwiki
			Converts file.sec to [[http://www.dokuwiki.org/syntax DokuWiki format]].
		* -w, --wikipedia
			Converts file.sec to [[http://en.wikipedia.org/wiki/Wikipedia:Cheatsheet Wikipedia format]].
		* -a, --article
			Converts file.sec to [[http://en.wikipedia.org/wiki/DocBook docbook]] article.
		* -l, --latex
			Converts file.sec to the content of a latex article.
		* -k, --markdown
			Converts file.sec to [[https://en.wikipedia.org/wiki/Markdown Markdown format]].
		* -o, --html_toc max_level
			Converts file.sec in an html nested list of links to the titles 
			of the sections of the document.

			Nested until max_level is reached.

			No limit if max_level is equal to 0.
	* Options
		* -f, --filter pattern
			Only shows the section with the title that match pattern.
		* -h, --help
			Show this help.
		* -i, --toc
			Include a table of contents of the subsections between the title 
			and the texts.

			Only works with selected type is html.
		* -n, --no_extra_divs
			Do not include extra divs for paragraphs, tocs, etc.
	"""

def main():
	try:
		opts, args = getopt.getopt(sys.argv[1:], "f:htkmxdwialno:", ["filter=", "help","txt","html","html_toc=", "markdown", "xml","dokuwiki","wikipedia","toc", "article", "latex", "no_extra_divs"])
	except getopt.GetoptError, err:
		# print help information and exit:
		print str(err) # will print something like "option -a not recognized"
		usage()
		sys.exit(2)

	sec = Section()
	pattern = ""
	html_toc_max_level=0
	toc=False
	extra_divs=True
	format = "sec"
	for o, a in opts:
		if o in ("-h", "--help"):
			usage()
			sys.exit()
		else:
			if o in ("-f","--filter"):
				pattern = a
			elif o in ("-t","--txt"):
				format = "sec"
			elif o in ("-m", "--html"):
				format = "html"
			elif o in ("-o", "--html_toc"):
				format = "html_toc"
				html_toc_max_level=int(a)
			elif o in ("-k", "--markdown"):
				format = "markdown"
			elif o in ("-x", "--xml"):
				format = "xml"
			elif o in ("-d", "--dokuwiki"):
				format = "dokuwiki"
			elif o in ("-w", "--wikipedia"):
				format = "wikipedia"
			elif o in ("-a", "--article"):
				format = "article"
			elif o in ("-l", "--latex"):
				format = "latex"
			elif o in ("-i", "--toc"):
				toc = True
			elif o in ("-n", "--no_extra_divs"):
				extra_divs = False
			else:
				assert False, "unhandled option"

	if len(args)>0:
		sec.parseFile(args[0])
	else:
		sec.parseStdin()

	if pattern != "":
		sec = sec.filter( pattern )

	if format == "sec":
		print sec.toString()
	elif format == "html":
		print sec.toHTML( toc=toc, extra_divs=extra_divs )
	elif format == "html_toc":
		print "<div id=\"full_toc\">"+sec.toHTMLTOC(html_toc_max_level=html_toc_max_level)+"</div>"
	elif format == "markdown":
		print sec.toMarkdown()
	elif format == "xml":
		print sec.toXML()
	elif format == "dokuwiki":
		print sec.toDokuWiki()
	elif format == "wikipedia":
		print sec.toWikipedia()
	elif format == "article":
		print sec.toArticle()
	elif format == "latex":
		print sec.toLatex()

if __name__ == "__main__":
	main()
	
