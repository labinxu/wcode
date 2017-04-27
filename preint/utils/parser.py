from HTMLParser import HTMLParser


class HTMLTag:
    def __init__(self, tagname, attrs):
        self.name = tagname
        if isinstance(attrs, dict):
            self.attrs = attrs
        else:
            self.attrs = dict(attrs)

    def text(self):
        pass


class WebParser(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
        self.content = {' ': []}
        self.tag_stack = []

    def add_tag(self, tag, attrs):
        if tag not in self.content:
            self.content[tag] = [HTMLTag(tag, attrs)]
        else:
            self.content[tag].append(HTMLTag(tag, attrs))

    def handle_starttag(self, tag, attrs):
        #self.tag_stack.append(HTMLTag(tag, attrs))
        if tag not in self.content:
            self.content[tag] = [HTMLTag(tag, attrs)]
        else:
            self.content[tag].append(HTMLTag(tag, attrs))

    def handle_endtag(self, tag):
        pass
        #if tag == self.tag_stack[-1].name:


    def handle_startendtag(self, tag, attrs):
        self.add_tag(tag, attrs)
