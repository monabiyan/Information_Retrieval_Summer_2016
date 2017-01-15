
class AutoVivification(dict):
    """Implementation of perl's autovivification feature."""
    def __getitem__(self, item):
        try:
            return dict.__getitem__(self, item)
        except KeyError:
            value = self[item] = type(self)()
            return value






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
def extract_query_url_dict():
    from elasticsearch import Elasticsearch

    es = Elasticsearch()


    query_list=['MAJOR TERRORISM ACTS in 21st CENTURY',
                'pentagon crash',
                'wtc twin towers',
                'london bombing',
                'patriot act',
                'boston marathon bombing motive',
                'domestic shooting on islamism'
                ]
    query_id=['1510','151001','151002','151003','151004','151005','151006']


    query_url_dict={}
    for query_text in query_list:
        query_url_dict[query_text]=[]


    for query_text in query_list:

        URL_km = es.search(index='four', doc_type='document',size=1000, body={"query": {
            "match": {
                "text":query_text
            }
        },
            "explain": "true"})['hits']['hits']

        url_dict=0
        for i in range(0,200):
            print(URL_km[i]['_id'])
            query_url_dict[query_text].append(URL_km[i]['_id'])


    path='/Users/mohsennabian/Dropbox/Summer_2016/Info_Retrieval/cs6200_Mohsen_Nabian/HW5/query_url_dict.txt'
    save_dictionary(path,query_url_dict)

# extract_query_url_dict()


def Excel_writing(myDictionary):
    import xlsxwriter

    workbook = xlsxwriter.Workbook('/Users/mohsennabian/Dropbox/Summer_2016/Info_Retrieval/cs6200_Mohsen_Nabian/HW5/query_url_dict_excel.xls')
    worksheet = workbook.add_worksheet()


    column=0
    print(column)
    for key in myDictionary.keys():
        print(key)
        row = 0
        worksheet.write(row, column, key)
        for url in myDictionary[key]:
            row = row+1
            if len(url)<255:
                worksheet.write(row, column, url)
            else:
                print('long URL  =   '+url)
        column = column + 1
        worksheet.write(0, column, 'Score')
        column=column+1
        print('hi')

    workbook.close()


# Excel_writing(query_url_dict)

def precision_calculations(rank_list,god,truth,teta,q,ezafi_q):
    precision=1
    recall=1
    FP=0
    TP=0
    FN=0
    # print (rank_list)
    # print(god)
    # print(truth)
    # print (len(rank_list))
    # print(len(god))
    # # print(teta)
    # print('nadiye')
    rank_list=rank_list[0:(teta)]
    # print(rank_list)
    # print('baradar')

    for i in range(0,len(rank_list)):
        # print(truth[i])
        # print('neda')
        if int(truth[i])==1:
            TP=TP+1
        else:
            FP=FP+1

    # print(range(len(rank_list), len(god)))
    # print((truth))
    # print('rouhani')
    for i in range(teta, len(god)):
        if int(truth[i])==1:
            FN=FN+1
    FN=FN+ezafi_q
    # print(teta)
    # print(TP)
    # print(" FP = " + str(FP) + "  TP = " + str(TP) + "  FN = " + str(FN))

    if (TP+FP==0):
        print('Query_have_recall_problem = ' + q)
        precision=0
    else:
        precision=float(TP)/(TP+FP)

    if TP+FN==0:
        print('Query_have_recall_problem = '+q)
        recall=0
    else:
        recall=float(TP)/(TP+FN)
    # print("TP =  " + str(TP))
    # print("FP =  " + str(FP))
    # print("FN =  " + str(FN))
    #
    # print("precioson =  "+str(precision))
    # print("recal =  "+str(recall))
    # print(" FP = " + str(FP) + " TP = " + str(TP) + " FN = " + str(FN) + "  Precision = " + str(precision) + " recall = " + str(recall))
    if float(precision+recall)==0:
        print('Query_have_recall_problem = ' + q)
        f_measure=0

    else :
        f_measure=2*precision*recall/float(precision+recall)

    return(FP,TP,FN,precision,recall,f_measure)

