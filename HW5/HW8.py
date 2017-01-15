########################################################################################
########################################################################################
########################################################################################
########################################################################################
class AutoVivification(dict):
    """Implementation of perl's autovivification feature."""
    def __getitem__(self, item):
        try:
            return dict.__getitem__(self, item)
        except KeyError:
            value = self[item] = type(self)()
            return value
#dict = AutoVivification()
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
def lists_sort(list1,list2,list3):
    zipped_lists = zip(list1, list2, list3)
    zip_sorted = sorted(zipped_lists, reverse=True)
    list11 = [list1 for (list1,list2,list3) in zip_sorted]
    list22= [list2 for (list1,list2,list3) in zip_sorted]
    list33= [list3 for (list1,list2,list3) in zip_sorted]
    return(list11,list22,list33)
########################################################################################
########################################################################################
########################################################################################
########################################################################################
def extract_txt(file_id_list):
    root_address= '/Users/mohsennabian/Datasets/AP_DATA/ap89_collection/'
    import os
    i=0
    doc_dict = {}
    for filename in os.listdir(root_address):
        i=i+1
        print(i)
        if filename == '.DS_Store': continue
        print(filename)
        file_address = root_address + filename
        from BeautifulSoup import BeautifulSoup
        f = open(file_address)
        f_txt=f.read()
        soup = BeautifulSoup(f_txt)
        DOCS = soup.findAll('doc')
        for DOC in DOCS:
            txt=''
            doc_id=DOC.findAll('docno')[0].text
            if doc_id in file_id_list:
                TEXTS=DOC.findAll('text')
                for TEXT in TEXTS:
                    txt = txt + str(TEXT.text)
                doc_dict[doc_id] = txt
    return(doc_dict)



########################################################################################
########################################################################################
########################################################################################
########################################################################################





def extract_all_txt():
    root_address= '/Users/mohsennabian/Datasets/AP_DATA/ap89_collection/'
    import os
    i=0
    doc_dict = {}
    for filename in os.listdir(root_address):
        i=i+1
        print(i)
        if filename == '.DS_Store': continue
        print(filename)
        file_address = root_address + filename
        from BeautifulSoup import BeautifulSoup
        f = open(file_address)
        f_txt=f.read()
        soup = BeautifulSoup(f_txt)
        DOCS = soup.findAll('doc')
        for DOC in DOCS:
            txt=''
            doc_id=DOC.findAll('docno')[0].text
            TEXTS=DOC.findAll('text')
            for TEXT in TEXTS:
                txt = txt + str(TEXT.text)
                txt=clean_text(txt)
            doc_dict[doc_id] = txt
    save_dictionary('/Users/mohsennabian/Datasets/AP_DATA/hw8_partB.txt', doc_dict)
    return(doc_dict)
########################################################################################
########################################################################################
########################################################################################
########################################################################################
def stopwords_load():
    stoplist_path = '/Users/mohsennabian/Datasets/AP_DATA/stoplist.txt'
    stop_list_f = open(stoplist_path)
    stop_list = stop_list_f.read().replace('\n', ' ').split(' ')
    return(stop_list)
########################################################################################
########################################################################################
########################################################################################
########################################################################################

def extract_documents_id_by_query_as_key_in_dict():
    bm25_dict = {}

    qrel_path = '/Users/mohsennabian/Datasets/AP_DATA/qrels.adhoc.51-100.AP89.txt'
    bm25_path = '/Users/mohsennabian/Dropbox/Summer_2016/Info_Retrieval/cs6200_Mohsen_Nabian/HW1/bm25.txt'

    f = open(bm25_path, 'r')
    whole_text = f.read()
    sentences = whole_text.split('\n')
    for sentence in sentences:
        if (sentence == ' ') | (sentence == ''):
            continue
        else:
            words = sentence.split(' ')
            if words[0] not in bm25_dict:
                bm25_dict[words[0]] = [words[2]]
            else:
                bm25_dict[words[0]].append(words[2])

    g = open(qrel_path, 'r')
    whole_text = g.read()
    sentences = whole_text.split('\n')
    for sentence in sentences:
        if (sentence == ' ') | (sentence == ''):
            continue
        else:
            words = sentence.split(' ')
            if words[0] in bm25_dict.keys():
                if words[3] == '1':
                    bm25_dict[words[0]].append(words[2])

    for k in bm25_dict.keys():
        bm25_dict[k] = list(set(bm25_dict[k]))
        print(len(bm25_dict[k]))

    return(bm25_dict)

def clean_text(txt):
    stopwordlist=stopwords_load()
    txt=txt.lower()
    txt=txt.replace('\n',' ')
    txt=txt.replace('  ',' ')
    words=txt.split(' ')
    words = [x for x in words if x not in stopwordlist]
    words = [x for x in words if len(x) >3]
    words=' '.join(words)
    return (words)




def save_cleaned_text_dict():
    b = read_dictionary('/Users/mohsennabian/Datasets/AP_DATA/hw8_dict.txt')
    c={}
    for k in b.keys():
       print(k)
       c[k]=clean_text(b[k])
    save_dictionary('/Users/mohsennabian/Datasets/AP_DATA/hw8_cleaned_dict.txt', c)


def print_top_words(model, feature_names, n_top_words):
    for topic_id, topic in enumerate(model.components_):
        print('\nTopic Nr.%d:' % int(topic_id + 1))
        print(''.join([feature_names[i] + ' ' + str(round(topic[i], 2))
              +' | ' for i in topic.argsort()[:-n_top_words - 1:-1]]))




def save_text_of_all_needed_docids_in_dict_files():
    a=extract_documents_id_by_query_as_key_in_dict()
    id_list=[]

    for q in a.keys():
        for id in a[q]:
            if id not in id_list:
                id_list.append(id)
    b=extract_txt(id_list)
    save_dictionary('/Users/mohsennabian/Datasets/AP_DATA/hw8_dict.txt',b)


