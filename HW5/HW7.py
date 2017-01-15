import email
import re
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
def takepasm_dict():
    spam_dict=dict()
    h=open('/Users/mohsennabian/Datasets/email_spam/full/index','r')
    TXT=h.read()
    sentences=TXT.split('\n')
    for sentence in sentences:
        if (sentence==' ')|(sentence=='')|(sentence=='\n'): continue
        words=sentence.split(' ')
        spam_txt=words[0]
        file_id=words[1].split('/')[2]
        print(file_id)
        if spam_txt=='spam':
            spam_dict[file_id]=True
            print('spam')
        elif spam_txt=='ham':
            spam_dict[file_id]=False
            print('ham')
        else :
            print('estebah shod   '+ spam_txt)
    return(spam_dict)
########################################################################################
########################################################################################
########################################################################################
########################################################################################
def cleanmail(myString):
    # b = email.message_from_string(myString)
    # my_out_s=''
    # if b.is_multipart():
    #     for payload in b.get_payload():
    #         # if payload.is_multipart(): ...
    #         sss=payload.get_payload()
    #         my_out_s= str(sss)+' '+str(my_out_s)
    # else:
    #     sss= b.get_payload()
    #     my_out_s=str(sss)
    # my_out_s=str(my_out_s)
    s=myString
    s = re.sub('<[^<]+?>', '', s)
    s = re.sub('\n', ' ', s)
    s = re.sub('  ', ' ', s)
    s = unicode(s, errors='replace')
    # d = enchant.Dict("en_US")
    words_list=set(s.split(' '))
    # print(len(words_list))
    all_english=' '
    for word in words_list:
        if word !='':
            # if d.check(word):
            try:
                if len(str(word))<30:
                    all_english=str(all_english)+' '+str(word)
            except:
                continue
    # non_english=set(words_list)-set(nltk.corpus.words.words())
    # s_english=list(set(words_list)-non_english)
    # s=' '.join(s_english)
    s=all_english.lower()
    return(s)
########################################################################################
########################################################################################
########################################################################################
########################################################################################
def push_all_to_elasticsearch():  #push all documents to elastic search
    import os
    from elasticsearch import Elasticsearch
    es = Elasticsearch()
    path='/Users/mohsennabian/Datasets/email_spam/data'
    spam_dict=takepasm_dict()
    # print('inmail.1' in spam_dict.keys())
    whole_list=os.listdir(path)
    l=len(whole_list)
    import random
    test_list=random.sample(whole_list, int(l*0.2))
    train_list=list(set(whole_list)-set(test_list))
    testortrain_dict=dict.fromkeys(test_list,'test')
    testortrain_dict.update(dict.fromkeys(train_list, 'train'))
    print(len(testortrain_dict))
    print(type(os.listdir(path)))
    for filename in os.listdir(path):
        if filename=='.DS_Store': continue
        print(filename)
        full_filename = path + '/' + filename
        f = open(full_filename,'r')
        whole_text=str(f.read())
        pure_text=cleanmail(whole_text)
        if len(str(pure_text))<5:
            pure_text="free price virus click viagra win bonus luxury"
        es.index(index="emails", doc_type="document", id=filename,
                 body={"docno": filename, "text": pure_text,"spam_statuse":spam_dict[filename],
                       "T": testortrain_dict[filename]})


########################################################################################
########################################################################################
########################################################################################
########################################################################################
def find_training_or_test_dict_for_all_documents_by_serching_through_elasticsearch():
    from elasticsearch import Elasticsearch
    es = Elasticsearch()
    document_id_list=list_all_documents_id()
    train_or_test_dict={}
    for doc_id in document_id_list:
        existing_data = es.get(index="emails", doc_type='document', id=doc_id,
                               fields=['T'])['fields']['T'][0]
        print(existing_data)
        train_or_test_dict[doc_id]=str(existing_data)
    return(train_or_test_dict)
