from elasticsearch import Elasticsearch

# by default we connect to localhost:9200
es = Elasticsearch()


def read_documents():    # extracts documents body and their ids from a bunch of files in the given address
    path='/Users/mohsennabian/Dropbox/AP_DATA/ap89_collection'
    Document_Number = []
    Document_Content = []
    TXT = ''
    index = 0
    index2=0

    import os

    for filename in os.listdir(path):
        filename = path + '/' + filename
        f = open(filename)
        TXT = 'filebeginingomid1'
        next = '1'
        while next != "":
            next = f.readline()

            if ('<DOC>' in next):
                new_doc=True

            if ("<DOCNO>" in next) | ("</DOCNO>" in next):


                index = index + 1
                pure_next = next.replace("<DOCNO>", '')
                pure_next = pure_next.replace("</DOCNO>", '')
                pure_next = pure_next.replace("\n", '')
                pure_next = pure_next.replace(" ", '')
                Document_Number.append(pure_next)


                print(index)
            if ('</DOC>' in next):

                TXT = TXT.replace("</DOC>",'')
                TXT = TXT.replace("<DOC>", '')
                TXT = TXT.replace("<NOTE>", '')
                TXT = TXT.replace("</NOTE>", '')
                TXT = TXT.replace("</DOCNO>", '')
                TXT = TXT.replace("<DOCNO>", '')
                TXT = TXT.replace("</HEAD>", '')
                TXT = TXT.replace("'", '')
                TXT = TXT.replace("`", '')
                TXT = TXT.replace(Document_Number[index-1], '')
                Document_Content.append(TXT)
                index2=index2+1
                TXT=''
            if ('<FILEID>' in next) | ('<FIRST>' in next)|('<SECOND>' in next)|('<HEAD>' in next)|('<BYLINE>' in next)\
                    |('<DATELINE>' in next)|('<TEXT>' in next)|('</TEXT>' in next):
                continue

            else:
                TXT = TXT + ' ' + next.replace("\n", '')

    print(len(Document_Content), len(Document_Number))

    Doc_dic={}
    for i in range(0,len(Document_Content)):
        Doc_dic[Document_Number[i]]=Document_Content[i]

    return (Document_Content, Document_Number,Doc_dic)


def elasticsearch_indexing():  # uses read_documents function.will create index file given the documents and ids.
    path = '/Users/mohsennabian/Dropbox/AP_DATA/ap89_collection'
    Document_Content, Document_Number ,Doc_dic = read_documents(path)
    Document_Content[32943] = Document_Content[32943][60:]    # some especial characters are omitted this way
    print(Document_Content[32943], Document_Number[32943])
    for i in range(0, len(Document_Content)):
        print(Document_Number[i])
        print(i)
        es.index(index="ap_dataset", doc_type="document", id=Document_Number[i], body={"docno": Document_Number[i], "text":Document_Content[i]})


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
    query_list1[0] = 'allegation corrupt government jurisdiction public officials'
    query_list1[1] = 'weather fatality location'
    query_list1[2] = 'prediction prime rate lend'
    query_list1[3] = 'incursion military guerrilla border land air water'
    query_list1[4] = 'political motivated hostage hostage-taking'
    query_list1[5] = "military coup d'etat attempted successful country"
    query_list1[6] = 'National Rifle Association  NRA supporters assets'
    query_list1[7] = 'Iran-Contra affair'
    query_list1[8] = 'rail strike rail-strike predict'
    query_list1[9] = 'poach wildlife poaching '
    query_list1[10] = 'launch commercial satellite contract preliminary agreement tentative reservation cite sign'
    query_list1[11] = 'criminal action officer failed U.S. financial institution'
    query_list1[12] = 'crime perpetrated computer'
    query_list1[13] = 'non-communist industrialized high-tech dual-use technology'
    query_list1[14] = 'pending investment OPEC "downstream" operation'
    query_list1[15] = 'Israel Iran-Contra Affair'
    query_list1[16] = 'computer application crime solving'
    query_list1[17] = 'safety manufacturing employees installation workers fine-diameter fibers insulation'
    query_list1[18] = 'MCI Bell'
    query_list1[19] = 'fiber optics technology'
    query_list1[20] = 'organization produce fiber optics equipment'
    query_list1[21] = 'salary levels incentive pay seniority longevity job'
    query_list1[22] = '1988 presidential candidate'
    query_list1[23] = 'machine translation'
    query_list1[24] = 'acquisition U.S. Army advanced weapons system'
    for index in range(0, 25):
        temp=query_list1[index].split(' ')
        query_list1[index]=[x for x in temp if x != '']
    return query_list1


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




def document_length(id):  # returns the document length given its id

    es = Elasticsearch()
    length = es.search(index='ap_dataset', doc_type='document', body={"query": {
        "match": {"docno": id}
    },
        "aggs": {
            "count": {
                "stats": {
                    "script": "doc['text'].values.size()"
                }
            }
        }})
    l=(length['aggregations']['count']['max'])
    return float(l)