###############################################
def read_combined_qrel_file():
    path = "/Users/mohsennabian/Dropbox/Summer_2016/Info_Retrieval/cs6200_Mohsen_Nabian/HW5/group_eval/Mohsen_eval.txt"
    g=open(path)
    whole_txt=g.read();
    sentences=whole_txt.split('\n')
    q_id_list=[]
    url_list=[]
    score_list=[]

    for sentence in sentences:
        if sentence=='':
            continue
        else:
            parts=sentence.split(' ')
            q_id_list.append(parts[0])
            url_list.append(parts[2])
            if int(float(parts[3]))==2:
                parts[3]=int(1);
            else:
                parts[3]=int(0);
            score_list.append(parts[3])

    print(str(len(q_id_list))+'\n')
    print (str(len(url_list))+'\n')
    print (str(len(score_list))+'\n')
    return(q_id_list,url_list,score_list)





    ###############################################
def excel_read():
    import xlrd
    # ----------------------------------------------------------------------
    def open_file(path):
        """
        Open and read an Excel file
        """
        book = xlrd.open_workbook(path)
        # print number of sheets
        # print book.nsheets
        # # print sheet names
        # print book.sheet_names()
        # get the first worksheet
        first_sheet = book.sheet_by_index(0)
        print(first_sheet.cell(1, 0))
        #########################
        Q1_name=151003
        Q1_url=[]
        Q1_grade=[]
        for i in range(0,150):
            print(i)
            Q1_url.append(first_sheet.cell(i+1, 0).value)
            Q1_grade.append(first_sheet.cell(i+1, 1).value)
        #########################



        #########################
        Q2_name = 151005
        Q2_url = []
        Q2_grade = []
        for i in range(0, 150):
            Q2_url.append(first_sheet.cell(i + 1, 2).value)
            Q2_grade.append(first_sheet.cell(i + 1, 3).value)
        #########################


        #########################
        Q3_name = 151002
        Q3_url = []
        Q3_grade = []
        for i in range(0, 150):
            Q3_url.append(first_sheet.cell(i + 1, 6).value)
            Q3_grade.append(first_sheet.cell(i + 1, 7).value)
        #########################



        #########################
        Q4_name = 151001
        Q4_url = []
        Q4_grade = []
        for i in range(0, 150):
            Q4_url.append(first_sheet.cell(i + 1, 8).value)
            Q4_grade.append(first_sheet.cell(i + 1, 9).value)
        #########################


        g=file('/Users/mohsennabian/Dropbox/Summer_2016/Info_Retrieval/cs6200_Mohsen_Nabian/HW5/Mohsen_eval.txt','w')

        for j in range(0,150):
            g.write(str(Q1_name)+' '+'Mohsen'+' '+Q1_url[j]+' '+str(Q1_grade[j])+'\n')

        for j in range(0, 150):
            g.write(str(Q2_name) + ' ' + 'Mohsen' + ' ' + Q2_url[j] + ' ' + str(Q2_grade[j])+'\n')

        for j in range(0, 150):
            g.write((str(Q3_name) + ' ' + 'Mohsen' + ' ' + Q3_url[j] + ' ' + str(Q3_grade[j])).encode('utf-8')+'\n')

        for j in range(0, 150):
            g.write(str(Q4_name) + ' ' + 'Mohsen' + ' ' + Q4_url[j] + ' ' + str(Q4_grade[j])+'\n')


    open_file('/Users/mohsennabian/Dropbox/Summer_2016/Info_Retrieval/cs6200_Mohsen_Nabian/HW5/query_url_dict_excel.xls')


# excel_read()
# scores()

