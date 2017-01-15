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



def read_virgil_file():
    path_data='/Users/mohsennabian/HW4/wt2g_inlinks.txt'
    g = open(path_data, 'r')

    graph=[]
    all_links=[]
    inlinks_dict={}

    index=0
    mmm={}
    all_nodes_dict ={}
    while next != "":
        next = g.readline()
        if next=='': continue
        line=next
        # print(next)
        line=line.split(' ')
        if '\n' in line[0]:
            print('yes')
            line[0]=line[0].replace('\n','')
        # else:  line.replace('\n','')


        if '\n' in line: line.remove('\n')

        print(line)
        keys_list=line[1:len(line)]

        n=len(keys_list)
        values_list=[True] * n
        inlink_urls=dict(zip(keys_list, values_list))


        inlinks_dict[line[0]]=inlink_urls
        all_nodes_dict[line[0]] = True
        all_nodes_dict.update(inlink_urls)

        index = index + 1
        print(index)
        # if index==2:
        #     print(inlinks_dict)
        #     break

    save_dictionary('/Users/mohsennabian/HW4/virgil_dict.txt', inlinks_dict)
    save_dictionary('/Users/mohsennabian/HW4/all_nodes_dict.txt', all_nodes_dict)








def M(graph_dict,p):   #M(p) is the set of pages that link to page p

   return(graph_dict[p].keys())


def L(number_of_outlinks_dict,q):   #L(q) is the number of out-links from page q
        return(number_of_outlinks_dict[q])



def compute_number_of_outlinks(graph_dict,all_nodes_dict):

    outlink_number_dict={}
    print('DONEEE!!')
    for node in all_nodes_dict.keys():
        outlink_number_dict[node]=0
    print('tanha')
    for nodes_dict in graph_dict.values():
        for node in nodes_dict.keys():
            outlink_number_dict[node]=outlink_number_dict[node]+1

    save_dictionary('/Users/mohsennabian/HW4/number_of_outlinks.txt', outlink_number_dict)


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





def compute_page_rank(graph_dict,all_nodes_dict,number_of_outlinks_dict,sink_dict):
    S = sink_dict.keys()
    P = all_nodes_dict.keys()
    N = len(P)
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
            new_PR[p]=(1-d)/N
            new_PR[p]=new_PR[p]+d*sinkPR/N
            for q in M(graph_dict,p):
                new_PR[p]=new_PR[p]+d*PR[q]/L(number_of_outlinks_dict,q)
        delta = difference()
        print(delta)
        for p in P :
            p = p.replace('\n', '')

            PR[p] = new_PR[p]


    save_dictionary('/Users/mohsennabian/HW4/PR.txt', PR)


def dictionary_into_2sorted_list_and_save(path_to_load, path_to_save):
    mydict = read_dictionary(path_to_load)
    myvalue = sorted(mydict.values(),reverse=True)
    mykey = sorted(mydict, key=mydict.__getitem__,reverse=True)
    g = open(path_to_save, 'w')
    for i in range(0, len(mykey)):
        g.write(str(mykey[i]) + '   =  ' + str(myvalue[i]) + '\n')







#read_virgil_file()
graph_dict = read_dictionary('/Users/mohsennabian/HW4/virgil_dict.txt')  #graph_dict={head1={tail1:true,tail2:true}}
all_nodes_dict = read_dictionary('/Users/mohsennabian/HW4/all_nodes_dict.txt')
#compute_number_of_outlinks(graph_dict,all_nodes_dict)
number_of_outlinks_dict = read_dictionary('/Users/mohsennabian/HW4/number_of_outlinks.txt')
#S(number_of_outlinks_dict)
sink_dict = read_dictionary('/Users/mohsennabian/HW4/sink_dict.txt')

PR={}
new_PR={}


compute_page_rank(graph_dict,all_nodes_dict,number_of_outlinks_dict,sink_dict)

PR= read_dictionary('/Users/mohsennabian/HW4/PR.txt')

import operator
sorted_PR = sorted(PR.items(), key=operator.itemgetter(1),reverse=True)
print(sorted_PR[0:100])


path_to_load='/Users/mohsennabian/HW4/PR.txt'
path_to_save='/Users/mohsennabian/HW4/PR_sorted.txt'
dictionary_into_2sorted_list_and_save(path_to_load, path_to_save)
s=0
for value in PR.values():
   s=value+s
   print(s)
