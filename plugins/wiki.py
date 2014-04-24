# Wiki.py - Wikipedia lookup functions for AinslyBot

from twisted.web.client import getPage
from urllib import urlencode
from HTMLParser import HTMLParser

import plugins as plugin
import json
import htmlentitydefs
import nltk
import traceback
import urllib

class HTMLTextExtractor(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
        self.result = [ ]

    def handle_data(self, d):
        self.result.append(d)

    def handle_charref(self, number):
        codepoint = int(number[1:], 16) if number[0] in (u'x', u'X') else int(number)
        self.result.append(unichr(codepoint))

    def handle_entityref(self, name):
        codepoint = htmlentitydefs.name2codepoint[name]
        self.result.append(unichr(codepoint))

    def get_text(self):
        return u''.join(self.result)

def html_to_text(html):
    s = HTMLTextExtractor()
    s.feed(html)
    return s.get_text().replace("\n","")

def plain_sentence(inp):
	sents = nltk.tokenize.sent_tokenize(inp)[0:3]
	if len(sents) == 1 and len(sents[0]) < 310:
		return sents[0]
	if len(sents) == 2 and (len(" ".join(sents[0:1]))) < 310:
		return " ".join(sents[0:1])
	if len(sents) == 3 and (len(" ".join(sents[0:2]))) < 310:
		return " ".join(sents[0:2])
	return sents[0]

WIKI_API_SEARCH = 'http://en.wikipedia.org/w/api.php?format=json&action=opensearch&limit=4&search='
WIKI_API_PAGE = 'http://en.wikipedia.org/w/api.php?action=query&prop=extracts&format=json&exintro=&titles='
WIKI_SHORT = 'http://enwp.org/'

def wikiSearchErrback(err,bot,channel):
	bot.sendMessage(channel, 'An error occurred when searching. Try again later.')

def wikiSearchCB(text,bot,channel):
	articles = json.loads(text)
	if len(articles[1]) == 0:
		bot.sendMessage(channel, 'No articles found.')
	elif len(articles[1]) > 0:
		getPage(bytes('%s%s' % (WIKI_API_PAGE,urllib.quote(articles[1][0])))).addCallbacks(
			callback=wikiGetPageCB,
			callbackArgs=[bot,channel,articles[1][0],articles[1][1:]],
			errback=wikiGetPageErrback,
			errbackArgs=[bot,channel]
			)

	
def wikiGetPageErrback(err,bot,channel):
	bot.sendMessage(channel, 'An error occurred when getting the requested article. Try again later.')

def wikiGetPageCB(text,bot,channel,pagename,similar):
	try:
		article = json.loads(text)
		articleID = article['query']['pages'].keys()[0]
		article = plain_sentence(html_to_text(article['query']['pages'][articleID]['extract']))
		if article == '':
			article = '[No excerpt available]'
		msg = u'%s' % unicode(article)
		msg = u'%s %s%s' % (msg, WIKI_SHORT,urllib.quote(pagename))
		#msg = u'%s (Similar: %s)' % (msg,u"; ".join(similar))
		bot.sendMessage(channel,msg.encode('utf-8'))
	except Exception,e:
		bot.sendMessage(channel,"An error happened :( :( :( check bot console nerd")
		print(e)
		traceback.print_exc()

@plugin.registerCommand('wiki',min_args=1)
def wikiSearchCommand(bot,user,channel,message):
	"""wiki <search term> - Searches for <search term>."""
	message = " ".join(message)
	getPage('%s%s' % (WIKI_API_SEARCH,urllib.quote(message))).addCallbacks(
		callback=wikiSearchCB,
		callbackArgs=[bot,channel],
		errback=wikiSearchErrback,
		errbackArgs=[bot,channel]
		)
