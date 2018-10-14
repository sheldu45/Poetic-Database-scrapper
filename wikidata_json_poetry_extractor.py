import json

'''
descriptions
type   (item vs property)
id
aliases
labels
datatype
claims
'''
'''#first go for property name identification ! 
with open("wikidata-20161212-all.json") as f:
    for line in f:

        if len(line)>2:
            j_content = json.loads(line[:-2])
            #identifiant wikidata
            object_id = j_content["id"]
            #THIS TRIGGERS it concerns a property
            if object_id[:1] == "P":
                for k,v in j_content.items():
                    print(k)
                print("-----------------------")'''

#than go for object analysis
with open("wikidata-20161212-all.json") as f:
    for line in f:

        if len(line)>2:
            j_content = None
            try :
                j_content = json.loads(line[:-2])
            except(json.decoder.JSONDecodeError):
                print("Error at json line "+str(i)+" : "+line)
                    
            #descriptions (+ description français)
            object_lang2desc = j_content["descriptions"]
            object_fr_desc = ""
            if "fr" in object_lang2desc:
                dict_prov = object_lang2desc["fr"]
                object_fr_desc = dict_prov["value"]

            #identifiant wikidata
            object_id = j_content["id"]
            #print(object_id)

            #type wikidata
            object_type = j_content["type"]
            
            #print(object_fr_desc)

            #titres (+ titre français)
            object_lang2title = j_content["labels"]
            object_fr_title = ""
            if "fr" in object_lang2title:
                dict_prov = object_lang2title["fr"]
                object_fr_title = dict_prov["value"]
            #print(object_fr_title)

            #synonymes (+synonymes français)
            object_aliases = j_content["aliases"]
            object_fr_aliases = []
            if "fr" in object_aliases:
                for dic in object_aliases["fr"]:
                    object_fr_aliases.append(dic["value"])
            object_fr_aliases.insert(0, object_fr_title)
            #print(object_fr_aliases)
            
            printed = False
            dictclaims = j_content["claims"]
            for k,v in dictclaims.items():

                if not printed and k == "P31":   
                   listoccupation = v
                   for dict_object_occupation in listoccupation:
                        '''
                        mainsnak
                        id
                        rank
                        type
                        '''
                        dict_mainsnack = dict_object_occupation["mainsnak"]
                        '''
                        property
                        datavalue
                        datatype
                        snaktype
                        '''
                        try:
                            if dict_mainsnack["datavalue"]["value"]["id"] == "Q5185279":
                                for title in object_fr_aliases:
                                    if not len(title) == 0:
                                        print(title)
                                    printed = True
                        except(KeyError):
                            pass          

                elif not printed and k == "P31":   
                   listoccupation = v
                   for dict_object_occupation in listoccupation:
                        '''
                        mainsnak
                        id
                        rank
                        type
                        '''
                        dict_mainsnack = dict_object_occupation["mainsnak"]
                        '''
                        property
                        datavalue
                        datatype
                        snaktype
                        '''
                        try:
                            if dict_mainsnack["datavalue"]["value"]["id"] == "Q12308638":
                                for title in object_fr_aliases:
                                    if not len(title) == 0:
                                        print(title)
                                    printed = True
                        except(KeyError):
                            pass          
                            
                        #print("-----------------------")
            #print("-----------------------")
        

print("done")