########################################################################################
########################################################################################
########################################################################################
########################################################################################
def give_train_test_random_based_as_two_lists():
    import os
    path = '/Users/mohsennabian/Datasets/email_spam/data'
    whole_list = os.listdir(path)
    l = len(whole_list)
    import random
    test_list = random.sample(whole_list, int(l * 0.2))
    train_list = list(set(whole_list) - set(test_list))
    return(train_list,test_list)
########################################################################################
########################################################################################
########################################################################################
########################################################################################
def spam_list(path):  #read the word list for spam
    g=file(path,'r')
    whole_text=g.read()
    spam_words=[]
    sentences=whole_text.split('\n')
    for sentence in sentences:
        if (sentence=='')|(sentence==' '):
            continue
        else:
            for word in sentence.split(' '):
                if word=='': continue
                spam_words.append(str(word).lower())
    return(set(spam_words))
########################################################################################
########################################################################################
########################################################################################
########################################################################################
def list_of_documents_contain_search_word(query_word):
    from elasticsearch import Elasticsearch
    es = Elasticsearch()
    docs_found=[]
    res = es.search(index="emails", doc_type="document", size=10000, body={"query": {"match": {"text": query_word}}})
    # print(res['hits'])
    # print("%d documents found" % res['hits']['total'])
    print(query_word)
    i = 0
    for doc in res['hits']['hits']:
        i = i + 1
        print(i)
        docs_found.append(doc['_id'])
        # print("%s) %s %s" % (doc['_id'], doc['_source']["text"], doc['_source']["spam_statuse"]))
    return(docs_found)
########################################################################################
########################################################################################
########################################################################################
########################################################################################
def list_all_documents_id():
    document_id_list=[]
    import os
    path = '/Users/mohsennabian/Datasets/email_spam/data'
    for filename in os.listdir(path):
        if filename=='.DS_Store': continue
        print(filename)
        document_id_list.append(filename)
    return(document_id_list)
########################################################################################
########################################################################################
########################################################################################
########################################################################################
def create_and_save_virgil_and_mohsen_machine_learning_dictionaries():
    virgil_path='/Users/mohsennabian/Dropbox/Summer_2016/Info_Retrieval/HW7/spam_words.txt'
    virgil_spam_list=spam_list(virgil_path)
    Mohsen_path='/Users/mohsennabian/Dropbox/Summer_2016/Info_Retrieval/HW7/Mohsen_spam.txt'
    Mohsen_spam_list=spam_list(Mohsen_path)
    # print(virgil_spam_list)
    # print(len(virgil_spam_list))
    # print(Mohsen_spam_list)
    # print(len(Mohsen_spam_list))
    # # print(list_of_documents_contain_search_word('sex'))
    train_or_test_dict = find_training_or_test_dict_for_all_documents_by_serching_through_elasticsearch()
    all_doc_ids=list_all_documents_id()
    spam_ham_container=takepasm_dict()
    #####################################
    matrix_virgil=AutoVivification()
    for doc_id in all_doc_ids:
        for spam_word in virgil_spam_list:
            matrix_virgil[doc_id][spam_word]=0
            matrix_virgil[doc_id]['y_lable'] = spam_ham_container[doc_id]
            matrix_virgil[doc_id]['tr_ts'] = train_or_test_dict[doc_id]

    #####################################
    matrix_mohsen=AutoVivification()
    for doc_id in all_doc_ids:
        for spam_word in Mohsen_spam_list:
            matrix_mohsen[doc_id][spam_word]=0
            matrix_mohsen[doc_id]['y_lable'] = spam_ham_container[doc_id]
            matrix_mohsen[doc_id]['tr_ts'] = train_or_test_dict[doc_id]

    k = 0
    for doc_id in all_doc_ids:
        k = k + 1
        print('word number ' + str(k))
        tf_dict = recieve_term_vector(doc_id)
        for term in virgil_spam_list:
            if term in tf_dict.keys():
                matrix_virgil[doc_id][term] = tf_dict[term]
        for term in Mohsen_spam_list:
            if term in tf_dict.keys():
                matrix_mohsen[doc_id][term] = tf_dict[term]
    path1 = '/Users/mohsennabian/Dropbox/Summer_2016/Info_Retrieval/HW7/matrix_virgil.txt'
    save_dictionary(path1, matrix_virgil)
    path2='/Users/mohsennabian/Dropbox/Summer_2016/Info_Retrieval/HW7/matrix_mohsen.txt'
    save_dictionary(path2,matrix_mohsen)
    #####################################
    print 'the end'
