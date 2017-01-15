def stopwords_load():
    global stop_list
    stop_list=[]
    # find stop_list
    stoplist_path = '/Users/mohsennabian/Dropbox/AP_DATA/stoplist.txt'
    stop_list_f = open(stoplist_path)
    stop_list = stop_list_f.read().replace('\n', ' ').split(' ')

########################################################################################
########################################################################################
########################################################################################
########################################################################################



def stopwords_remove(word_list):
    newlist=[]
    for i in range(0, len(word_list)):
        if word_list[i] not in stop_list:
            newlist.append(word_list[i])  # removes the stopwords from the list
    return(newlist)


########################################################################################
########################################################################################
########################################################################################
########################################################################################


def clean_wordlist(str_list):
    import re
    newlist = []
    for word in str_list:

        match = re.search(r'\w+(\.?\w+)*', word)
        if match:
            newlist.append(match.group().lower())  ## we also make it all lower case here .lower()
    return(newlist)


########################################################################################
########################################################################################
########################################################################################
########################################################################################

def stemming_list(word_list):
    # steming a word
    stemmed_list=[]
    from stemming.porter2 import stem
    for word in word_list:
        stemmed_list.append(stem(word))
    return(stemmed_list)



########################################################################################
########################################################################################
########################################################################################
########################################################################################
def doc_name_index_save():
    global g_doc_name_index
    g_doc_name_index = {}
    ids=[]
    path = '/Users/mohsennabian/Dropbox/AP_DATA/ap89_collection'  # path address of all document files
    import os
    h=0
    for filename in os.listdir(path):
        if filename == '.DS_Store':
            continue
        fileaddress = path + '/' + filename
        d=extract_data(fileaddress, 1)
        for i in range(0,len(d.keys())):
            g_doc_name_index[str(h)]=d.keys()[i]
            h = h + 1
            print(str(h)+' '+str(d.keys()[i]))
    path='/Users/mohsennabian/Dropbox/Summer_2016/Info_Retrieval/cs6200_Mohsen_Nabian/HW2/combine_all_inverted/' + 'doc_name_index.txt'
    save_dictionary(path, g_doc_name_index)



def doc_name_index_upload():
    global g_doc_name_index
    g_doc_name_index = {}
    path='/Users/mohsennabian/Dropbox/Summer_2016/Info_Retrieval/cs6200_Mohsen_Nabian/HW2/combine_all_inverted/' + 'doc_name_index.txt'
    g_doc_name_index=read_dictionary(path)
    return(g_doc_name_index)
########################################################################################
########################################################################################
########################################################################################
########################################################################################


def extract_data(file_address, filter_type):
    stopwords_load()
    from BeautifulSoup import BeautifulSoup


    all_documents = {}

    f = open(file_address)

    f_txt=f.read()

    soup = BeautifulSoup(f_txt)

    # print type(soup)
    # print soup.prettify()

    DOCS = soup.findAll('doc')

    doc_dict={}

    for DOC in DOCS:
        txt=''
        doc_id=DOC.findAll('docno')[0].text
        TEXTS=DOC.findAll('text')
        for TEXT in TEXTS:
            txt=txt+str(TEXT.text)

        txt = txt.split(' ')
        txt = clean_wordlist(txt)     #filters with '\w+(\.?\w+)*' reg.expression and make it lower case



        if filter_type== 1:
            pass

        if filter_type == 2:     #stopwords are removed
            txt=stopwords_remove(txt)



        if filter_type == 3:     #words are stemmed
            txt=stemming_list(txt)


        if filter_type == 4:  # removes the stopwords and stemmed
            txt=stopwords_remove(txt)
            txt = stemming_list(txt)

        doc_dict[doc_id] = txt


    return(doc_dict)

########################################################################################
########################################################################################
########################################################################################
########################################################################################


def query_filter(querylist,filter_type):

    if filter_type == 1:
        pass

    if filter_type == 2:  # stopwords are removed
        querylist = stopwords_remove(querylist)

    if filter_type == 3:  # words are stemmed
        querylist = stemming_list(querylist)

    if filter_type == 4:  # removes the stopwords and stemmed
        querylist = stopwords_remove(querylist)
        querylist = stemming_list(querylist)

    return(querylist)



########################################################################################
########################################################################################
########################################################################################
########################################################################################





