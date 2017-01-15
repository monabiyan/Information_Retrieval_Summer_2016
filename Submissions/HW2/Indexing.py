
def query_prep():  # edits the query file and returns a list of edited queries

    path='/Users/mohsennabian/Dropbox/AP_DATA/query_desc.51-100.short.txt'
    import re
    f = open(path)
    next='1'
    query_list = []

    while next != "":
        next = f.readline()
        next = re.sub('^[0-9][0-9]..','',next)
        next = next.replace("  ",' ')
        next = next.replace('Document', '')
        next = next.replace('will', '')
        next = next.replace('report', '')
        next = next.replace('discuss', '')
        next = next.replace('identify', '')
        next = next.replace('describe', '')
        next = next.replace('must', '')
        next = next.replace('discuss', '')
        next = next.replace('how', '')
        next = next.replace('has', '')
        next = next.replace('have', '')
        next = re.sub('(\sof\s|\sor\s|\sin\s|\sor\s|\sand\s|\sto\s|\son\s|\sa\s|\san\s|\sby\s|\sthe\s|\san\s|\sa\s|\sany\s|\.$|\(|\)|\sat\s)', ' ', next)
        query_list.append(next)

    print(query_list[2])

    query_list1=range(0,25)    # initializing query_list1
    #query_list1[0] = 'allegations corrupt public officials governmental jurisdiction'
    query_list1[0] = ' corrupt government'
    query_list1[1] = 'weather fatality'
    query_list1[2] = 'prime rate '
    query_list1[3] = 'guerrilla'
    query_list1[4] = 'hostage'
    query_list1[5] = "military coup etat "
    query_list1[6] = 'Rifle   NRA '
    query_list1[7] = 'Iran Contra'
    query_list1[8] = 'rail strike '
    query_list1[9] = 'poach  '
    query_list1[10] = 'satellite contract '
    query_list1[11] = ' U.S. financial institution'
    query_list1[12] = 'crime cyber'
    query_list1[13] = 'noncommunist '
    query_list1[14] = ' OPEC '
    query_list1[15] = 'Israel Iran Contra '
    query_list1[16] = 'computer crime'
    query_list1[17] = 'safety manufacturing employees fibers insulation'
    query_list1[18] = 'MCI Bell'
    query_list1[19] = 'fiber optics technology'
    query_list1[20] = ' fiber optics '
    query_list1[21] = 'salary  pay seniority  job'
    query_list1[22] = '1988 presidential candidate'
    query_list1[23] = 'machine translation'
    query_list1[24] = 'U.S. Army  weapons '
    for index in range(0, 25):
        temp=query_list1[index].split(' ')
        temp=clean_wordlist(temp)
        temp=query_filter(temp, 4)           #filtering query
        query_list1[index]=[x for x in temp if x != '']
    return query_list1






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
        print(word)
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
# def proximity():
#     import re
#
#     log = 'loss of gene'
#     phrases = ['aquaporin protein', 'another protein']
#
#     with open('input.txt') as f_input:
#         for number, line in enumerate(f_input, start=1):
#             # Sanitise the line
#             text = ' '.join(re.findall( line.lower()))

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

    g = open('/Users/mohsennabian/Dropbox/AP_DATA/inverted_stmmed_stop/' + filename + 'inverted','r')
    g.seek(start)
    result=g.readline()
    result = result.replace('\n', '')
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
        filter_type=4
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
    g = open('/Users/mohsennabian/Dropbox/Summer_2016/Info_Retrieval/cs6200_Mohsen_Nabian/HW2/combine_all_inverted/' + 'combine_all_inv_files.txt','w')
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

        a=word_final.keys()  #list of document ids
        b=word_final.values() #list of list of locations
        c=[]

        for x in b:
            c.append(len(x))

        DK={}
        for i in range(0,len(a)):
            DK[a[i]]=[c[i]]

        sorted_DK = sorted(DK.items(), key=operator.itemgetter(1),reverse=True)   #[(doc_id,length)]


        txt = word + '/'




        for i in range(0, len(a)):
            occurance_list = word_final[sorted_DK[i][0]]
            doc_name=sorted_DK[i][0]
            doc_id_indexed=mapping_id[doc_name]
            #doc_id_indexed=g_doc_name_index.keys()[g_doc_name_index.values().index(sorted_DK[i][0])]
            txt = txt + str(doc_id_indexed).replace(' ', '') + str(occurance_list).replace(' ', '').replace("'",'') + ' '


        start_bit = g.tell()
        g.write(txt + '\n')
        end_bit = g.tell()
        location = [start_bit, end_bit]
        catalog_all[word]= location
    path2='/Users/mohsennabian/Dropbox/Summer_2016/Info_Retrieval/cs6200_Mohsen_Nabian/HW2/combine_all_inverted/catalog_all.txt'
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

def read_txt_file(path):
    f=open(path)
    TXT=f.read()
    word_list=TXT.split('\n')
    del word_list[-1]
    return(word_list)