########################################################################################
########################################################################################
########################################################################################
########################################################################################
def evaluation(truth_list,pred_list):
   l=len(truth_list)
   hit=0
   for i in range(0,l):
       if int(truth_list[i])==int(pred_list[i]):
           hit=hit+1
   return(float(hit)/l)
########################################################################################
########################################################################################
########################################################################################
########################################################################################
def recieve_term_vector(document_id):
    tf_dict={}
    from elasticsearch import Elasticsearch
    es = Elasticsearch()
    try:
        termvec = es.termvectors(index='emails', doc_type="document", id=document_id,fields=['text'], term_statistics="true")['term_vectors']['text']['terms']
    except:
        return({'free':1})
    for term in termvec.keys():
        tf_dict[term]=termvec[term]['term_freq']
    return(tf_dict)
########################################################################################
########################################################################################
########################################################################################
########################################################################################
def extract_all_words_as_a_dictionary():  #saves all unique words as a dictionary
    import os

    path = '/Users/mohsennabian/Datasets/email_spam/data'

    whole_str = ''
    for filename in os.listdir(path):
        if filename == '.DS_Store': continue
        print(filename)
        full_filename = path + '/' + filename
        f = open(full_filename, 'r')
        whole_text = str(f.read())
        pure_text = cleanmail(whole_text)
        if len(str(pure_text)) < 5:
            pure_text = "free price virus click viagra win bonus luxury"

        whole_str = whole_str + ' ' + pure_text
    whole_str = list(set(whole_str.split(' ')))
    word_dict=dict.fromkeys(whole_str,'0')
    save_dictionary('/Users/mohsennabian/Dropbox/Summer_2016/Info_Retrieval/HW7/all_words.txt',word_dict)

########################################################################################
########################################################################################
########################################################################################
########################################################################################
def all_unique_words_dict_save():
    words_list=[]
    from elasticsearch import Elasticsearch
    es = Elasticsearch()
    docs_id = list_all_documents_id()
    for document_id in docs_id:
        print(document_id)
        termvec = es.termvectors(index='emails', doc_type="document", id=document_id,fields=['text'], term_statistics="true")['term_vectors']['text']['terms']
        words_list[0:0]=termvec.keys()

    print('allset with list')
    words_list=list(set(words_list))
    print('make unique and start pushing in dict')
    words_dict=dict.fromkeys(words_list,'0')
    print('ready to save')
    save_dictionary('/Users/mohsennabian/Dropbox/Summer_2016/Info_Retrieval/HW7/all_words.txt', words_dict)
########################################################################################
########################################################################################
########################################################################################
########################################################################################

def sparse_matrix_push(sparce_matrix,row,column,tf):
    import scipy.sparse

    rows = [row]
    cols = [column]
    prod = [(x, y) for x in rows for y in cols] # combinations
    r = [x for (x, y) in prod] # x_coordinate
    c = [y for (x, y) in prod] # y_coordinate
    data = [1] * len(r)
    m = scipy.sparse.coo_matrix((data, (r, c)), shape=(100000, 40000))






########################################################################################
########################################################################################
########################################################################################
########################################################################################