# def read_documents(fileaddress):    # extracts documents body and their ids from a bunch of files in the given address
#
#     Document_Number = []
#     Document_Content = []
#     TXT = ''
#     index = 0
#     index2=0
#
#     import os
#
#
#     f = open(fileaddress)
#     TXT = 'filebeginingomid1'
#     next = '1'
#     while next != "":
#         next = f.readline()
#
#         if ('<DOC>' in next):
#             new_doc=True
#
#         if ("<DOCNO>" in next) | ("</DOCNO>" in next):
#
#
#             index = index + 1
#             pure_next = next.replace("<DOCNO>", '')
#             pure_next = pure_next.replace("</DOCNO>", '')
#             pure_next = pure_next.replace("\n", '')
#             pure_next = pure_next.replace(" ", '')
#             Document_Number.append(pure_next)
#
#
#             print(index)
#         if ('</DOC>' in next):
#
#             TXT = TXT.replace("</DOC>",'')
#             TXT = TXT.replace("<DOC>", '')
#             TXT = TXT.replace("<NOTE>", '')
#             TXT = TXT.replace("</NOTE>", '')
#             TXT = TXT.replace("</DOCNO>", '')
#             TXT = TXT.replace("<DOCNO>", '')
#             TXT = TXT.replace("</HEAD>", '')
#             TXT = TXT.replace("'", '')
#             TXT = TXT.replace("`", '')
#             TXT = TXT.replace(Document_Number[index-1], '')
#             Document_Content.append(TXT)
#             index2=index2+1
#             TXT=''
#         if ('<FILEID>' in next) | ('<FIRST>' in next)|('<SECOND>' in next)|('<HEAD>' in next)|('<BYLINE>' in next)\
#                 |('<DATELINE>' in next)|('<TEXT>' in next)|('</TEXT>' in next):
#             continue
#
#         else:
#             TXT = TXT + ' ' + next.replace("\n", '')
#
#     print(len(Document_Content), len(Document_Number))
#
#     Doc_dic={}
#     for i in range(0,len(Document_Content)):
#         Doc_dic[Document_Number[i]]=Document_Content[i]
#
#     return (Document_Content, Document_Number,Doc_dic)


########################################################################################
########################################################################################
########################################################################################
########################################################################################

def tf_dictionary(doc_txt):    #gets one doc_cont (string) and one doc_id (string)


    import collections
    tf_txt = collections.Counter(doc_txt)    #counts the word frequency in the document
    tf_txt = dict(tf_txt)
    return (tf_txt)      # returns:  doc_id_cont={doc_id:{term_id1:freq,term_id2:freq,...}}

########################################################################################
########################################################################################
########################################################################################
########################################################################################

def location_occurance_list(word,txt_list):           #returns a list of locations of a word in txt list
    locations=([i for i, x in enumerate(txt_list) if x == word])
    return locations
########################################################################################
########################################################################################
########################################################################################
########################################################################################


def tokenize2(Document_Content, Document_Number,filename):   # 1) write converted file for each filename
    word_general_dict={}                                                     # 2) Populate global variable catalog for the inverted files
    for i in range(0,len(Document_Number)):
        print(i)
        doc_txt=Document_Content[i]
        doc_id= Document_Number[i]
        tf=tf_dictionary(doc_txt)    #a dictionary of TF for all words
        #  pattern for word=Iran   "doc_id[tf(1,2,3)] doc_id2[tf(1,2,3)] ..."
        doc_id_index = g_doc_name_index.keys()[g_doc_name_index.values().index(doc_id)]  #recieve the indexed doc_id (string)

        for word in  tf.keys():  #words in the doc_id
            location_list = location_occurance_list(word, doc_txt)
            if word not in word_general_dict.keys():
                word_general_dict[word]={}
            if tf[word] not in word_general_dict[word].keys():
                word_general_dict[word][tf[word]]={}
            if  doc_id_index not in word_general_dict[word][tf[word]].keys():
                word_general_dict[word][tf[word]][doc_id_index]={}
            word_general_dict[word][tf[word]][doc_id_index]=location_list

            #
            # word_general_dict[word]=tf
            # word_general_dict[word][tf]={}
            # word_general_dict[word][tf][doc_id_index]=location_list


    g=open('/Users/mohsennabian/Dropbox/AP_DATA/inverted'+filename+'inverted','w')
    catalog[filename]={}
    import collections
    for word in word_general_dict.keys() :
        if word=='sampleword':
            continue
        word_info=word_general_dict[word]
        #tf_sorted_word_info =collections.OrderedDict(sorted(word_info.items(),reverse=True))
        tf_sorted_word_info = word_info
        txt = word+ '/'
        for tf_value in tf_sorted_word_info.keys():
            for doc_id_value in tf_sorted_word_info[tf_value].keys():
                occurance_list=tf_sorted_word_info[tf_value][doc_id_value]
                txt=txt+doc_id_value+str(occurance_list).replace(' ','')+' '
        start_bit = g.tell()
        g.write(txt+'\n')
        end_bit=g.tell()
        location=[start_bit,end_bit]
        catalog[filename][str(word)] = location


