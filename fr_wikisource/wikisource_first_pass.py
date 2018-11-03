import re
import datetime

print(datetime.datetime.now())

reg_open_title = re.compile("<title>")
reg_close_title = re.compile("</title>")
reg_open_text = re.compile("<text")
reg_close_text = re.compile("</text>")
reg_pages_open = re.compile("<pages")
open_title = False
open_text = False
unclosed_tag = False

list_title_ready_wiki_source_poems = []
last_title = ""

output_file = open("first_pass", "w")

with open("/home/paprika/Documents/Git/Poetic-Database-scrapper/title_ready_wiki_source_poems") as f:
    for line in f:
        list_title_ready_wiki_source_poems.append(line[:-1])

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
                    if not last_title in list_title_ready_wiki_source_poems:
                        last_title = ""  
                    else:
                        output_file.write("<title>"+last_title+"</title>\n")
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

