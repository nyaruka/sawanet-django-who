from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.views.decorators.csrf import csrf_exempt
from parser import Parser
import datetime
import urllib2
import urllib
import json
import re
from wiki import get_summary

def unescape(s):
    from htmlentitydefs import name2codepoint
    name2codepoint['#39'] = 39    
    return re.sub('&(%s);' % '|'.join(name2codepoint),
                  lambda m: unichr(name2codepoint[m.group(1)]), s)

def clean(data):
    p = re.compile(r'</?[^\W].{0,10}?>')
    stripped = p.sub('', data)

    p = re.compile(r'\s+')
    cleaned = p.sub(' ', stripped)

    return unescape(cleaned)

def lookup(needle):
    # we use google's ajax apis to search wikipedia first
    needle = "site:en.wikipedia.org %s" % needle
    query = urllib.urlencode({'q': needle})
    url = 'http://ajax.googleapis.com/ajax/services/search/web?v=1.0&%s' % query
    search_response = urllib.urlopen(url)
    search_results = search_response.read()

    # get a json response, which we parse
    results = json.loads(search_results)
    data = results['responseData']
    hits = data['results']

    # if we got at least one hit
    if len(hits):
        # get the url for the hit
        url = hits[0]['url']

        # get the title of this article, wikipedia pages always have a /wiki/ in their URL
        match = re.match(".*/wiki/(.*)", url)
        article = match.group(1)

        # grab the raw wiki markup
        wiki_markup = urllib.urlopen("http://en.wikipedia.org/w/api.php?format=xml&action=query&titles=%s&prop=revisions&rvprop=content" % article).read()

        # try to parse it and get the summary
        summary = get_summary(wiki_markup)

        # we like having 'neat' content, that is which ends on a sentence boundary, but 
        # we can't send back from than 320 characters.  This takes care of doing that.
        if len(summary) > 317:
            summary = summary[:317]
            last_period = summary.rfind(".")
            if last_period > 160:
                return summary[:last_period+1]
            else:
                return summary + ".."
        else:
            return summary
    else:
        return None

# this is where we receive our SMS message
@csrf_exempt
def receive(request):
    # POST means we should process things
    if request.method == 'POST':
        parser = Parser(request.REQUEST['text'])

        # this just strips the first word, which is our keyword 'who'
        who = parser.next_word()

        # is there more to this?  if not, send a help message
        if not parser.has_word():
            return HttpResponse("Error. Missing name. To look up facts on someone, send 'who [name]'  ex: 'who steve jobs'")

        # the reset of the text in the parser is the name of the person we are looking up
        name = parser.rest

        # try to look up the item
        summary = lookup(name)

        if summary:
            return HttpResponse(summary)
        else:
            return HttpResponse("Sorry, there are no results for %s." % name)

    # this request is a GET, so we should display a form instead
    else:
        return render_to_response('sms/receive.html',
                                  dict(),
                                  context_instance=RequestContext(request))

