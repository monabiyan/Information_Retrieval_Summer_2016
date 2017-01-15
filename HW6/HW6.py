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
def extract_data(file_address, filter_type):
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



        if filter_type== 1:
            pass


        doc_dict[doc_id] = txt


    return(doc_dict)


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




qrel = AutoVivification()
#dict['q1']['docnumber']=0


h=open("/Users/mohsennabian/Dropbox/Summer_2016/Info_Retrieval/cs6200_Mohsen_Nabian/HW1/bm25.txt",'r')
bm25=AutoVivification()
whole_text=h.read()
sentences=whole_text.split('\n')
for sentence in sentences:
    if sentence =='\n':
        break
    if sentence =='':
        break
    else:
        words = sentence.split(' ')
        q = words[0]
        if q=='10': q='100'
        d = words[2]
        r = float(words[4])
        bm25[q][d] = r

h=open("/Users/mohsennabian/Dropbox/Summer_2016/Info_Retrieval/cs6200_Mohsen_Nabian/HW1/okapi_tf.txt",'r')
okapitf=AutoVivification()
whole_text=h.read()
sentences=whole_text.split('\n')
for sentence in sentences:
    if sentence =='\n':
        break
    if sentence =='':
        break
    else:
        words = sentence.split(' ')
        q = words[0]
        if q == '10': q = '100'
        d = words[2]
        r = float(words[4])
        okapitf[q][d] = r


h=open("/Users/mohsennabian/Dropbox/Summer_2016/Info_Retrieval/cs6200_Mohsen_Nabian/HW1/tf_idf.txt",'r')
tfidf=AutoVivification()
whole_text=h.read()
sentences=whole_text.split('\n')
for sentence in sentences:
    if sentence =='\n':
        break
    if sentence =='':
        break
    else:
        words = sentence.split(' ')
        q = words[0]
        if q == '10': q = '100'
        d = words[2]
        r = float(words[4])
        tfidf[q][d] = r

#Jelinek_smoothing
h=open("/Users/mohsennabian/Dropbox/Summer_2016/Info_Retrieval/cs6200_Mohsen_Nabian/HW1/tf_idf.txt",'r')
jelinek=AutoVivification()
whole_text=h.read()
sentences=whole_text.split('\n')
for sentence in sentences:
    if sentence =='\n':
        break
    if sentence =='':
        break
    else:
        words = sentence.split(' ')
        q = words[0]
        if q == '10': q = '100'
        d = words[2]
        r = float(words[4])
        jelinek[q][d] = r



#laplace_smoothing
h=open("/Users/mohsennabian/Dropbox/Summer_2016/Info_Retrieval/cs6200_Mohsen_Nabian/HW1/lmlaplace.txt",'r')
laplace=AutoVivification()
whole_text=h.read()
sentences=whole_text.split('\n')
for sentence in sentences:
    if sentence =='\n':
        break
    if sentence =='':
        break
    else:
        words = sentence.split(' ')
        q = words[0]
        if q == '10': q = '100'
        d = words[2]
        r = float(words[4])
        laplace[q][d] = r

q_list=bm25.keys()
g=open("/Users/mohsennabian/Dropbox/Summer_2016/Info_Retrieval/cs6200_Mohsen_Nabian/HW1/qrels.adhoc.51-100.AP89.txt",'r')
whole_text=g.read()
sentences=whole_text.split('\n')
for sentence in sentences:
    if sentence =='\n':
        break
    if sentence =='':
        break
    else:
        words=sentence.split(' ')
        q=words[0]
        if q in q_list:
            d=words[2]
            r=int(words[3])
            qrel[q][d]=r




ml=AutoVivification()
for q in qrel.keys():
    for d in qrel[q].keys():
        ml[q][d]['relevence']=qrel[q][d]



        if d in bm25[q].keys():
            ml[q][d]['bm25_score']=bm25[q][d]
        else:
            min_score=9999999

            for dd in bm25[q].keys():
                m=bm25[q][dd]
                if m<min_score:
                    min_score=m
            ml[q][d]['bm25_score']=min_score


        if d in tfidf[q].keys():
            ml[q][d]['tfidf_score']=tfidf[q][d]
        else:
            min_score=9999999

            for dd in tfidf[q].keys():
                m=tfidf[q][dd]
                if m<min_score:
                    min_score = m
            ml[q][d]['tfidf_score']=min_score



        if d in okapitf[q].keys():
            ml[q][d]['okapitf_score']=okapitf[q][d]
        else:
            min_score=9999999

            for dd in okapitf[q].keys():
                m=okapitf[q][dd]
                if m<min_score:
                    min_score = m
            ml[q][d]['okapitf_score']=min_score


        if d in jelinek[q].keys():
            ml[q][d]['jelinek_score']=jelinek[q][d]
        else:
            min_score=9999999

            for dd in jelinek[q].keys():
                m=jelinek[q][dd]
                if m<min_score:
                    min_score = m
            ml[q][d]['jelinek_score']=min_score


        if d in laplace[q].keys():
            ml[q][d]['laplace_score']=laplace[q][d]
        else:
            min_score=9999999

            for dd in laplace[q].keys():
                m=laplace[q][dd]
                if m<min_score:
                    min_score = m
            ml[q][d]['laplace_score']=min_score