def avg_docs_length():
    Document_Content, Document_Number,Doc_dic=read_documents()
    sums=0
    for i in range(0,len(Document_Number)):
        sums=sums+document_length(Document_Number[i])
        print(sums)

    print(sums/len(Document_Number))
    return(sums/len(Document_Number))






def doc_length_file():

    Document_Length=[]
    Document_Content, Document_Number,Doc_dic=read_documents()

    path = '/Users/mohsennabian/Dropbox/Summer_2016/Info_Retrieval/cs6200_Mohsen_Nabian/HW1/docs_length.txt'
    f = open(path, 'w')

    for i in range(0, len(Document_Number)):
        Document_Length.append(document_length(Document_Number[i]))

        stt = str(Document_Length[i]) + ',' + str(Document_Number[i]) + '\n'

        f.write(stt)  # python will convert \n to os.linesep
        print(stt)
    f.close()






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


def call_id_list():
    path='/Users/mohsennabian/Dropbox/Summer_2016/Info_Retrieval/cs6200_Mohsen_Nabian/HW1/docs_length.txt'
    f = open(path)
    next='1'
    id_list=[]
    while next != "":
        next = f.readline()
        if next=='': break
        next = next.replace('\n', '')
        temp = next.split(',')
        print(temp[1])
        id_list.append(temp[1])


    return(id_list)







def term_search(word):  # returns the term frequency of the given word in all documents as well as the document id
    es = Elasticsearch()
    tf = []
    doc_id = []

    total_hit = es.search(index='ap_dataset', doc_type='document', body={"query": {
        "match": {
            "text": word
        }
    },
        "explain": "true"})['hits']['total']

    print('number of hits for ',word, 'is ',total_hit)
    total_hit=int(total_hit)
    orig_total_hit=total_hit
    if (total_hit>10000):
        total_hit=10000
    xx_root = es.search(index='ap_dataset', doc_type='document', size=total_hit, body={"query": {
        "match": {
            "text": word
        }
    },
        "explain": "true"})['hits']['hits']

    for id in range(0, total_hit):
        print(id)
        Jlist = xx_root[id]
        Jlist = str(Jlist)
        import re
        m = re.search("description': u'tf.freq=([0-9]+)", Jlist)
        found = m.group(1)
        print(found)
        xx = int(found)+0.0
        yy = xx_root[id]['_id']
        tf.append(xx)
        doc_id.append(yy)

    print(total_hit)
    print(len(tf))
    print(len(doc_id))
    return(orig_total_hit,doc_id,tf)




def Ranking(query_list):  #return okapi_TF score of all documents with respect to word 'word'

  D = 84678
  V = 178081
  avgs_Docs_length = 166.0558
  k1=1.2
  k2=100
  b=0.75
  tf_wq=1


  import math
  Document_Content, Document_Number, Doc_dic = read_documents()
  Doc_length = call_doc_length()
  sum_length_all_Doc = sum(Doc_length.values())
  #id_list = call_id_list()

  all_query_okapi_tf=[]
  all_query_tf_idf = []
  all_query_bm25=[]
  all_query_laplace_smoothing = []
  all_query_Jelinek_smoothing = []


  for query in query_list:
      score_okapi_tf = {}
      score_tf_idf = {}
      score_bm25={}
      score_laplace_smoothing = {}
      score_Jelinek_smoothing = {}

      for id in Document_Number:
          score_okapi_tf[id] = 0
          score_tf_idf[id] = 0
          score_bm25[id] = 0
          score_laplace_smoothing[id] = 0
          score_Jelinek_smoothing[id] = 0


      for word in query:

        print(word)
        total_hit, doc_id, tf = term_search(word)
        print('done')

        for i in range(0, len(doc_id)):
            print(i,'dodo')
            tf_wd = tf[doc_id.index(doc_id[i])]     #tf related to the
            len_d = float(Doc_length.get(doc_id[i]))
            tf_w_all =sum(tf)
            landa = len_d/(len_d+avgs_Docs_length)


            okptf = tf_wd/(tf_wd+0.5+1.5*len_d/avgs_Docs_length)      # Score Criteria
            tf_idf = okptf * math.log(D/total_hit,10)
            bm25=math.log(((D+0.5)/(total_hit+0.5)),10)*((tf_wd+k1*tf_wd)/(tf_wd+k1*((1-b)+b*len_d/avgs_Docs_length))*(tf_wq+k2*tf_wq)/(tf_wq+k2))

            laplace_smoothing = math.log((tf_wd + 1)/(len_d+V),10)     #math.log
            #print('laplace_smoothing',laplace_smoothing)
            Jelinek_smoothing = math.log(((landa * tf_wd)/len_d+(1-landa)*tf_w_all/sum_length_all_Doc),10)

            

            score_okapi_tf[doc_id[i]] = okptf+score_okapi_tf[doc_id[i]]
            score_tf_idf[doc_id[i]] =tf_idf+ score_tf_idf[doc_id[i]]
            score_bm25[doc_id[i]]=bm25+score_bm25[doc_id[i]]
            score_laplace_smoothing[doc_id[i]]=laplace_smoothing + score_laplace_smoothing[doc_id[i]]
            score_Jelinek_smoothing[doc_id[i]]=Jelinek_smoothing + score_Jelinek_smoothing[doc_id[i]]


      import operator

      score_okapi_tf_sorted = sorted(score_okapi_tf.items(), key=operator.itemgetter(1), reverse=True)[0:1000]
      all_query_okapi_tf.append(score_okapi_tf_sorted)

      score_tf_idf_sorted = sorted(score_tf_idf.items(), key=operator.itemgetter(1), reverse=True)[0:1000]
      all_query_tf_idf.append(score_tf_idf_sorted)

      score_bm25_sorted = sorted(score_bm25.items(), key=operator.itemgetter(1), reverse=True)[0:1000]
      all_query_bm25.append(score_bm25_sorted)




      for id in score_laplace_smoothing.keys():

          if (score_laplace_smoothing[id]==0) :
              score_laplace_smoothing[id] = -99999

      score_laplace_smoothing_sorted = sorted(score_laplace_smoothing.items(), key=operator.itemgetter(1), reverse=True)[0:1000]

      all_query_laplace_smoothing.append(score_laplace_smoothing_sorted)


      for id in score_Jelinek_smoothing.keys():

          if (score_Jelinek_smoothing[id] == 0):
              score_Jelinek_smoothing[id] = -99999


      score_Jelinek_smoothing_sorted = sorted(score_Jelinek_smoothing.items(), key=operator.itemgetter(1), reverse=True)[0:1000]

      all_query_Jelinek_smoothing.append(score_Jelinek_smoothing_sorted)



  return(all_query_okapi_tf,all_query_tf_idf,all_query_bm25,all_query_laplace_smoothing, all_query_Jelinek_smoothing)