########################################################################################
########################################################################################
########################################################################################
########################################################################################
########################################################################################
########################################################################################
########################################################################################
########################################################################################
########################################################################################
########################################################################################
########################################################################################
########################################################################################
def document_id_list():  #return a list of all document ids
    return(g_doc_name_index.values())

def term_search(word):
    myDict=read_inverted_files_using_cataloge_all(word)
    if myDict==0:
        return(0,[],[])
    document_ids=myDict.keys()
    tf=[]
    for i in range(0,len(document_ids)):
        tf.append(len(myDict.values()[i]))
    hit=sum(tf)
    return(hit,document_ids,tf)



def call_doc_length():
    path='/Users/mohsennabian/Dropbox/Summer_2016/Info_Retrieval/cs6200_Mohsen_Nabian/HW1/docs_length.txt'
    f = open(path)
    next='1'
    dict={}
    while next != "":
        next = f.readline()
        if next == '': break
        next = next.replace('\n', '')
        temp = next.split(',')
        dict[temp[1]]=float(temp[0])
    return(dict)



def ss(query_list,Document):
    for i in query_list:
        if i in Document:
            score=score+1


def kk(quey_list):
    kk=len(quey_list)

def term_search2(word):
    myDict=read_inverted_files_using_cataloge_all(word)
    if myDict==0:
        return(0,[],[])
    document_ids=myDict.keys()
    tf=[]
    for i in range(0,len(document_ids)):
        tf.append(len(myDict.values()[i]))
    hit=sum(tf)
    return(hit,document_ids,tf)


def Ranking2(query_list):
    ll=0.8
    import math
    k=kk(quey_list)
    s=ss(query_list, Document)
    Doc_length = call_doc_length()  # find Doc length as a dictionary
    Document_Number = Doc_length.keys()
    sum_length_all_Doc = sum(Doc_length.values())
    # id_list = call_id_list()

    all_query_okapi_tf = []
    all_query_tf_idf = []
    all_query_bm25 = []
    all_query_laplace_smoothing = []
    all_query_Jelinek_smoothing = []
    print(landa)
    for query in query_list:
        score_okapi_tf = {}
        score_tf_idf = {}
        score_bm25 = {}
        score_laplace_smoothing = {}
        score_Jelinek_smoothing = {}

        for id in Document_Number:
            score_okapi_tf[id] = 0
            score_tf_idf[id] = 0
            score_bm25[id] = 0
            score_laplace_smoothing[id] = 0
            score_Jelinek_smoothing[id] = 0
            score_proximity[id] = 0
        s=ss(query, Document)
        k=kk(quey)






def Ranking(query_list):  # return okapi_TF score of all documents with respect to word 'word'

    D = 84678
    V = 178081
    avgs_Docs_length = 166.0558
    k1 = 1.2
    k2 = 100
    b = 0.75
    tf_wq = 1
    landa=0.8

    ll=0.8
    kk=0.8

    import math

    Doc_length = call_doc_length()      #find Doc length as a dictionary
    Document_Number=Doc_length.keys()
    sum_length_all_Doc = sum(Doc_length.values())
    # id_list = call_id_list()

    all_query_okapi_tf = []
    all_query_tf_idf = []
    all_query_bm25 = []
    all_query_laplace_smoothing = []
    all_query_Jelinek_smoothing = []
    all_query_proximity=[]
    print(landa)
    for query in query_list:
        score_okapi_tf = {}
        score_tf_idf = {}
        score_bm25 = {}
        score_laplace_smoothing = {}
        score_Jelinek_smoothing = {}
        score_proximity= {}

        for id in Document_Number:
            score_okapi_tf[id] = 0
            score_tf_idf[id] = 0
            score_bm25[id] = 0
            score_laplace_smoothing[id] = 0
            score_Jelinek_smoothing[id] = 0
            score_proximity[id]=0

        for word in query:

            print(word)
            total_hit, doc_id, tf = term_search(word)
            print('done')

            for i in range(0, len(doc_id)):
                print(i, 'dodo')
                tf_wd = tf[doc_id.index(doc_id[i])]  # tf related to the

                prox=tf_wd




                score_proximity[doc_id[i]]= prox + score_proximity[doc_id[i]]

        import operator



        score_proximity_sorted=sorted(score_proximity.items(), key=operator.itemgetter(1), reverse=True)[0:1000]
        all_query_proximity.append(score_proximity_sorted)




    return ([], [], [], [], [],all_query_proximity)




def query_number_extract():

    path = '/Users/mohsennabian/Dropbox/AP_DATA/query_desc.51-100.short.txt'
    import re
    f = open(path)
    next = '1'
    query_list = []
    index=0
    q_no=[]
    while next != "":
        next = f.readline()
        print(next[0:2])
        q_no.append(next[0:2])

    return(q_no)



