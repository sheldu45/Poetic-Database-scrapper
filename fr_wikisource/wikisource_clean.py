import json
import re

reg_dont_print = re.compile("(<[^/]+>|[ ]+</.+>)")
reg_print_quand_meme = re.compile("<title>")
sauf_que_la_dont_print_quan_meme = re.compile("<title>MediaWiki:")

printed = False
opened_text = False

open_file_title_corpus_wikisource = open("title_wikisource_page", "w")

list_title = []

with open("frwikisource-20181001-pages-articles-multistream.xml") as f:
    for line in f:
        printed = False
        if opened_text and reg_dont_print.search(line) == None:
            #print(line, end = "")
            printed = True
        if not sauf_que_la_dont_print_quan_meme.search(line) == None:
            printed = True
        if not printed and not reg_print_quand_meme.search(line) == None:
            left_subs = line.index(">")+1
            right_subs = len(line)-line[::-1].index("<")-1
            list_title.append(line[left_subs:right_subs])
            opened_text = True

sorted_list_title = sorted(list_title)
for title in sorted_list_title:
    open_file_title_corpus_wikisource.write(title+"\n")

open_file_title_corpus_wikisource.close()
'''
with open("frwikisource-20181001-pages-articles-multistream.xml") as f:
    for line in f:
        printed = False
        if opened_text and reg_dont_print.search(line) == None:
            #print(line, end = "")
            printed = True
        if not sauf_que_la_dont_print_quan_meme.search(line) == None:
            printed = True
        if not printed and not reg_print_quand_meme.search(line) == None:
            left_subs = line.index(">")+1
            right_subs = len(line)-line[::-1].index("<")-1
            print(line[left_subs:right_subs])
            opened_text = True
'''
            
       
            