########################################################################################
########################################################################################
########################################################################################
########################################################################################

def set_globvar():
    global catalog
    global catalog_all   # Needed to modify global copy of globvar
    catalog = {}
    catalog_all={}

########################################################################################
########################################################################################
########################################################################################
########################################################################################

def read_inverted_files_using_cataloge (filename,word):    #returns a list of (doc_id,tf) for a filename and a wrod

    import re
    start=catalog[filename][word][0]

    finish = catalog[filename][word][1]

    g = open('/Users/mohsennabian/Dropbox/AP_DATA/inverted'+filename+'inverted','r')
    g.seek(start)
    result=g.readline()
    result = result.replace('\n', '')
    print(result)
    word_s=result.split('/')[0]
    list_s= result.split('/')[1].split(' ')
    i=0
    doc_id_indexed=[]
    locations_word=[]
    dict={}
    for item in list_s:
        # print (item)
        doc_id_indexed=item.split('[')[0]
        # print(doc_id_indexed)
        if doc_id_indexed == '':
            continue
        doc_id=g_doc_name_index[doc_id_indexed]   #g_doc_name_index is a global dictionary uploaded from main()
        locations_word=item.split('[')[1].replace(']','').split(',')
        dict[doc_id]=locations_word

    # list_result=re.split(': ',result)[1]

    # import ast
    # final = ast.literal_eval(list_result)
    return(dict)   #return a dictionary with keys=doc_id  and values=a list of occurances of the word for each doc_id

########################################################################################
########################################################################################
########################################################################################
########################################################################################

def read_inverted_files_using_cataloge_all (word):    #returns a list of (doc_id,tf) for a filename and a wrod
    if (word) in catalog_all.keys():
        import re
        start=catalog_all[word][0]

        finish = catalog_all[word][1]

        g = open('/Users/mohsennabian/Dropbox/Summer_2016/Info_Retrieval/cs6200_Mohsen_Nabian/HW2/combine_all_inverted/combine_all_inv_files.txt','r')
        g.seek(start)
        result=g.readline()
        result = result.replace('\n', '')
        word_s = result.split('/')[0]
        list_s = result.split('/')[1].split(' ')
        i=0
        doc_id_indexed=[]
        locations_word=[]
        dict={}
        for item in list_s:
            # print (item)
            doc_id_indexed=item.split('[')[0]
            # print(doc_id_indexed)
            if doc_id_indexed == '':
                continue
            doc_id=g_doc_name_index[doc_id_indexed]   #g_doc_name_index is a global dictionary uploaded from main()
            locations_word=item.split('[')[1].replace(']','').split(',')
            dict[doc_id]=locations_word

        # list_result=re.split(': ',result)[1]

        # import ast
        # final = ast.literal_eval(list_result)
        return(dict)   #return a dictionary with keys=doc_id  and values=a list of occurances of the word for each doc_id
    else :
        return(0)
########################################################################################
########################################################################################
########################################################################################
########################################################################################

# def write_catalog_intofile():
#     g = open('/Users/mohsennabian/Dropbox/Summer_2016/Info_Retrieval/cs6200_Mohsen_Nabian/HW2/combine_all_inverted/' + filename + 'inverted','r')
#
#     for file  in catalog.keys():
#         for word in catalog[file]:
#             g.write()




