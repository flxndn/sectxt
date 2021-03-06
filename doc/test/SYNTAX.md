# Syntax of sec files
Version 1.0

## Files
A sec file is a plain text file.


## Format
The format of the document is done with tabs, asterisks plus space and
white lines.

The indentation means importance. The more indentation the less 
important in the document structure.

The titles are formatted with one asterisks and one space.


## Structure
### File
A *.sec file is a Section.


### Section
A section contains a title, zero or more paragraphs and zero or 
more subsections.


### Title
A text string with no carriage return allowed.


### Paragraph
The texts of the section.

The paragraphs can be:

#### Normal paragraphs
The first non-tab character can be any char except 
asterisk (*), dash (-), greater-than (>) or number sign (#).

You can write a paragraph using many lines. 

To make a new paragraph, write a blank line.

The paragraphs are separated with blank lines.


#### List elements
The first non-tab character is a dash.

Example:

*  Europe
*  America
*  Asia

#### Numeric list elements
The first non-tab character is number sign (#).

Example:

*  Python
*  C++
*  Perl

#### Literal lines
The first non-tab character is a greater-than sign.

Example:

```
class program:
```

```
  def run(self):
```

```
    print "Hello World"
```

```
    return 0
```


#### Definition lists
You can do definition lists using List elements as term with the definition or definitions after two colons (::)

Example:

*  title

*  Moby Dick

*  Author

*  Herman Melville

*  Year

*  1851

*  1926, first movie



### Titles and Paragraphs 
Can contain:

#### Plain text
Plain text is..., well..., you know...


#### Emphasized text
One or more words can be emphasized in the same line using 2 
apostrophe-quotes in the begin and in the end of the text:

Example: I like Poe's poem *The Raven*.


#### Strong text
One or more words can be marked as strong in the same line 
using 3 apostrophe-quotes in the begin and in the end of the text:

Example: I like Poe's poem **The Raven**.


#### Hyperlinks
Hyperlinks are an URL and a title enclosed into double square
brackets, with an space between the URL and the title.

Example: [Competitors](https://en.wikipedia.org/wiki/Category:Markup_languages) of sectxt.


#### Images
You can include external and internal images with curly brackets.	

You can add optional elements as title and the URL for a bigger image.

Examples: 

*  Image only

*  ![Alternative text](http://i.imgur.com/e0bfiLv.jpg)

*  Image with caption 

*  ![The python](http://i.imgur.com/e0bfiLv.jpg) 

*  place cursor over image

*  Image with caption and link to bigger image 

*  ![The python](http://i.imgur.com/e0bfiLv.jpg) 

*  click in image



### Subsections
The subsections are sections. Do you know what is recursion?