def combine_scores():
    path_mohsen  = "/Users/mohsennabian/Dropbox/Summer_2016/Info_Retrieval/HW5/group_eval/Mohsen_eval.txt"
    path_Sanjana = "/Users/mohsennabian/Dropbox/Summer_2016/Info_Retrieval/HW5/group_eval/SanjanaQrel.txt"
    path_Anvita  = "/Users/mohsennabian/Dropbox/Summer_2016/Info_Retrieval/HW5/group_eval/AnvitaQrel.txt"
    path_soumya1 = "/Users/mohsennabian/Dropbox/Summer_2016/Info_Retrieval/HW5/group_eval/soumya_qrels-151001.txt"
    path_soumya2 = "/Users/mohsennabian/Dropbox/Summer_2016/Info_Retrieval/HW5/group_eval/soumya_qrels-151002.txt"
    path_soumya3 = "/Users/mohsennabian/Dropbox/Summer_2016/Info_Retrieval/HW5/group_eval/soumya_qrels-151003.txt"
    path_soumya4 = "/Users/mohsennabian/Dropbox/Summer_2016/Info_Retrieval/HW5/group_eval/soumya_qrels-151005.txt"
    quey_id_list=[151001,151002,151003,151005]
    path_list=[path_Sanjana,path_Anvita,path_soumya1,path_soumya2,path_soumya3,path_soumya4]




    dict = AutoVivification()
    combine_dict=AutoVivification()
    for path in path_list:
        print(path)

        g=file(path,'r')

        whole_text=g.read()
        sentences=whole_text.split('\n')
        i=0
        for sentence in sentences:
            if sentence=='':
                continue
            i=i+1
            print(i)
            # sentence=sentence.replace('\n','')
            cases=sentence.split(' ')
            dict[cases[0]][cases[1]][cases[2]]=int(float(cases[3]))
            print(dict[cases[0]][cases[1]][cases[2]])



    for q_no in dict.keys():
        for name in dict[q_no].keys():
            for url in dict[q_no][name].keys():
                combine_dict[q_no][url]=0

    for q_no in dict.keys():
        for name in dict[q_no].keys():
            for url in dict[q_no][name].keys():
                combine_dict[q_no][url] = combine_dict[q_no][url]+dict[q_no][name][url];
    for q_no in combine_dict.keys():
        for url in combine_dict[q_no].keys():
                combine_dict[q_no][url] = combine_dict[q_no][url]/4
                if combine_dict[q_no][url] < 1:
                    combine_dict[q_no][url] = 0
                else:
                    combine_dict[q_no][url] = 1
    path="/Users/mohsennabian/Dropbox/Summer_2016/Info_Retrieval/cs6200_Mohsen_Nabian/HW5/group_eval/combined_eval.txt"
    g=open(path,'w')
    for q_no in combine_dict.keys():
        for url in combine_dict[q_no].keys():
            sentence=q_no+' '+'0'+' '+str(url)+' '+str(combine_dict[q_no][url])+'\n'
            g.write(sentence)



def save_standard_rank_list():
    q_id_list, url_list, score_list = read_combined_qrel_file()
    path='/Users/mohsennabian/Dropbox/Summer_2016/Info_Retrieval/cs6200_Mohsen_Nabian/HW5/ranklist_standard_format.txt'
    g=open(path,'w')
    for i in range(0,len(q_id_list)):
        statement=str(q_id_list[i])+' '+'Q0'+' '+str(url_list[i])+' '+str(i+1)+' '+'EXP'+'\n'
        g.write(statement)


def make_standard_qrel():
    q_id_list, url_list, score_list = read_combined_qrel_file()
    path = '/Users/mohsennabian/Dropbox/Summer_2016/Info_Retrieval/cs6200_Mohsen_Nabian/HW5/qrel_standard_format.txt'
    g = open(path,'w')
    for i in range(0, len(q_id_list)):

        statement = str(q_id_list[i]) + ' ' + '0' + ' ' + str(url_list[i]) + ' ' +str(score_list[i])+'\n'
        print(statement)
        g.write(statement)


# def extract_requiered_parameters():
#     path11='/Users/mohsennabian/Dropbox/Summer_2016/Info_Retrieval/HW5/ranklist_standard_format.txt'
#     path22='/Users/mohsennabian/Dropbox/Summer_2016/Info_Retrieval/HW5/qrel_standard_format.txt'
#