Q_LIST=qrel.keys()
import random
Q_TEST=random.sample(Q_LIST, 5)
# Q_TEST=['58', '99', '98', '87', '100']
Q_TRAIN=[]
for q in Q_LIST:
    if q not in Q_TEST:
        Q_TRAIN.append(q)



print(Q_TEST)
print (Q_TRAIN)


#Training Model###########

X_TRAIN=[]
Y_TRAIN=[]
fff=open('/Users/mohsennabian/Desktop/matrix','w')
mmm=1
for q in Q_TRAIN:
    for d in ml[q].keys():
            x1 = ml[q][d]['jelinek_score']
            x2 = ml[q][d]['laplace_score']
            x3 = ml[q][d]['okapitf_score']
            x4 = ml[q][d]['tfidf_score']
            x5 = ml[q][d]['bm25_score']
            if (x1) == {}: print('empty x1')
            if (x2) == {}: print('empty x2')
            if (x3) == {}: print('empty x3')
            if (x4) == {}: print('empty x4')
            if (x5) == {}: print('empty x5')
            X_TRAIN.append([x1,x2,x3,x4,x5])
            Y_TRAIN.append(ml[q][d]['relevence'])
            fff.write(str(mmm)+' '+str(x1)+' '+str(x5)+' '+str(x3)+' '+str(x4)+' '+str(x2)+'    ====   '+str(ml[q][d]['relevence'])+'\n')
            mmm=mmm+1


print('training...')
import numpy as np
import matplotlib.pyplot as plt
X_TRAIN=np.array(X_TRAIN)

from sklearn import svm,linear_model

clf = svm.SVC()
regr = linear_model.LinearRegression()

clf.fit(X_TRAIN,Y_TRAIN)
# regr.fit(X_TRAIN,Y_TRAIN)


######################
print('testing...')
X_TEST=[]
Y_TEST_Predicted=[]
Y_TEST=[]
report_test=[]
report_test_query=[]
report_test_doc=[]
for q in Q_TRAIN:
    for d in ml[q].keys():
            x1 = ml[q][d]['jelinek_score']
            x2 = ml[q][d]['laplace_score']
            x3 = ml[q][d]['okapitf_score']
            x4 = ml[q][d]['tfidf_score']
            x5 = ml[q][d]['bm25_score']
            if (x1) == {}: print('empty')
            if (x2) == {}: print('empty')
            if (x3) == {}: print('empty')
            if (x4) == {}: print('empty')
            if (x5) == {}: print('empty')
            ml[q][d]['prediction']=clf.predict([x1,x2,x3,x4,x5]).tolist()[0]
            ml[q][d]['training']=True

for q in Q_TEST:
    for d in ml[q].keys():
            x1 = ml[q][d]['jelinek_score']
            x2 = ml[q][d]['laplace_score']
            x3 = ml[q][d]['okapitf_score']
            x4 = ml[q][d]['tfidf_score']
            x5 = ml[q][d]['bm25_score']
            if (x1) == {}: print('empty')
            if (x2) == {}: print('empty')
            if (x3) == {}: print('empty')
            if (x4) == {}: print('empty')
            if (x5) == {}: print('empty')
            ml[q][d]['prediction']=clf.predict([x1,x2,x3,x4,x5]).tolist()[0]
            ml[q][d]['training']=False
            fff.write(str(mmm) + ' ' + str(x1) + ' ' + str(x5) + ' ' + str(x3) + ' ' + str(x4) + ' ' + str(
                x2) + '    ====   ' + str(ml[q][d]['prediction']) + '\n')
            mmm=mmm+1


f=open('/Users/mohsennabian/Dropbox/Summer_2016/Info_Retrieval/cs6200_Mohsen_Nabian/HW1/train.txt','w')
for qr in Q_TRAIN:
    d=[]
    q=[]
    r=[]
    for dd in ml[qr].keys():
        d.append(dd)
        r.append(ml[qr][dd]['prediction'])
        q.append(qr)
    r,q,d=lists_sort(r,q,d)
    for i in range(0, len(r)):
        f.write(q[i] + ' ' + 'Q0' + ' ' + d[i] + ' ' + str(i + 1) + ' ' + str(r[i]) + ' Exp' + '\n')
f.close()



f = open('/Users/mohsennabian/Dropbox/Summer_2016/Info_Retrieval/cs6200_Mohsen_Nabian/HW1/test.txt', 'w')
for qr in Q_TEST:
    d = []
    q = []
    r = []
    for dd in ml[qr].keys():
        d.append(dd)
        r.append(ml[qr][dd]['prediction'])
        q.append(qr)
    r, q, d = lists_sort(r, q, d)
    for i in range(0, len(r)):
        f.write(q[i] + ' ' + 'Q0' + ' ' + d[i] + ' ' + str(i + 1) + ' ' + str(r[i]) + ' Exp' + '\n')
f.close()


print(Q_TEST)