def write_results(query_list):
    q_no = query_number_extract()
    all_query_okapi_tf, all_query_tf_idf, all_query_bm25, all_query_laplace_smoothing, all_query_Jelinek_smoothing, all_query_proximity = Ranking(query_list)
    path = '/Users/mohsennabian/Dropbox/Summer_2016/Info_Retrieval/cs6200_Mohsen_Nabian/HW2/'

    # f = open(path + 'okapi_tf.txt', 'w')
    # for i in range(0, len(all_query_okapi_tf)):
    #     for j in range(0, len(all_query_okapi_tf[i])):
    #         stt = str(q_no[i]) + ' Q0 ' + str(all_query_okapi_tf[i][j][0]) + ' ' + str(j + 1) + ' ' + str(
    #             all_query_okapi_tf[i][j][1]) + ' Exp' + '\n'
    #         f.write(str(stt))
    # f.close()
    #
    # f = open(path + 'tf_idf.txt', 'w')
    # for i in range(0, len(all_query_tf_idf)):
    #     for j in range(0, len(all_query_tf_idf[i])):
    #         stt = str(q_no[i]) + ' Q0 ' + str(all_query_tf_idf[i][j][0]) + ' ' + str(j + 1) + ' ' + str(
    #             all_query_tf_idf[i][j][1]) + ' Exp' + '\n'
    #         f.write(str(stt))
    # f.close()
    #
    # f = open(path + 'bm25.txt', 'w')
    # for i in range(0, len(all_query_bm25)):
    #     for j in range(0, len(all_query_bm25[i])):
    #         stt = str(q_no[i]) + ' Q0 ' + str(all_query_bm25[i][j][0]) + ' ' + str(j + 1) + ' ' + str(
    #             all_query_bm25[i][j][1]) + ' Exp' + '\n'
    #         f.write(str(stt))
    # f.close()

    # f = open(path + 'laplace_smoothing.txt', 'w')
    # for i in range(0, len(all_query_laplace_smoothing)):
    #     for j in range(0, len(all_query_laplace_smoothing[i])):
    #         stt = str(q_no[i]) + ' Q0 ' + str(all_query_laplace_smoothing[i][j][0]) + ' ' + str(j + 1) + ' ' + str(
    #             all_query_laplace_smoothing[i][j][1]) + ' Exp' + '\n'
    #         f.write(str(stt))
    # f.close()
    #
    # f = open(path + 'Jelinek_smoothing.txt', 'w')
    # for i in range(0, len(all_query_Jelinek_smoothing)):
    #     for j in range(0, len(all_query_Jelinek_smoothing[i])):
    #         stt = str(q_no[i]) + ' Q0 ' + str(all_query_Jelinek_smoothing[i][j][0]) + ' ' + str(j + 1) + ' ' + str(
    #             all_query_Jelinek_smoothing[i][j][1]) + ' Exp' + '\n'
    #         f.write(str(stt))
    # f.close()
    f = open(path + 'proximity.txt', 'w')
    for i in range(0, len(all_query_proximity)):
        for j in range(0, len(all_query_proximity[i])):
            stt = str(q_no[i]) + ' Q0 ' + str(all_query_proximity[i][j][0]) + ' ' + str(j + 1) + ' ' + str(
                all_query_proximity[i][j][1]) + ' Exp' + '\n'
            f.write(str(stt))
    f.close()


########################################################################################
########################################################################################
########################################################################################
########################################################################################
########################################################################################
########################################################################################
########################################################################################
########################################################################################
########################################################################################
########################################################################################
########################################################################################
########################################################################################

def proximity(one_query_list):

    landa=0.8
    k=kkk()
    s=sss()
    catalog_path = '/Users/mohsennabian/Dropbox/Summer_2016/Info_Retrieval/cs6200_Mohsen_Nabian/HW2/combine_all_inverted/' + 'catalog.txt'
    catalog = read_dictionary(catalog_path)  # reads catalog from the hard disc  {filename:{word:[start,finish]}}


def main():

    global g_doc_name_index
    # doc_name_index_save()
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


    # merge_all()
    catalog_all_path = '/Users/mohsennabian/Dropbox/Summer_2016/Info_Retrieval/cs6200_Mohsen_Nabian/HW2/combine_all_inverted/catalog_all.txt'
    catalog_all=read_dictionary(catalog_all_path)




    # print(str(stemming_list(['variations'])[0]))
    # doc_hit, all_frequency = word_frequency(str(stemming_list(['cowell'])[0]))
    # print(str(doc_hit) + '  doc_hit')
    # print(str(all_frequency) + '  all_frequency')
    #


    # combine_all_inv_files()
    # print(catalog_all['Iran']
    #
    # word_list=read_txt_file('/Users/mohsennabian/Desktop/in.1')
    # g=open('/Users/mohsennabian/Dropbox/Summer_2016/Info_Retrieval/cs6200_Mohsen_Nabian/HW2/index_result_demo.txt','w')
    # i=0
    # for word in word_list:
    #     i=i+1
    #     print(i/75000 *100)
    #     stemed_word=stemming_list([word ])[0]
    #     doc_hit, all_frequency = word_frequency(stemed_word)
    #     g.write(word+' '+str(doc_hit)+ ' '+str(all_frequency)+'\n')
    #


    #
    query_list = query_prep()
    print((query_list))
    query_number_extract()
    write_results((query_list))

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