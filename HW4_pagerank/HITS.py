from elasticsearch import Elasticsearch

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




def elasticsearch_score(word):
    from elasticsearch import Elasticsearch
    es = Elasticsearch()
    global node_score_dict
    total_hit = es.search(index='four', doc_type='document', body={"query": {
        "match": {
            "text": word
        }
    },
        "explain": "true"})['hits']['total']

    print('number of hits for ', word, 'is ', total_hit)
    total_hit = int(total_hit)
    orig_total_hit = total_hit
    if (total_hit > 2000):
        total_hit = 2000
    score_root = es.search(index='four', doc_type='document', size=total_hit, body={"query": {
        "match": {
            "text": word
        }
    },
        "explain": "true"})['hits']['hits']


    for i in range(0,total_hit):
        print(i)
        id=score_root[i]['_id']
        score=score_root[i]['_score']
        node_score_dict[id]=node_score_dict[id]+score



# all_nodes=get_all_ids_from_elasticsearh_as_list()
# #
# global node_score_dict
# node_score_dict={}
# for id in all_nodes:
#     node_score_dict[id]=0
# query_list=['terror','shooting','massacare','terrorist']
# for word in query_list:
#     print(word)
#     elasticsearch_score(word)
#
#
# save_dictionary('/Users/mohsennabian/HW4/root_node_score_dict.txt',node_score_dict)
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




node_score_dict=read_dictionary('/Users/mohsennabian/HW4/root_node_score_dict.txt')

all_parsed_nodes_dict = read_dictionary('/Users/mohsennabian/HW4/merge_all_parsed_nodes_dict.txt')
graph_dict = read_dictionary('/Users/mohsennabian/HW4/merge_inlinks_dict.txt')  # graph_dict={head1={tail1:true,tail2:true}}


number_of_outlinks_dict = read_dictionary('/Users/mohsennabian/HW4/merge_number_of_out_links_dict.txt')
sink_dict = read_dictionary('/Users/mohsennabian/HW4/merge_sink_dict.txt')
outlink_from_inlink_dict = read_dictionary('/Users/mohsennabian/HW4/merge_outlinks_dict.txt')






#
#
# myvalue = sorted(node_score_dict.values(), reverse=True)[0:1000]
# mykey = sorted(node_score_dict, key=node_score_dict.__getitem__, reverse=True)[0:1000]
# # g = open('/Users/mohsennabian/HW4/root_top_1000.txt', 'w')
#
# for i in range(0, 1000):
#     print(mykey[i])
new_graph_inlinks={}
new_graph_outlinks={}

base_dict={}
import random
my_root=sorted(node_score_dict, key=node_score_dict.__getitem__, reverse=True)[0:1000]
print(my_root)

# outlink_from_inlink_dict
n=0
for root in my_root:
    if root  in  outlink_from_inlink_dict:     #some roots are sink
        out_urls_dict=outlink_from_inlink_dict[root]
        base_dict.update(out_urls_dict)
        for url in out_urls_dict.keys():
            if url!=root:
                if url not in new_graph_inlinks: new_graph_inlinks[url]=[root]
                else: new_graph_inlinks[url] = list(set(new_graph_inlinks[url]+[root]))

    else:
        print(root)
    base_dict.update({root:True})



for root in my_root:
    in_urls_dict=graph_dict[root]
    if len(in_urls_dict)>1000:
        random_list=random.sample(in_urls_dict.keys(), 1000)
        in_urls_dict= dict.fromkeys(random_list, True)
    if root not in new_graph_inlinks: new_graph_inlinks[root] = list(set(in_urls_dict.keys()))
    else: new_graph_inlinks[root] = list(set(in_urls_dict.keys()+new_graph_inlinks[root]))
    base_dict.update(in_urls_dict)