def creat_all_inverted_files_and_save_catalog(path):

    import os
    h=0
    for filename in os.listdir(path):
        if filename=='.DS_Store':
            continue
        h=h+1
        print('folder number:  '+str(h))
        fileaddress = path + '/' + filename
        print(fileaddress)


        filter_type=2


        Doc_dic = extract_data(fileaddress, filter_type)


        Document_Number=Doc_dic.keys()

        Document_Content=Doc_dic.values()

        tokenize2(Document_Content, Document_Number, filename)  #creat one inverted file for each file and populate dict
    catalog_path = '/Users/mohsennabian/Dropbox/Summer_2016/Info_Retrieval/cs6200_Mohsen_Nabian/HW2/combine_all_inverted/' + 'catalog.txt'
    save_dictionary(catalog_path, catalog)  # saves catalog inside the hard disc
########################################################################################
########################################################################################
########################################################################################
########################################################################################



def save_dictionary(path,data):
    print('saving catalog...')
    #open('u.item', encoding="utf-8")
    import json
    with open(path,'w') as outfile:
        json.dump(data, fp=outfile)
    # save to file:
    print(' catalog saved')
########################################################################################
########################################################################################
########################################################################################
########################################################################################

def read_dictionary(path):
    import json
    # load from file:
    g = open(path, 'r')
    print('reading ...')

    try:
        data = json.load(g)
    # if the file is empty the ValueError will be thrown
    except ValueError:
        data = {}
    print('reading finished!')
    return(data)
########################################################################################
########################################################################################
########################################################################################
########################################################################################

# def combine_all_inv_files():
#     print('combining all inverted files to one file...')
#     wordlist=[]
#     files=catalog.keys()
#     g = open('/Users/mohsennabian/Dropbox/Summer_2016/Info_Retrieval/cs6200_Mohsen_Nabian/HW2/combine_all_inverted/' + 'combine_all_inv_files.txt', 'w')
#     print('making all words as one wordlist...')
#     for file in files:
#         words=catalog[file].keys()
#         for word in words:
#             wordlist.append(word)
#     wordlist = list(set(wordlist))  ##keeps terms unique
#
#     print('wordlist is fully recorded')
#     print(len(wordlist))
#
#     for word in wordlist:
#         word_final=[]
#         for file in files:
#             if word in catalog[file].keys():
#                 a=read_inverted_files_using_cataloge(file,word)
#                 word_final=word_final+a
#         word_final=sorted(word_final, key=lambda x: x[1])  #this will sort a list of tuples based on the tuples second value(tf)
#         start_bit = g.tell()
#         g.write(str(word) + ': ' + str(word_final) + '\n')
#         end_bit = g.tell()
#         location = [start_bit, end_bit]
#         catalog_all[word] = location
#         print(word)

########################################################################################
########################################################################################
########################################################################################
########################################################################################


def merge_all():
    print('merging..')
    path = '/Users/mohsennabian/Dropbox/AP_DATA/ap89_collection'  # path address of all document files
    import os
    h = 0
    all_filename = os.listdir(path)
    print('combining all inverted files to one file...')
    wordlist = []
    files = catalog.keys()
    g = open('/Users/mohsennabian/Dropbox/Summer_2016/Info_Retrieval/cs6200_Mohsen_Nabian/HW2/combine_all_inverted/' + 'combine_all_inv_files2.txt','w')
    print('making all words as one wordlist...')

    for file in files:
        words = catalog[file].keys()
        for word in words:
            wordlist.append(word)
    wordlist = list(set(wordlist))  ##keeps terms unique
    print(len(wordlist))


    id_index = g_doc_name_index.keys()
    id_fullname = g_doc_name_index.values()
    mapping_id = dict(zip(id_fullname, id_index))



    print('wordlist is fully recorded')
    # print(len(wordlist))
    import operator
    for word in wordlist:
        print(word)
        word_final = {}
        for file in files:
            if word in catalog[file].keys():
                a = read_inverted_files_using_cataloge(file, word)
                word_final.update(a)    #combined dictionaries  {doc_id:[location]}

        print('hiii')
        a=word_final.keys()  #list of document ids
        b=word_final.values() #list of list of locations
        c=[]

        for x in b:
            c.append(len(x))

        DK={}
        for i in range(0,len(a)):
            DK[a[i]]=[c[i]]

        sorted_DK = DK   #[(doc_id,length)]


        txt = word + '/'




        for i in range(0, len(a)):
            occurance_list = word_final[a[i]]
            doc_name=a[i]
            doc_id_indexed=mapping_id[doc_name]
            #doc_id_indexed=g_doc_name_index.keys()[g_doc_name_index.values().index(sorted_DK[i][0])]
            txt = txt + str(doc_id_indexed).replace(' ', '') + str(occurance_list).replace(' ', '').replace("'",'') + ' '


        start_bit = g.tell()
        g.write(txt + '\n')
        end_bit = g.tell()
        location = [start_bit, end_bit]
        catalog_all[word]= location
    path2='/Users/mohsennabian/Dropbox/Summer_2016/Info_Retrieval/cs6200_Mohsen_Nabian/HW2/combine_all_inverted/catalog_all2.txt'
    save_dictionary(path2, catalog_all)





