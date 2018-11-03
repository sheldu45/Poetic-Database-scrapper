import re
import datetime

print(datetime.datetime.now())

class FirstPassReader():
    
    reg_page_open = re.compile("<[ ]*pages")
    reg_close_tag = re.compile("/>")
    reg_space = re.compile("[_]+")
    reg_alpha_num = re.compile("[0-9]")
    
    list_title_ready_wiki_source_poems2 =  {}

    def __init__(self):
        pass

    def parse(self):
        with open("/home/paprika/Documents/Git/Poetic-Database-scrapper/fr_wikisource/first_pass") as f:
            for line in f:
                try:
                    match_reg_page_open = self.reg_page_open.search(line)
                    if not match_reg_page_open == None:
                        line = line[match_reg_page_open.end()+1:self.reg_close_tag.search(line).start()-1]                  
                        normalised_line = ""
                        open_guillemets = False
                        for c in line:
                            if c == '"':
                                if open_guillemets :
                                    open_guillemets = False
                                else:
                                    open_guillemets = True
                            if not open_guillemets and c == " ":
                                normalised_line += "_"
                            else:
                                normalised_line += c
                        val_tab = self.reg_space.split(normalised_line)
                        key2v = {}
                        for val in val_tab:
                            if not val.find("=") == -1:
                                splitted = val.split('=')
                                key2v[splitted[0]] = splitted[1]
                        index = key2v["index"].strip('"')
                        start_page = ""
                        #from
                        if "from" in key2v:        
                            start_page_brut = key2v["from"]
                            for c in start_page_brut:
                                if not self.reg_alpha_num.search(str(c)) == None:
                                    start_page += c
                        end_page = start_page
                        #to
                        if "to" in key2v:
                            end_page_brut = key2v["to"]
                            end_page = ""
                            for c in end_page_brut:
                                if not self.reg_alpha_num.search(str(c)) == None:
                                    end_page += c
                        
                        try:                     
                            start_page = int(start_page)
                            end_page = int(end_page)
                            couple = (start_page, end_page)
                            final_title = "Page:"+index+"/"
                            if not final_title in self.list_title_ready_wiki_source_poems2:
                                self.list_title_ready_wiki_source_poems2[final_title] = []
                            self.list_title_ready_wiki_source_poems2[final_title].append(couple)
                        except(ValueError):
                            print(val_tab)
                            pass
                except(KeyError):
                    print(line)
                    pass






'''class MyHandler (xml.sax.ContentHandler):

    def __init__(self):
        xml.sax.ContentHandler.__init__(self)

    def startElement( self, name, attrs):
        #print("Element start: " + str((name, len(attrs))))       
        if name == 'page':
          print("Element start: " + str((name, len(attrs))))

    def endElement( self, name):
        #print("Element end: " +str(name))
        if name == 'title':
            self.encountered_open_title = False
        elif name == 'text':
            self.encountered_open_text = False
            if self.last_title in self.list_title_ready_wiki_source_poems:
                print("</text>")
        pass

    def characters(self, data):
        pass
        if self.encountered_open_title:
            self.last_title = data
            if self.last_title in self.list_title_ready_wiki_source_poems:
                print(str("<title>")+str(data)+str("</title>"))
        elif self.encountered_open_text and self.last_title in self.list_title_ready_wiki_source_poems:
            print(str(data), end="")
'''

'''filename = "/home/paprika/Documents/Git/Poetic-Database-scrapper/fr_wikisource/first_pass"
handler = MyHandler()
xml.sax.parse(filename, handler)'''

fpr = FirstPassReader()
fpr.parse()
#print(fpr.list_title_ready_wiki_source_poems2["Page:Sully Prudhomme - Poésies 1866-1872, 1872.djvu/"])
#print(fpr.list_title_ready_wiki_source_poems2)

reg_open_title = re.compile("<title>")
reg_close_title = re.compile("</title>")
reg_open_text = re.compile("<text")
reg_close_text = re.compile("</text>")
reg_pages_open = re.compile("<pages")
open_title = False
open_text = False
unclosed_tag = False