def scores(path1,path2):

    result_file=open('/Users/mohsennabian/Dropbox/Summer_2016/Info_Retrieval/cs6200_Mohsen_Nabian/HW5/result_final.txt','w')
    dict = AutoVivification()
    ezafi= AutoVivification()
    q_id_rank_list=[]
    url_rank_list=[]
    rank_rank_list=[]
    rank_list_file= open(path1, 'r')
    whole_text=rank_list_file.read()
    sentences=whole_text.split('\n')
    for sentence in sentences:
        if sentence=='':
            continue
        else:
            parts=sentence.split(' ')
            q_id_rank_list.append(parts[0])
            url_rank_list.append(parts[2])
            rank_rank_list.append(int(parts[3]))


    q_id_qrel=[]
    url_qrel=[]
    relevence_qrel=[]

    q_rel_file = open(path2, 'r')
    whole_text = q_rel_file.read()
    sentences = whole_text.split('\n')
    for sentence in sentences:
        if sentence == '':
            continue
        else:
            parts = sentence.split(' ')
            q_id_qrel.append( parts[0])
            url_qrel.append(parts[2])
            relevence_qrel.append(int(parts[3]))

    set_q_id_rank=set(q_id_rank_list)
    set_q_id_qrel = set(q_id_qrel)









    # for qs in query_url_dict.keys():
    #     if qs=="london bombing":
    #         query_url_dict_2['151003']=query_url_dict[qs]
    #     if qs=="wtc twin towers":
    #         query_url_dict_2['151002']=query_url_dict[qs]
    #     if qs == "pentagon crash":
    #         query_url_dict_2['151001'] = query_url_dict[qs]
    #     if qs == "boston marathon bombing motive":
    #         query_url_dict_2['151005'] = query_url_dict[qs]
    #
    # rank_list_dict=query_url_dict_2
    #
    #
    #
    #
    # q_id_list, url_list, score_list = read_combined_qrel_file()
    # print(q_id_list)

    # url_list_1 = []
    # url_list_2 = []
    # url_list_3 = []
    # url_list_4 = []
    # score_list_1 = []
    # score_list_2 = []
    # score_list_3 = []
    # score_list_4 = []


    for query_id in set_q_id_rank:
        url_rank_list_q=[]
        rank_rank_list_q=[]
        for i in range(0,len(q_id_rank_list)):
            if q_id_rank_list[i]==query_id:
                url_rank_list_q.append(url_rank_list[i])
                rank_rank_list_q.append(rank_rank_list[i])
        url_rank_list_q=[url_rank_list_q for (rank_rank_list_q,url_rank_list_q) in sorted(zip(rank_rank_list_q,url_rank_list_q))]


        dict[query_id]['url_rank_list_q']=url_rank_list_q[0:1000]
        print(url_rank_list_q[0:1000])
        print('hassan')


    for query_id in set_q_id_rank:
        url_qrel_q = []
        relevence_qrel_q=[]
        for i in range(0, len(q_id_qrel)):
            if q_id_qrel[i] == query_id:
                url_qrel_q.append(url_qrel[i])
                relevence_qrel_q.append(relevence_qrel[i])


        dict[query_id]['url_qrel_q'] = url_qrel_q
        dict[query_id]['relevence_qrel_q'] = relevence_qrel_q

    for query_id in set_q_id_rank:
        num=0
        pp=dict[query_id]['url_qrel_q']
        qq=dict[query_id]['relevence_qrel_q']
        for i in range(0,len(pp)):
            if pp[i] not in dict[query_id]['url_rank_list_q']:
                if int(qq[i])==1:
                    num=num+1
        ezafi[query_id]=num
        print('Haji ezafi for query '+str(query_id)+ '  is  '+str(ezafi[query_id]))



    for query_id in set_q_id_rank:
        dict[query_id]['final_list_assesment_0_1'] = []
        temp=list(dict[query_id]['url_rank_list_q'])
        for i in range(0,len(temp)):
            # print('finding.....'+str(i)+'   '+str(len(temp))+'   '+str(temp[i]))

            if (temp[i] not in dict[query_id]['url_qrel_q']):

                dict[query_id]['final_list_assesment_0_1'].append(0)
            else:
                for j in range(0,len(dict[query_id]['url_qrel_q'])):
                    if dict[query_id]['url_qrel_q'][j]==temp[i]:
                        dict[query_id]['final_list_assesment_0_1'].append(dict[query_id]['relevence_qrel_q'][j])


    #
    # dict[query_id][8]=list(dict[query_id]['url_rank_list_q'])
    # for i in range(0,len(dict[query_id]['url_qrel_q'])):
    #     if dict[query_id]['url_qrel_q'][i] not in dict[query_id]['url_rank_list_q']:
    #         dict[query_id][8].append(dict[query_id]['url_qrel_q'][i])
    #         dict[query_id][7].append(dict[query_id][4][i])
    #

    #
    # for query in dict.keys():
    #
    #     dict[query][4] = []   #relevence for ranklist
    #     for i in range(0,len(dict[query][2])):
    #         if dict[query][2][i] not in dict[query][1]:
    #
    #         url=dict[query][1][i]
    #         for j in range(0,len(dict[query][2])):
    #             if url==dict[query][2][j]:
    #                 dict[query][4].append(dict[query][3][j])
    #                 continue

    # dict[query][1] = the rank-list url id sorted
    # dict[query][4] = corresponding relevence check of the rank-list
    # dict[query][2] = q_rel_urls list
    # for query in dict.keys():
    #     q_rel_urls_new=dict[query][1]
    #     for i in range(0,len(dict[query][2])):
    #         if dict[query][2][i] not in dict[query][1]:
    #             q_rel_urls_new.append(dict[query][2][i])
    #             dict[query][4].append(dict[query][3][i])
    #
    #     dict[query][5]=q_rel_urls_new
    # print(dict['151003'][5])
    # print('baba')
    # dict[query][5] = q_rel_urls list with the urls sorted with the rank and the rest in qrel

    rank_list_dict=AutoVivification()
    god_dict = AutoVivification()
    truth_dict = AutoVivification()
    summary_dict=AutoVivification()
    summary_dict['r-precission']=[]
    summary_dict['average-precision'] = []
    summary_dict['NDCG'] = []
    summary_dict['precision_5']=[]
    summary_dict['recall_5'] = []
    summary_dict['fmeasure_5'] = []
    summary_dict['precision_10'] = []
    summary_dict['recall_10'] = []
    summary_dict['fmeasure_10'] = []
    summary_dict['precision_20'] = []
    summary_dict['recall_20'] = []
    summary_dict['fmeasure_20'] = []
    summary_dict['precision_50'] = []
    summary_dict['recall_50'] = []
    summary_dict['fmeasure_50'] = []
    summary_dict['precision_100'] = []
    summary_dict['recall_100'] = []
    summary_dict['fmeasure_100'] = []




    for q in dict.keys():
        rank_list_dict[q]=dict[q]['url_rank_list_q']
        god_dict[q]=dict[q]['url_rank_list_q']
        truth_dict[q]=dict[q]['final_list_assesment_0_1']
        # print('length rank_list for query = '+ str(q)+'  is equal = '+str(len(rank_list_dict[q])))
        # print('length god_dict for query = ' + str(q) + '  is equal = ' + str(len(god_dict[q])))
        # print('length truth_dict for query = ' + str(q) + '  is equal = ' + str(len(truth_dict[q])))

    print('minoo')
    print(len(god_dict))

    #
    #
    # for i in range(0,len(q_id_list)):
    #     if str(q_id_list[i])=='151001':
    #         url_list_1.append(url_list[i])
    #         score_list_1.append(score_list[i])
    #
    #
    #
    #     if str(q_id_list[i]) == '151002':
    #         url_list_2.append(url_list[i])
    #         score_list_2.append(score_list[i])
    #
    #     if str(q_id_list[i]) == '151003':
    #         url_list_3.append(url_list[i])
    #         score_list_3.append(score_list[i])
    #
    #     if str(q_id_list[i]) == '151005':
    #         url_list_4.append(url_list[i])
    #         score_list_4.append(score_list[i])
    #
    #
    #
    # if query_num==1:
    #     rank_list=url_list_1
    #     truth=score_list_1
    #
    # if query_num == 2:
    #     rank_list = url_list_2
    #     truth = score_list_2
    #
    # if query_num == 3:
    #     rank_list = url_list_3
    #     truth = score_list_3
    #
    # if query_num == 4:
    #     rank_list = url_list_4
    #     truth = score_list_4
    for q in rank_list_dict.keys():
        print(q)
        print('ali')
        rank_list=rank_list_dict[q]
        # print(rank_list)
        print('ali1')
        god=god_dict[q]
        print(god)
        print('ali2')
        truth=truth_dict[q]
        truth=map(int, truth)
        # print(truth)
        print('ali3')




    # print(len(rank_list))
    #
    # print(len(truth))
    #
    # s=0
        s=0

        for teta in range(1,(len(rank_list)+1)):
            print(teta)
            print('iman')
            print('query'+ str(q))
            a0,a1,a2,p,a4,a5=precision_calculations(rank_list,god,truth,teta,q,ezafi[query_id])
            s=s+p*int(truth[teta-1])

            print("s = "+str(s))

        RQ=((truth).count(1))+ezafi[q]
        if RQ==0:
            average_precsion =0
        else:
            average_precsion=s/RQ
        print('average_precsion  = '+str(average_precsion))

        a0,a1,a2,p,r,a5=precision_calculations(rank_list,god,truth,RQ,q,ezafi[query_id])
        r_precision= p
        print(p)
        print('r_precision'+str(r_precision))



        rank=0
        summ=0
        import math

        for i in range(2,len(rank_list)+1):

            summ=summ+(truth[i-1]/(float(math.log(i,2))))
        summ=summ+truth[0]
        NDCG=summ

        ##calculate IDCG:

        ones_IDCG=[]
        zeros_IDCG=[]

        zeros_IDCG_rank_list=[]
        zeros_IDCG_truth=[]
        ones_IDCG_rank_list=[]
        ones_IDCG_truth=[]


        for i in range(0,len(rank_list)):
            if truth[i]==0:
                zeros_IDCG_rank_list.append(rank_list[i])
                zeros_IDCG_truth.append(0)
            if truth[i]==1:
                ones_IDCG_rank_list.append(rank_list[i])
                ones_IDCG_truth.append(1)


        rank_list_IDCG=ones_IDCG_rank_list+zeros_IDCG_rank_list
        truth_IDCG=ones_IDCG_truth+zeros_IDCG_truth

        rank = 0
        summ = 0
        import math

        for i in range(2, len(rank_list_IDCG) + 1):
            summ = summ + (truth_IDCG[i - 1] / (float(math.log(i, 2))))
        summ = summ + truth_IDCG[0]
        IDCG = summ


        summ=NDCG/IDCG






        ###############################################
        import matplotlib.pyplot as plt

        prc=[]
        rec=[]

        for teta in range(1,(len(rank_list)+1)):
            a0, a1, a2, p, r, a5 = precision_calculations(rank_list, god,truth, teta,q,ezafi[query_id])
            prc.append(p)
            rec.append(r)



        for i in range(len(prc)-1,0,-1):
            if prc[i]>prc[i-1]:
                prc[i-1]=prc[i]

        print('skype precision'+str(prc))
        print('skype recall' + str(rec))

        plt.plot( rec,prc, 'ro')
        plt.axis([0, 1, 0, 1])
        plt.show()

        ###############################################
        FP, TP, FN, precision5, recall5, f_measure5=precision_calculations(rank_list,god,truth,5,q,ezafi[query_id])
        FP, TP, FN, precision10, recall10, f_measure10 = precision_calculations(rank_list, god, truth, 10,q,ezafi[query_id])
        FP, TP, FN, precision20, recall20, f_measure20 = precision_calculations(rank_list, god, truth, 20,q,ezafi[query_id])
        FP, TP, FN, precision50, recall50, f_measure50 = precision_calculations(rank_list, god, truth, 50,q,ezafi[query_id])
        FP, TP, FN, precision100, recall100, f_measure100 = precision_calculations(rank_list, god, truth, 100,q,ezafi[query_id])

        # print("NDCG= " + str(summ))
        # print('r_precision = ' + str(r_precision))
        # print('average_precsion  = ' + str(average_precsion))

        result_file.write("query id = "+str(q)+'\n')
        result_file.write("for k = 5 " +"precision = "+str(precision5) +"  "+"recall = "+str(recall5) +"  "+"f_measuere = "+str(f_measure5) +"  "+'\n')
        result_file.write("for k = 10 " + "precision = " + str(precision10) + "  " + "recall = " + str(
            recall10) + "  " + "f_measuere = " + str(f_measure10) + "  " + '\n')
        result_file.write("for k = 20 " + "precision = " + str(precision20) + "  " + "recall = " + str(
            recall20) + "  " + "f_measuere = " + str(f_measure20) + "  " + '\n')
        result_file.write("for k = 50 " + "precision = " + str(precision50) + "  " + "recall = " + str(
            recall50) + "  " + "f_measuere = " + str(f_measure50) + "  " + '\n')
        result_file.write("for k = 100 " + "precision = " + str(precision100) + "  " + "recall = " + str(
            recall100) + "  " + "f_measuere = " + str(f_measure100) + "  " + '\n')

        result_file.write("    Average Precision =  "+ str(average_precsion)+'\n')
        result_file.write("    NDCG= " + str(summ) + '\n')
        result_file.write("    R-Precision =  " + str(r_precision) + '\n')
        result_file.write("#########################################################################"+'\n')

        summary_dict['r-precission'].append(r_precision)
        summary_dict['average-precision'].append(average_precsion)
        summary_dict['NDCG'].append(summ)
        summary_dict['precision_5'].append(precision5)
        summary_dict['recall_5'].append(recall5)
        summary_dict['fmeasure_5'].append(f_measure5)
        summary_dict['precision_10'].append(precision10)
        summary_dict['recall_10'].append(recall10)
        summary_dict['fmeasure_10'].append(f_measure10)
        summary_dict['precision_20'].append(precision20)
        summary_dict['recall_20'].append(recall20)
        summary_dict['fmeasure_20'].append(f_measure20)
        summary_dict['precision_50'].append(precision50)
        summary_dict['recall_50'].append(recall50)
        summary_dict['fmeasure_50'].append(f_measure50)
        summary_dict['precision_100'].append(precision100)
        summary_dict['recall_100'].append(recall100)
        summary_dict['fmeasure_100'].append(f_measure100)

    import numpy as np

    r_precision=sum(summary_dict['r-precission']) / float(len(summary_dict['r-precission']))
    average_precsion=sum(summary_dict['average-precision']) / float(len(summary_dict['average-precision']))
    summ=sum(summary_dict['NDCG']) / float(len(summary_dict['NDCG']))
    precision5=sum(summary_dict['precision_5']) / float(len(summary_dict['precision_5']))
    recall5=sum(summary_dict['recall_5']) / float(len(summary_dict['recall_5']))
    f_measure5=sum(summary_dict['fmeasure_5']) / float(len(summary_dict['fmeasure_5']))
    precision10 =sum(summary_dict['precision_10']) / float(len(summary_dict['precision_10']))
    recall10 =sum(summary_dict['recall_10']) / float(len(summary_dict['recall_10']))
    f_measure10 =sum(summary_dict['fmeasure_10']) / float(len(summary_dict['fmeasure_10']))
    precision20 =sum(summary_dict['precision_20']) / float(len(summary_dict['precision_20']))
    recall20 =sum(summary_dict['recall_20']) / float(len(summary_dict['recall_20']))
    f_measure20 =sum(summary_dict['fmeasure_20']) / float(len(summary_dict['fmeasure_20']))
    precision50 =sum(summary_dict['precision_50']) / float(len(summary_dict['precision_50']))
    recall50 =sum(summary_dict['recall_50']) / float(len(summary_dict['recall_50']))
    f_measure50 =sum(summary_dict['fmeasure_50']) / float(len(summary_dict['fmeasure_50']))
    precision100 =sum(summary_dict['precision_100']) / float(len(summary_dict['precision_100']))
    recall100 =sum(summary_dict['recall_100']) / float(len(summary_dict['recall_100']))
    f_measure100 =sum(summary_dict['fmeasure_100']) / float(len(summary_dict['fmeasure_100']))
    result_file.write("#########################################################################" + '\n')
    result_file.write("#########################################################################" + '\n')
    result_file.write("#########################################################################" + '\n')
    result_file.write("       AAAAVVVEEERRRRAAAAGGGGEEEE   VVVVAAAAALLLLUUUUUEEEEESSSSSS" + '\n')
    result_file.write("query id = " + str(q) + '\n')
    result_file.write("for k = 5 " + "precision = " + str(precision5) + "  " + "recall = " + str(
        recall5) + "  " + "f_measuere = " + str(f_measure5) + "  " + '\n')
    result_file.write("for k = 10 " + "precision = " + str(precision10) + "  " + "recall = " + str(
        recall10) + "  " + "f_measuere = " + str(f_measure10) + "  " + '\n')
    result_file.write("for k = 20 " + "precision = " + str(precision20) + "  " + "recall = " + str(
        recall20) + "  " + "f_measuere = " + str(f_measure20) + "  " + '\n')
    result_file.write("for k = 50 " + "precision = " + str(precision50) + "  " + "recall = " + str(
        recall50) + "  " + "f_measuere = " + str(f_measure50) + "  " + '\n')
    result_file.write("for k = 100 " + "precision = " + str(precision100) + "  " + "recall = " + str(
        recall100) + "  " + "f_measuere = " + str(f_measure100) + "  " + '\n')

    result_file.write("    Average Precision =  " + str(average_precsion) + '\n')
    result_file.write("    NDCG= " + str(summ) + '\n')
    result_file.write("    R-Precision =  " + str(r_precision) + '\n')
    result_file.write("#########################################################################" + '\n')

    #     fp,tp,fn,pr5,rc5,f5 = precision_calculations(rank_list, truth, 5)
    #     fp, tp, fn, pr10, rc10, f10 = precision_calculations(rank_list, truth, 10)
    #     fp, tp, fn, pr20, rc20, f20 = precision_calculations(rank_list, truth, 20)
    #     fp, tp, fn, pr50, rc50, f50 = precision_calculations(rank_list, truth, 50)
    #     fp, tp, fn, pr100, rc100, f100 = precision_calculations(rank_list, truth, 100)
    #
    #     pr_list=[pr5,pr10,pr20,pr50,pr100]
    #     rc_list=[rc5,rc10,rc20,rc50,rc100]
    #     f1_list=[f5,f10,f20,f50,f100]
    #
    #
    # # return(r_precision,average_precsion,NDCG,pr_list,rc_list,f1_list)






    #
    # path = '/Users/mohsennabian/Dropbox/Summer_2016/Info_Retrieval/HW5/query_url_dict.txt'
    # query_url_elasticsearch_dict = read_dictionary(path)
    #

    # combine_scores()

    # scores()
    # a,b,c=read_combined_qrel_file()