########################################################################################
########################################################################################
########################################################################################
########################################################################################





def word_frequency(word):

    if read_inverted_files_using_cataloge_all(word)==0 :
        return(0,0)
    else:
        l=(read_inverted_files_using_cataloge_all(word)).values()
        sums=0
        for i in l:
            sums=sums+len(i)

        all_frequency=sums

        doc_hit=len(l)

        return(doc_hit,all_frequency)

########################################################################################
########################################################################################
########################################################################################
########################################################################################

def read_txt_file():
    f=open('/Users/mohsennabian/Dropbox/Summer_2016/Info_Retrieval/cs6200_Mohsen_Nabian/HW2/in.0.50.txt')
    TXT=f.read()
    word_list=TXT.split('\n')
    del word_list[-1]
    return(word_list)


def main():
    global g_doc_name_index
    #doc_name_index_save()
    g_doc_name_index = doc_name_index_upload()


    stopwords_load()      #it is saved in a global variable stop_list


    global catalog
    global catalog_all  # Needed to modify global copy of globvar
    catalog = {}
    catalog_all = {}


    # path = '/Users/mohsennabian/Dropbox/AP_DATA/ap89_collection'    #path address of all document files
    # creat_all_inverted_files_and_save_catalog(path)    #Creat inverted file for each document file and one cataloge for entire


    catalog_path = '/Users/mohsennabian/Dropbox/Summer_2016/Info_Retrieval/cs6200_Mohsen_Nabian/HW2/combine_all_inverted/' + 'catalog.txt'
    catalog=read_dictionary(catalog_path)    #reads catalog from the hard disc  {filename:{word:[start,finish]}}

    # print((catalog)['ap890101']['four'])
    # print(read_inverted_files_using_cataloge('ap890101', 'soviet'))


    merge_all()
    catalog_all_path = '/Users/mohsennabian/Dropbox/Summer_2016/Info_Retrieval/cs6200_Mohsen_Nabian/HW2/combine_all_inverted/catalog_all2.txt'
    catalog_all=read_dictionary(catalog_all_path)

    # print(str(stemming_list(['variations'])[0]))
    #
    #
    #
    # doc_hit, all_frequency = word_frequency(str(stemming_list(['cowell'])[0]))
    # print(str(doc_hit) + '  doc_hit')
    # print(str(all_frequency) + '  all_frequency')
    #
    #
    #
    # # combine_all_inv_files()
    # # print(catalog_all['Iran'])
    #
    # word_list=read_txt_file()
    # g=open('/Users/mohsennabian/Dropbox/Summer_2016/Info_Retrieval/cs6200_Mohsen_Nabian/HW2/index_result.txt','w')
    # for word in word_list:
    #     print (word)
    #     stemed_word=stemming_list([word ])[0]
    #     doc_hit, all_frequency = word_frequency(stemed_word)
    #     g.write(word+' '+str(doc_hit)+ ' '+str(all_frequency)+'\n')

###########################################












if __name__ == "__main__":

        main()

        # global catalog
        # global catalog_all  # Needed to modify global copy of globvar
        # catalog = {}
        # catalog_all = {}
        # xmlparse()

        #doc_name_index_save()

        # read_cataloge('ap890102','marching')



        #beauty_soup()

        #print(catalog)
        #doc_id_cont=tokenize1("Hi, my omid's name is Omid","2")
       #print(doc_id_cont)
       #test3()
       # test1()
       # a,b=BS()
       # print(a,b)
       # regexp()