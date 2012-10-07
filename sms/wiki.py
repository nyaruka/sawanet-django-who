#!/usr/bin/python

from xml.dom.minidom import parse, parseString
import re

# iterates through all nodes in the XML catting all the text nodes together
def get_text(node, text):
    if node.nodeType == node.TEXT_NODE:
        return node.data
    else:
        for node in node.childNodes:
            text += get_text(node, text)

        return text

# given a mediawiki markup file does its best to return the text for the file
def get_summary(wikitext):
    dom = parseString(wikitext)

    # grab all our text out
    text = ""
    for node in dom.childNodes:
        text += get_text(node, text)

    # start stripping things.. first everything between {{ }}
    old_text = ""
    while text != old_text:
       old_text = text
       text = re.sub("{{[^{{]*?}}", "", text, flags=re.DOTALL|re.MULTILINE)

    # start stripping things.. next everything between {| |}
    old_text = ""
    while text != old_text:
       old_text = text
       text = re.sub("{\|[^{]*?\|}", "", text, flags=re.DOTALL|re.MULTILINE)

    text = re.sub("<ref[^<]*?/>", "", text, flags=re.DOTALL|re.MULTILINE)

    # ref tags
    old_text = ""
    while text != old_text:
       old_text = text
       text = re.sub("<ref[^<]*?>.*?</ref>", "", text, flags=re.DOTALL|re.MULTILINE)

    text = re.sub("<\!--.*?-->", "", text, flags=re.DOTALL|re.MULTILINE)
    text = re.sub("\[\[([^\|\]]+?)\]\]", "\\1", text, flags=re.DOTALL|re.MULTILINE)
    text = re.sub("\[\[.*?\|(.*?)\]\]", "\\1", text, flags=re.DOTALL|re.MULTILINE)
    text = re.sub("'''", "", text, flags=re.DOTALL|re.MULTILINE)
    text = re.sub("\(\W*;\W*", "(", text, flags=re.DOTALL|re.MULTILINE)

    return text.strip()

#f = open('mj.xml', 'r')
#content = f.read()

#print get_summary(content)[:1024].strip()
