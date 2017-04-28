from HTMLParser import HTMLParser


class HTMLTag:
    def __init__(self, tagname, attrs):
        self.begin_pos = None
        self.end_pos = None
        self.name = tagname
        if isinstance(attrs, dict):
            self.attrs = attrs
        else:
            self.attrs = dict(attrs)
        self.content = None
        
    def set_content(self, content):
        self.content = content
        
    def text(self):
        pass


class WebParser(HTMLParser):
    def __init__(self, data):
        HTMLParser.__init__(self)
        self.content = {' ': []}
        self.tag_stack = []
        self.last_tag = None
        self.feed(data)
        self.flag = 0

        
    def add_tag(self, tag, attrs):
        self.last_tag = HTMLTag(tag, attrs)
        
        if tag not in self.content:
            self.content[tag] = [self.last_tag]
        else:
            self.content[tag].append(self.last_tag)
        return self.last_tag

    def handle_starttag(self, tag, attrs):
        #self.tag_stack.append(HTMLTag(tag, attrs))
        self.flag = 0
        self.add_tag(tag, attrs).begin_pos = self.getpos()

    def handle_data(self, data):
        """
        recognize data, html content string
        :param data:
        :return:
        """
        if self.last_tag and self.flag:
            self.last_tag.set_content(data.strip())
           

    def handle_endtag(self, tag):
        self.flag = 1
        self.last_tag.end_pos = self.getpos()
        #if tag == self.tag_stack[-1].name:


    def handle_startendtag(self, tag, attrs):
        self.add_tag(tag, attrs)

    def find(self, tagname, attrs):
        for key, value in attrs.items():
            for tag in self.content[tagname]:
                if key in tag.attrs and value == tag.attrs[key]:
                    return tag
        return None
