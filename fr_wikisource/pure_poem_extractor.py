import re
import datetime

print(datetime.datetime.now())

reg_open_poem = re.compile("<poem")
reg_close_poem = re.compile("</poem>")
open_poem = False
printLine = False

output_file = open("pure_poesie", "w")

for i in range(0,2):
    source = ""
    if  i == 0:
        source = "deuxieme_pass"
    if i == 1:
        source = "deuxieme_pass"
    with open("/home/paprika/Documents/Git/Poetic-Database-scrapper/fr_wikisource/"+source) as f:
        for line in f:
            printLine = False

            open_poem_matcher = reg_open_poem.search(line)
            if not open_poem_matcher == None:
                open_poem = True
                line = line[len(line)-line[::-1].find('>')+1:]
                printLine = True

            if len(line)>0:
                line = line[:-1]

            close_poem_matcher = reg_close_poem.search(line)            
            if not close_poem_matcher == None:
                open_poem = False
                line = line[:close_poem_matcher.start()]

            if open_poem or printLine:
                if not len(line) == 0:
                    output_file.write(line+"\n")
            

output_file.close()