# path11 = '/Users/mohsennabian/Dropbox/Summer_2016/Info_Retrieval/cs6200_Mohsen_Nabian//HW5/ranklist_standard_format.txt'
# path22 = '/Users/mohsennabian/Dropbox/Summer_2016/Info_Retrieval/cs6200_Mohsen_Nabian/HW5/qrel_standard_format.txt'

path11 = '/Users/mohsennabian/Dropbox/Summer_2016/Info_Retrieval/cs6200_Mohsen_Nabian/HW1/bm25.txt'
path22='/Users/mohsennabian/Dropbox/Summer_2016/Info_Retrieval/cs6200_Mohsen_Nabian/HW1/qrels.adhoc.51-100.AP89.txt'


# r_precision1,average_precsion1,NDCG1,pr_list1,rc_list1,f1_list1=scores(path11,path22,1)
# r_precision2,average_precsion2,NDCG2,pr_list2,rc_list2,f1_list2=scores(path11,path22,2)
# r_precision3,average_precsion3,NDCG3,pr_list3,rc_list3,f1_list3=scores(path11,path22,3)
# r_precision4,average_precsion4,NDCG4,pr_list4,rc_list4,f1_list4=scores(path11,path22,4)


save_standard_rank_list()
make_standard_qrel()

scores(path11,path22)