last_title = ""

output_file = open("deuxieme_pass", "w")

with open("/home/paprika/Documents/Git/Poetic-Database-scrapper/fr_wikisource/frwikisource-20181001-pages-articles-multistream.xml") as f:
    for line in f:
        #search <title> tag when title is not open 
        if not open_title:
            open_title_matcher = reg_open_title.search(line)
            if not open_title_matcher == None:
                close_title_matcher = reg_close_title.search(line)
                #title is in only one line
                if not close_title_matcher == None:
                    last_title = line[open_title_matcher.end():close_title_matcher.start()]
                    splitted_title = last_title.split("/")
                    page_index = splitted_title.pop()
                    if len(page_index) >0:
                        last_title = "/".join(splitted_title)+"/"
                        lastTitleIsListed = False
                        if last_title in fpr.list_title_ready_wiki_source_poems2: 
                            page_index = int(page_index)
                            list_couples = fpr.list_title_ready_wiki_source_poems2[last_title]
                            for couple in list_couples:
                                (a,b) = couple
                                if page_index >= a and page_index<= b:
                                    lastTitleIsListed = True
                    if not lastTitleIsListed:
                        last_title = "" 
                    else:
                        output_file.write("<title>"+last_title+str(page_index)+"</title>\n")
                        open_title = True
                
        #search opening <text> tag
        if open_title:
            #waiting for open <text> tag
            if not open_text:
                open_text_matcher = reg_open_text.search(line)
                #<text> open
                if not open_text_matcher == None:     
                    open_text = True  
                    close_text_matcher = reg_close_text.search(line)
                    #text content is in only one line
                    if not close_text_matcher == None:
                        #print("<text>"+line[open_text_matcher.end():close_text_matcher.start()]+"</text>")    
                        open_title = False  
                        open_text = False
                        line = line[line.find(">")+1:close_text_matcher.start()]
                        line = line.replace("&lt;", "<").replace("&gt;", ">").replace("&quot;","\"").replace("&amp;","&")
                        suppl_backspace = "\n"
                        if not reg_pages_open.search(line) == None and line.find(">") == -1:
                            unclosed_tag = True
                            line = line[:-1]
                        elif unclosed_tag:
                            if not line.find(">") == -1:
                                unclosed_tag = False
                            else:
                                line = line[:-1]
                        output_file.write("<text>\n"+line+"</text"+suppl_backspace)
                    else:
                        line = line[line.find(">")+1:]
                        line = line.replace("&lt;", "<").replace("&gt;", ">").replace("&quot;","\"").replace("&amp;","&")
                        suppl_backspace = "\n"
                        if line.find("<") > line.find(">"):
                            suppl_backspace = ""
                        if not reg_pages_open.search(line) == None and line.find(">") == -1:
                            unclosed_tag = True
                            line = line[:-1]
                        elif unclosed_tag:
                            if not line.find(">") == -1:
                                unclosed_tag = False
                            else:
                                line = line[:-1]
                        output_file.write("<text>\n"+line+suppl_backspace)
            #waiting for </text> tag
            else:
                close_text_matcher = reg_close_text.search(line)
                #whole line
                if close_text_matcher == None:
                    line = line.replace("&lt;", "<").replace("&gt;", ">").replace("&quot;","\"").replace("&amp;","&")
                    if not reg_pages_open.search(line) == None and line.find(">") == -1:
                        unclosed_tag = True
                        line = line[:-1]
                    elif unclosed_tag:
                        if not line.find(">") == -1:
                            unclosed_tag = False
                        else:
                            line = line[:-1]
                    output_file.write(line)
                #text end tag found        
                else:
                    open_text = False 
                    open_title = False
                    line = line[:close_text_matcher.start()]
                    line = line.replace("&lt;", "<").replace("&gt;", ">").replace("&quot;","\"").replace("&amp;","&")
                    suppl_backspace = "\n"
                    if line.find("<") > line.find(">"):
                        suppl_backspace = ""
                    output_file.write(line+"</text>"+suppl_backspace)

output_file.close()
print(datetime.datetime.now())