def part1():   #implements  part1 of HW7. It outputs the test results in memory

    # push_all_to_elasticsearch()    #we call them to create the dictionaries. Once we called them, no need to call next time
    # create_and_save_virgil_and_mohsen_machine_learning_dictionaries()     #we call them to create the dictionaries. Once we called them, no need to call next time

    virgil_matrix=read_dictionary('/Users/mohsennabian/Dropbox/Summer_2016/Info_Retrieval/HW7/matrix_virgil.txt')
    mohsen_matrix=read_dictionary('/Users/mohsennabian/Dropbox/Summer_2016/Info_Retrieval/HW7/matrix_mohsen.txt')
    mohsen_test=[]
    mohsen_train=[]
    for id in mohsen_matrix.keys():
        if mohsen_matrix[id]['tr_ts']=='test': mohsen_test.append(id)
        else: mohsen_train.append(id)
    virgil_test=[]
    virgil_train=[]
    for id in virgil_matrix.keys():
        if virgil_matrix[id]['tr_ts']=='test': virgil_test.append(id)
        else: virgil_train.append(id)

    ########################################## Learning Mohsen Matrix
    X_TRAIN=[]
    Y_TRAIN=[]
    l=[]
    mohsen_spam_words=spam_list('/Users/mohsennabian/Dropbox/Summer_2016/Info_Retrieval/HW7/Mohsen_spam.txt')
    for id in mohsen_train:
        l=[]
        for word in mohsen_spam_words:
            l.append(mohsen_matrix[id][word])
        X_TRAIN.append(l)
        label=mohsen_matrix[id]['y_lable']
        if label:Y_TRAIN.append(1)
        else : Y_TRAIN.append(0)
    print('training...')
    import numpy as np
    import matplotlib.pyplot as plt
    X_TRAIN=np.array(X_TRAIN)
    from sklearn import svm,linear_model
    from sklearn.naive_bayes import GaussianNB
    regr = linear_model.LinearRegression()
    gnb = GaussianNB()
    regr.fit(X_TRAIN,Y_TRAIN)

    pp=len(mohsen_spam_words)
    feature_dict={}
    for j in range(0,pp):
        feature_dict[list(mohsen_spam_words)[j]]=regr.coef_[j]
    ff=sorted(feature_dict, key=feature_dict.get)

    from sklearn.externals import joblib
    joblib.dump(regr, '/Users/mohsennabian/Dropbox/Summer_2016/Info_Retrieval/HW7/regr_mohsen.pkl')
    regr=joblib.load('/Users/mohsennabian/Dropbox/Summer_2016/Info_Retrieval/HW7/regr_mohsen.pkl')
    ##########################################   prediction
    for id in mohsen_train:
        l=[]
        for word in mohsen_spam_words:
            l.append(mohsen_matrix[id][word])
        prediction=regr.predict(l).tolist()[0]
        mohsen_matrix[id]['prediction'] = prediction
        print(str(mohsen_matrix[id]['y_lable'])+'  '+str(mohsen_matrix[id]['prediction']))
    for id in mohsen_test:
        l=[]
        for word in mohsen_spam_words:
            l.append(mohsen_matrix[id][word])
        prediction=regr.predict(l).tolist()[0]
        mohsen_matrix[id]['prediction'] = prediction
        print(str(mohsen_matrix[id]['y_lable'])+'  '+str(mohsen_matrix[id]['prediction']))
    ########################################## Sorting
    ids=[]
    labels=[]
    preds=[]
    for id in mohsen_test:
        ids.append(id)
        labels.append(mohsen_matrix[id]['y_lable'])
        preds.append(mohsen_matrix[id]['prediction'])
    print('ghasem')
    print(len(ids))
    print(len(labels))
    print(len(preds))
    ########################################## writing the sorted lists on file
    result=file('/Users/mohsennabian/Dropbox/Summer_2016/Info_Retrieval/HW7/result_Mohsen.txt','w')
    preds,ids,labels=lists_sort(preds,ids,labels)
    thresholds=0.55
    for i in range(0,len(ids)):
        if preds[i]>thresholds:
            preds[i]=1
        else:
            preds[i] = 0

        line=str(i)+' '+str(ids[i])+' '+str(labels[i])+' '+str(preds[i])+'\n'
        result.write(line)
    result.close()
    print('eval_mohsen= ' +str(evaluation(labels,preds)))
    ##########################################
    ########################################## Learning virgil Matrix
    X_TRAIN=[]
    Y_TRAIN=[]
    l=[]
    virgil_spam_words=spam_list('/Users/mohsennabian/Dropbox/Summer_2016/Info_Retrieval/HW7/spam_words.txt')
    for id in virgil_train:
        l=[]
        for word in virgil_spam_words:
            l.append(virgil_matrix[id][word])
        X_TRAIN.append(l)
        label=virgil_matrix[id]['y_lable']
        if label:Y_TRAIN.append(1)
        else:Y_TRAIN.append(0)
    print('training...')
    import numpy as np
    import matplotlib.pyplot as plt
    X_TRAIN=np.array(X_TRAIN)
    from sklearn import svm,linear_model
    from sklearn.naive_bayes import GaussianNB
    regr = linear_model.LinearRegression()
    gnb = GaussianNB()
    regr.fit(X_TRAIN,Y_TRAIN)

    pp = len(virgil_spam_words)
    feature_dict = {}
    for j in range(0, pp):
        feature_dict[list(virgil_spam_words)[j]] = regr.coef_[j]
    gg = sorted(feature_dict, key=feature_dict.get)


    from sklearn.externals import joblib
    joblib.dump(regr,'/Users/mohsennabian/Dropbox/Summer_2016/Info_Retrieval/HW7/regr_virgil.pkl')
    regr=joblib.load( '/Users/mohsennabian/Dropbox/Summer_2016/Info_Retrieval/HW7/regr_virgil.pkl')
    ##########################################   prediction
    for id in virgil_train:
        l=[]
        for word in virgil_spam_words:
            l.append(virgil_matrix[id][word])
        prediction=regr.predict(l).tolist()[0]
        virgil_matrix[id]['prediction'] = prediction
        print(str(virgil_matrix[id]['y_lable'])+'  '+str(virgil_matrix[id]['prediction']))
    for id in virgil_test:
        l=[]
        for word in virgil_spam_words:
            l.append(virgil_matrix[id][word])
        prediction=regr.predict(l).tolist()[0]
        virgil_matrix[id]['prediction'] = prediction
        print(str(virgil_matrix[id]['y_lable'])+'  '+str(virgil_matrix[id]['prediction']))
    ########################################## Sorting
    ids=[]
    labels=[]
    preds=[]
    for id in virgil_test:
        ids.append(id)
        labels.append(virgil_matrix[id]['y_lable'])
        preds.append(virgil_matrix[id]['prediction'])
    print('ghasem')
    print(len(ids))
    print(len(labels))
    print(len(preds))
    ########################################## writing the sorted lists on file
    result=file('/Users/mohsennabian/Dropbox/Summer_2016/Info_Retrieval/HW7/result_virgil.txt','w')
    preds,ids,labels=lists_sort(preds,ids,labels)
    thresholds=0.55
    for i in range(0,len(ids)):
        if preds[i]>thresholds:
            preds[i]=1
        else:
            preds[i] = 0

        line=str(i)+' '+str(ids[i])+' '+str(labels[i])+' '+str(preds[i])+'\n'
        result.write(line)
    result.close()
    print('eval_virgil= ' +str(evaluation(labels,preds)))
    print (ff)
    print (gg)