def partA():

    a=extract_documents_id_by_query_as_key_in_dict()  #a[qery]=[doc_id1,doc_id2]
    # save_text_of_all_needed_docids_in_dict_files()
    # save_cleaned_text_dict()
    b=read_dictionary('/Users/mohsennabian/Datasets/AP_DATA/hw8_cleaned_dict.txt')  #b[doc_id1]='Hi chetori khubi'

    qs=a.keys()
    print(qs)
    from sklearn.feature_extraction.text import TfidfVectorizer
    from sklearn.feature_extraction.text import CountVectorizer
    from sklearn.decomposition import LatentDirichletAllocation

    for q in qs:
        if q!='56': continue
        print(q)
        doc_id_list=a[q]
        all_txt_list=[]
        for id in doc_id_list:
            all_txt_list.append(b[id])
        vec = CountVectorizer()
        data = vec.fit_transform(all_txt_list).toarray()   #The sparse matrix is created now for each query

        n_topics = 20
        lda = LatentDirichletAllocation(n_topics=n_topics)
        lda.fit(data)      #finds 20 clusters for the data
        n_top_words = 30
        data_feature_names = vec.get_feature_names()
        print_top_words(lda, data_feature_names, n_top_words)

        topic_distibution=lda.transform(data)
        for i in range(0,len(data)):
            print('for document number  '+str(i)+' distribution is : '+str(topic_distibution[i]))
        print(len(data))



def partB():
    print('jadid 821')
    from sklearn.feature_extraction.text import TfidfVectorizer
    from sklearn.feature_extraction.text import CountVectorizer
    from sklearn.decomposition import LatentDirichletAllocation
    from sklearn.cluster import KMeans
    # extract_all_txt()
    a=read_dictionary('/Users/mohsennabian/Datasets/AP_DATA/hw8_partB.txt')
    print(len(a))
    all_txt_list=[]
    doc_id=[]
    for k in a.keys():
        doc_id.append(k)
        all_txt_list.append(a[k])
    vec = CountVectorizer(stop_words='english',min_df =2,max_df=30)
    print('Tokenizing ...')
    data = vec.fit_transform(all_txt_list)


    # The sparse matrix is created now for each query
    n_topics = 200
    lda = LatentDirichletAllocation(n_topics=n_topics)
    print('fitting LDA...')
    lda.fit(data)  # finds 20 clusters for the data
    # n_top_words = 30
    # data_feature_names = vec.get_feature_names()
    # print_top_words(lda, data_feature_names, n_top_words)

    topic_distibution = lda.transform(data)
    print(len(topic_distibution))

    km = KMeans(n_clusters=25)
    print('fitting...')
    km.fit(topic_distibution)
    centers = km.cluster_centers_
    print('predicting...')
    prediction = km.predict(topic_distibution)
    prediction= list(map(str, prediction) )



    # print('\n--------Which cluster each customer is in--------')
    # print('{:<15}\t{}'.format('Customer', 'Cluster'))
    # for i in range(len(prediction)):
    #     print('{:<15}\t{}'.format(topic_distibution[i], prediction[i] + 1))
    # doc_id=doc_id[0:100]
    cluster_dict = dict(zip(doc_id,prediction))
    cluster_dict=dict(cluster_dict)

    save_dictionary('/Users/mohsennabian/Datasets/AP_DATA/hw8_partB_clusters_1104.txt',cluster_dict)



def extract_query_doc_touple():


    q_ids = ['85', '59', '56', '71', '64', '62', '93', '99', '58', '77', '54', '87', '94', '100', '89', '61', '95',
             '68', '57', '97', '98', '60', '80', '63', '91']
    q_ids = list(set(q_ids))

    tt=[]
    qrel_path = '/Users/mohsennabian/Datasets/AP_DATA/qrels.adhoc.51-100.AP89.txt'
    f=open(qrel_path,'r')
    whole_txt=f.read()
    sentences = whole_txt.split('\n')

    for sentence in sentences:
        if (sentence == ' ') | (sentence == ''):
            continue
        else:
            words = sentence.split(' ')
            if words[0] in q_ids:
                if words[3] == '1':
                    tt.append((words[0],words[2]))
    return(tt)


# partB()

bb = read_dictionary('/Users/mohsennabian/Datasets/AP_DATA/hw8_partB_clusters_1104.txt')


# h=b.values()
# print(h.count('12'))
# print(len(b))
# print(b)


tt=extract_query_doc_touple()
print(len(tt))

same_query_same_cluster=0
same_query_diff_cluster=0
diff_query_same_cluster=0
diff_query_diff_cluster=0
d=[]
i=0
ddd={}
for a in tt:
    for b in tt:
        if (b,a) not in ddd:
            if (a,b) not in ddd:
                if b !=a:
                    ddd[(a,b)]=1
    print((a,b))
d=ddd.keys()
print(len(d))

total=0
for m in d:

         total=total+1
         if bb[m[0][1]]==bb[m[1][1]]:
             if m[0][0]==m[1][0]:
                same_query_same_cluster=same_query_same_cluster+1
             else:
                 diff_query_same_cluster = diff_query_same_cluster+1
                 print (bb[m[0][1]])

         else:
             if m[0][0] == m[1][0]:
                 same_query_diff_cluster=same_query_diff_cluster+1
             else:
                 diff_query_diff_cluster=diff_query_diff_cluster+1

print(same_query_same_cluster)
print(diff_query_diff_cluster)
print(diff_query_same_cluster)
print(same_query_diff_cluster)
accuracy=(same_query_same_cluster+diff_query_diff_cluster)/float(total)
print(accuracy)