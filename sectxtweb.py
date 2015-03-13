import os, sectxt
from google.appengine.ext.webapp import template
import cgi

from google.appengine.api import users
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext import db

class Greeting(db.Model):
	author = db.UserProperty()
	content = db.StringProperty(multiline=True)
	date = db.DateTimeProperty(auto_now_add=True)

formats = ( "html",
			 "esc_html",
			 "sec",
			 "xml",
			 "dokuwiki",
			 "wikipedia",
			 "edit" )

files= (
		"README", 
		"SYNTAX", 
		"todo",
		"help",
		"organizacion_de_la_informacion", 
		) 

class MainPage(webapp.RequestHandler):

	def __process(self, sec, format, post=False, file=''):

		output="None"
		escape='no'
		if format=="html":
			output=sec.toHTML()
			escape='no'
		if format=="esc_html":
			output=sec.toHTML()
			escape='yes'
		elif format=="sec":
			output=sec.toString()
			escape='yes'
		elif format=="xml":
			output=sec.toXML()
			escape='yes'
		elif format=="dokuwiki":
			output=sec.toDokuWiki()
			escape='yes'
		elif format=="wikipedia":
			output=sec.toWikipedia()
			escape='yes'
		elif format=="edit":
			output=sec.toString()
			escape='edit'

		path = os.path.join(os.path.dirname(__file__), 'index.html')
		template_values = { 'output_html': output, 
							'escape': escape, 
							'formats': formats, 
							'format': format, 
							'files': files,
							'file': file,
							'post': post,
							'input': sec.toString(),
							}
		self.response.out.write(template.render(path, template_values))

	def get(self, format = formats[0] , file= files[0] ):
		sec = sectxt.Section()
		sec.parseFile("data/"+file+".sec")
		post = False
		self.__process(sec, format, post, file)

	def post(self):
		text = self.request.get('input')
		format = self.request.get('format')
		sec = sectxt.Section()
		lines = text.split("\n")
		sec.parseLines( lines )
		post = True
		self.__process( sec, format, post)

application = webapp.WSGIApplication(
										[
											('/', MainPage),
											('/(.*)/(.*)', MainPage),
											('/edit', MainPage),
										],
									debug=True)

def main():
	run_wsgi_app(application)

if __name__ == "__main__":
	main()
