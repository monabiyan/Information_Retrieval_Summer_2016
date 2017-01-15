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
from datetime import datetime
from elasticsearch import Elasticsearch
from elasticsearch_dsl import Search



def get_all_ids_from_elasticsearh_as_list():
    from elasticsearch import Elasticsearch
    from elasticsearch_dsl import Search
    es = Elasticsearch()
    s = Search(using=es, index='four')

    s = s.fields([])  # only get ids, otherwise `fields` takes a list of field names
    ids = [h.meta.id for h in s.scan()]
    return(ids)


def get_and_save_all_inlinks_and_outlinks_elasticsearch():
    es = Elasticsearch()
    all_ids_list=get_all_ids_from_elasticsearh_as_list()
    inlinks_dict={}
    outlinks_dict={}
    all_nodes_dict={}
    number_of_out_links_dict={}
    all_parsed_nodes_dict={}
    all_nodes_dict={}
    index=0
    for url_id in all_ids_list:
        index=index+1
        print(str(index)+'-'+url_id)
        existing_data = es.get(index='four', doc_type='document', id=url_id,
                                                       fields=['in_links', 'out_links'])
        inlinks = set((''.join(existing_data['fields']['in_links'])).split('\t')).intersection(set(all_ids_list))
        # inlinks = [x for x in inlinks if x  in all_ids_list]
        outlinks = set((''.join(existing_data['fields']['out_links'])).split('\t')).intersection(set(all_ids_list))
        # outlinks= [x for x in outlinks if x  in all_ids_list]


        n = len(inlinks)
        values_list = [True] * n
        inlink_urls = dict(zip(inlinks, values_list))
        inlinks_dict[url_id]=inlink_urls
        # all_nodes_dict.update(inlink_urls)



        m = len(outlinks)
        values_list = [True] * m
        outlinks_urls = dict(zip(outlinks, values_list))
        outlinks_dict[url_id] = outlinks_urls
        # all_nodes_dict.update(outlinks_urls)
        all_parsed_nodes_dict[url_id]=True

        number_of_out_links_dict[url_id]=len(outlinks)

    save_dictionary('/Users/mohsennabian/HW4/merge_inlinks_dict.txt', inlinks_dict)

    save_dictionary('/Users/mohsennabian/HW4/merge_number_of_out_links_dict.txt', number_of_out_links_dict)
    save_dictionary('/Users/mohsennabian/HW4/merge_outlinks_dict.txt', outlinks_dict)
    save_dictionary('/Users/mohsennabian/HW4/merge_all_parsed_nodes_dict.txt', all_parsed_nodes_dict)
    #save_dictionary('/Users/mohsennabian/HW4/merge_all_nodes_dict.txt', all_nodes_dict)

def outlink_from_inlinks_only(my_inlink_dict):
    merge_number_of_out_links_dict={}
    outlink_from_inlink_dict={}
    heads=my_inlink_dict.keys()
    for head in heads:
        for url in my_inlink_dict[head].keys():
            print('hi')
            if url not in outlink_from_inlink_dict:
                outlink_from_inlink_dict[url]={head:True}
            else: outlink_from_inlink_dict[url].update({head:True})
    save_dictionary('/Users/mohsennabian/HW4/merge_outlinks_dict.txt',outlink_from_inlink_dict)

    for url in outlink_from_inlink_dict.keys():
        merge_number_of_out_links_dict[url]=len(outlink_from_inlink_dict[url])
    save_dictionary('/Users/mohsennabian/HW4/merge_number_of_out_links_dict.txt', merge_number_of_out_links_dict)



def save_sink_node_file():
    number_of_outlinks_dict = read_dictionary('/Users/mohsennabian/HW4/merge_number_of_out_links_dict.txt')
    merge_all_parsed_nodes_dict=read_dictionary('/Users/mohsennabian/HW4/merge_all_parsed_nodes_dict.txt')
    aall=merge_all_parsed_nodes_dict.keys()
    sink_dict = {}
    for id in aall:
        if id not in number_of_outlinks_dict.keys():
            sink_dict.update({id: True})

    for id in number_of_outlinks_dict.keys():
        if number_of_outlinks_dict[id]==0:
            sink_dict.update({id:True})
    save_dictionary('/Users/mohsennabian/HW4/merge_sink_dict.txt',  sink_dict)