def write_results(query_list):


    q_no = query_number_extract()
    all_query_okapi_tf, all_query_tf_idf, all_query_bm25, all_query_laplace_smoothing, all_query_Jelinek_smoothing = Ranking(query_list)
    path = '/Users/mohsennabian/Dropbox/Summer_2016/Info_Retrieval/cs6200_Mohsen_Nabian/HW1/'


    f = open(path+'okapi_tf.txt', 'w')
    for i in range (0,len(all_query_okapi_tf)) :
        for j in range(0, len(all_query_okapi_tf[i])):
            stt = str(q_no[i])+' Q0 '+str(all_query_okapi_tf[i][j][0]) +' '+str(j+1) +' ' +str(all_query_okapi_tf[i][j][1])+' Exp'+'\n'
            f.write(str(stt))
    f.close()

    f = open(path + 'tf_idf.txt', 'w')
    for i in range(0, len(all_query_tf_idf)):
        for j in range(0, len(all_query_tf_idf[i])):
            stt = str(q_no[i]) + ' Q0 ' + str(all_query_tf_idf[i][j][0]) + ' ' + str(j + 1) + ' ' + str(all_query_tf_idf[i][j][1]) + ' Exp' + '\n'
            f.write(str(stt))
    f.close()

    f = open(path + 'bm25.txt', 'w')
    for i in range(0, len(all_query_bm25)):
        for j in range(0, len(all_query_bm25[i])):
            stt = str(q_no[i]) + ' Q0 ' + str(all_query_bm25[i][j][0]) + ' ' + str(j + 1) + ' ' + str(all_query_bm25[i][j][1]) + ' Exp' + '\n'
            f.write(str(stt))
    f.close()

    f = open(path + 'laplace_smoothing.txt', 'w')
    for i in range(0, len(all_query_laplace_smoothing)):
        for j in range(0, len(all_query_laplace_smoothing[i])):
            stt = str(q_no[i]) + ' Q0 ' + str(all_query_laplace_smoothing[i][j][0]) + ' ' + str(j + 1) + ' ' + str(all_query_laplace_smoothing[i][j][1]) + ' Exp' + '\n'
            f.write(str(stt))
    f.close()

    f = open(path + 'Jelinek_smoothing.txt', 'w')
    for i in range(0, len(all_query_Jelinek_smoothing)):
        for j in range(0, len(all_query_Jelinek_smoothing[i])):
            stt = str(q_no[i]) + ' Q0 ' + str(all_query_Jelinek_smoothing[i][j][0]) + ' ' + str(j + 1) + ' ' + str(all_query_Jelinek_smoothing[i][j][1]) + ' Exp' + '\n'
            f.write(str(stt))
    f.close()





if __name__ == "__main__":
     query_list = query_prep()
     print((query_list))
     query_number_extract()
     #doc_length_file()
     #avg_docs_length()
     #main_indexing()
     #term_search('car')
     #q=query_prep()
     #print(q[0])
     #print(q[5])
     #example_elastic_search()
     #test()
     #test3()
     #main_quering()
     #H=okapi_TF(q)
     #print(H[1])
     #TF , DF,
     write_results((query_list))

     #avgs_Docs_length=166.055811427