for link in new_graph_inlinks:
    inlinks_list=new_graph_inlinks[link]
    for inlink in inlinks_list:
        if inlink not in new_graph_outlinks:new_graph_outlinks[inlink]=[link]
        else: new_graph_outlinks[inlink]=new_graph_outlinks[inlink]+[link]




save_dictionary('/Users/mohsennabian/HW4/new_graph_inlinks.txt',new_graph_inlinks)
save_dictionary('/Users/mohsennabian/HW4/new_graph_outlinks.txt',new_graph_outlinks)

print(len(base_dict))

print('hi')
print(len(new_graph_outlinks))
print(len(new_graph_inlinks))
print('by')
s=0
for link in new_graph_outlinks:
    s=s+len(new_graph_outlinks[link])
print(s)
s=0
for link in new_graph_inlinks:
    s=s+len(new_graph_inlinks[link])
print(s)


import math




hub={}
authority={}

for link in base_dict.keys():

    hub[link] = 1
    authority[link] = 1

N=len(hub)




diff=100
while diff>0.00000000000000000001:
    print('ghasem')
    hub_old=hub.copy()
    for link in new_graph_inlinks.keys():
        inlinks=new_graph_inlinks[link]
        s=0
        for inlink in inlinks:
            s=s+hub[inlink]

        authority[link]=s



    for link in new_graph_outlinks.keys():
        outlinks=new_graph_outlinks[link]
        s=0
        for outlink in outlinks:
            s=s+authority[outlink]
        hub[link]=s

    kk=0
    pp=0
    for link in base_dict.keys():
        kk=kk+hub[link]*hub[link]
        pp=pp+authority[link]*authority[link]



    for link in base_dict.keys():
        hub[link] = hub[link]/math.sqrt(kk)
        authority[link] =  authority[link]/math.sqrt(pp)
        # print(hub[link])

    m=0

    # for link in hub.keys():
    #    print(hub[link])
    #


    for link in hub.keys():
        # print(hub_old[link])
        m = abs(hub[link]-hub_old[link])+m
    diff=float(m)
    print(diff)


save_dictionary('/Users/mohsennabian/HW4/hub_dict.txt',hub)
save_dictionary('/Users/mohsennabian/HW4/authority_dict.txt',authority)
dictionary_into_2sorted_list_and_save('/Users/mohsennabian/HW4/hub_dict.txt','/Users/mohsennabian/HW4/hub_demo.txt')
dictionary_into_2sorted_list_and_save('/Users/mohsennabian/HW4/authority_dict.txt','/Users/mohsennabian/HW4/authority_demo.txt')

#
# print(len(all_parsed_nodes_dict.keys()))
#
#
#
#
# print(len(outlink_from_inlink_dict.keys()))
#
#
# sum=0
# for url in outlink_from_inlink_dict:
#  sum=sum+len(outlink_from_inlink_dict[url])
# print(sum)
#
# sum=0
# for url in graph_dict:
#  sum=sum+len(graph_dict[url])
# print(sum)

# print(len(graph_dict['https://en.wikipedia.org/wiki/Brooklyn_Bridge_Shooting']))
# print(len(outlink_from_inlink_dict['https://en.wikipedia.org/wiki/Brooklyn_Bridge_Shooting']))
#
# index=0
# es = Elasticsearch()
# for url_id in all_parsed_nodes_dict.keys():
#
#     index = index + 1
#     # print(str(index) + '-' + url_id)
#     # print('ghasem')
#     existing_data = es.get(index='four', doc_type='document', id=url_id,
#                            fields=['in_links', 'out_links','author'])
#     inlinks = set((''.join(existing_data['fields']['in_links'])).split('\t')).intersection(set(all_parsed_nodes_dict.keys()))
#     if len(inlinks)<1:
#         print('baaaaad'+ str(existing_data['fields']['author']))
#     # ss=len((''.join(existing_data['fields']['in_links'])).split('\t'))
#     # if ss==0:
#     #     print('dadi')
#
#