def M(graph_dict,p):   #M(p) is the set of pages that link to page p

   return(graph_dict[p].keys())


def L(number_of_outlinks_dict,q):   #L(q) is the number of out-links from page q

     return(number_of_outlinks_dict[q])




def difference():
    global PR
    global new_PR
    N = len(new_PR)
    y = 0
    if N == 0 :
        return(999)

    for key in PR.keys():
        key = key.replace('\n', '')
        y=abs(PR[key]-new_PR[key])+y
    return(y/N)



def compute_page_rank(graph_dict,all_parsed_nodes_dict,number_of_outlinks_dict,sink_dict):

    S = sink_dict.keys()
    P = all_parsed_nodes_dict.keys()
    N = len(P)
    print(N)
    d = 0.85
    global PR
    global new_PR
    delta=9999
    PR={}
    new_PR={}
    for p in P :
        PR[p]=1/N
    while delta>0.0000000001:
        print('hi')
        sinkPR = 0
        for p in S:
            p = p.replace('\n', '')
            sinkPR=sinkPR+PR[p]
        for p in P:

            p=p.replace('\n','')
            if p=='': continue
            new_PR[p]=(1-d)/N
            new_PR[p]=new_PR[p]+d*sinkPR/N
            for q in M(graph_dict,p):
                new_PR[p]=new_PR[p]+d*PR[q]/L(number_of_outlinks_dict,q)
        delta = difference()
        print(delta)
        for p in P :
            p = p.replace('\n', '')

            PR[p] = new_PR[p]


    save_dictionary('/Users/mohsennabian/HW4/merged_PR.txt', PR)


def dictionary_into_2sorted_list_and_save(path_to_load,path_to_save):
    mydict=read_dictionary(path_to_load)
    myvalue=sorted(mydict.values(),reverse=True)
    mykey=sorted(mydict, key=mydict.__getitem__,reverse=True)
    g=open(path_to_save,'w')

    for i in range(0,len(mykey)):


        sentence = ((mykey[i]) + '   =  '  + str(myvalue[i]) +'\n').encode('utf8')


        # sentense = unicode(str(sentence), errors='ignore').encode("utf-8")
        try:
            g.write(sentence)
        except:
            print('bad')




PR = {}
new_PR = {}

# get_and_save_all_inlinks_and_outlinks_elasticsearch()

#
all_parsed_nodes_dict = read_dictionary('/Users/mohsennabian/HW4/merge_all_parsed_nodes_dict.txt')
graph_dict = read_dictionary('/Users/mohsennabian/HW4/merge_inlinks_dict.txt')  # graph_dict={head1={tail1:true,tail2:true}}

# outlink_from_inlinks_only(graph_dict)
# save_sink_node_file()


number_of_outlinks_dict = read_dictionary('/Users/mohsennabian/HW4/merge_number_of_out_links_dict.txt')
sink_dict = read_dictionary('/Users/mohsennabian/HW4/merge_sink_dict.txt')
#
#
#
#
#
compute_page_rank(graph_dict, all_parsed_nodes_dict, number_of_outlinks_dict, sink_dict)
#
PR = read_dictionary('/Users/mohsennabian/HW4/merged_PR.txt')

import operator
sorted_PR = sorted(PR.items(), key=operator.itemgetter(1), reverse=True)
print(sorted_PR[0:100])




path_to_load='/Users/mohsennabian/HW4/merged_PR.txt'
path_to_save='/Users/mohsennabian/HW4/merged_PR_sorted.txt'
dictionary_into_2sorted_list_and_save(path_to_load, path_to_save)