##########################################
########################################################################################
########################################################################################
########################################################################################
########################################################################################

def part2():
    # push_all_to_elasticsearch()   #we call this to index the files.
    spam_dict=takepasm_dict()
    # all_unique_words_dict_save()  #saves to a file
    all_words = read_dictionary('/Users/mohsennabian/Dropbox/Summer_2016/Info_Retrieval/HW7/all_words.txt')
    all_words=all_words.keys()
    train_list,test_list=give_train_test_random_based_as_two_lists()

#     rows=[]
#     cols=[]
#     data=[]
#     label=[]
#     words_map_dict={}
#     i=0
#     for word in all_words:
#         words_map_dict[word]=i
#         i=i+1
#     i = 0
# ############## Train
#
#     if '.DS_Store' in train_list:
#         train_list.remove('.DS_Store')
#     if '.DS_Store' in test_list:
#         test_list.remove('.DS_Store')
#
#
#     for doc_id in train_list:
#         print(i)
#         tf_dict=recieve_term_vector(doc_id)
#         for word in tf_dict.keys():
#             cols.append(words_map_dict[word])
#             rows.append(i)
#             data.append(tf_dict[word])
#         label.append(spam_dict[doc_id])
#         i = i + 1
#     import scipy.sparse
#
#     # prod = [(x, y) for x in rows for y in cols]  # combinations
#     # print('samane')
#     # r = [x for (x, y) in prod]  # x_coordinate
#     # c = [y for (x, y) in prod]  # y_coordinate
#     # print('samane')
#     m = scipy.sparse.coo_matrix((data, (rows, cols)), shape=(len(train_list), len(all_words)))
#     from sklearn import linear_model
#     regr = linear_model.LinearRegression()
#     print('fitting....')
#     regr.fit(m, label)
#     print('ask features...')
#     pp = len(all_words)
#     feature_dict = {}
#
#     #########
#
#
#
#
#
#
#
#     from sklearn.externals import joblib
#     joblib.dump(regr, '/Users/mohsennabian/Dropbox/Summer_2016/Info_Retrieval/HW7/regr.pkl')
    from sklearn.externals import joblib
    regr=joblib.load( '/Users/mohsennabian/Dropbox/Summer_2016/Info_Retrieval/HW7/regr.pkl')
    feature_dict = dict(zip(list(all_words), regr.coef_))
    # for j in range(0, pp):
    #     feature_dict[list(all_words)[j]] = regr.coef_[j]
    ff = sorted(feature_dict, key=feature_dict.get, reverse=True)
############# Test

    rows = []
    cols = []
    data = []
    label = []



    i=0
    result = file('/Users/mohsennabian/Dropbox/Summer_2016/Info_Retrieval/HW7/result_all_terms.txt', 'w')
    for doc_id in test_list:
        print('test  '+str(i))
        tf_dict=recieve_term_vector(doc_id)
        for word in tf_dict.keys():
            cols.append(words_map_dict[word])
            rows.append(i)
            data.append(tf_dict[word])
        i = i + 1
    # prod = [(x, y) for x in rows for y in cols]  # combinations
    # r = [x for (x, y) in prod]  # x_coordinate
    # c = [y for (x, y) in prod]  # y_coordinate
    # data = [1] * len(r)
    m = scipy.sparse.coo_matrix((data, (rows, cols)), shape=(len(test_list), len(all_words)))
    pred={}
    labels={}
    for i in range(0,len(test_list)):
        doc_id=test_list[i]
        labels[doc_id]=spam_dict[doc_id]
    pred_list = regr.predict(m)




    prd=[]
    for i in range(0, len(test_list)):
        prd.append(pred_list[i])
    ids=[]
    lbl=[]
    for doc_id in test_list:
        ids.append(doc_id)
        lbl.append(labels[doc_id])
    prd, ids, lbl = lists_sort(prd, ids, lbl)
    thresholds = 0.55


    for i in range(0, len(ids)):
        if prd[i] > thresholds:
            prd[i] = 1
        else:
            prd[i] = 0

        line = str(i) + ' ' + str(ids[i]) + ' ' + str(lbl[i]) + ' ' + str(prd[i]) + '\n'
        result.write(line)
    result.close()
    print('eval_virgil= ' + str(evaluation(lbl, prd)))
    print(ff[0:50])

    # print(regr.coef_)

########################################################################################
########################################################################################
########################################################################################
########################################################################################

# part1()
part2()

