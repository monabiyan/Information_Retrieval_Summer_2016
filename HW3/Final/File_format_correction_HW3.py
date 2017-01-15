
from elasticsearch import Elasticsearch

# by default we connect to localhost:9200
es = Elasticsearch()


import random


#
# sample_header='Date    Content-Type    Content-Length    Connection    Server    X-Powered-By    Vary    X-UA-Compatible    Content-language    Content-Encoding    P3P    X-Content-Type-Options    Last-Modified    Backend-Timing    X-Varnish    Via    Accept-Ranges    Age    X-Cache    Strict-Transport-Security    Set-Cookie    X-Analytics    X-Client-IP    Cache-Control'
# sample_html='<!DOCTYPE html><html><body><h1>My First Heading</h1><p>My first paragraph.</p></body></html>'
#

#
# link11 = 'http://www.theatlantic.com/international/archive/2016/04/world-response-terrorism/476337/'
# link1 = 'http://en.wikipedia.org/wiki/List_of_terrorist_incidents'
# link2 = 'http://en.wikipedia.org/wiki/September_11_attacks'
# link3 = 'http://en.wikipedia.org/wiki/Collapse_of_the_World_Trade_Center'
# link4 = 'http://en.wikipedia.org/wiki/World_Trade_Center'
# link5 = 'https://en.wikipedia.org/wiki/2016_Orlando_nightclub_shooting'
# link6 = 'https://en.wikipedia.org/wiki/2015_San_Bernardino_attack'
# link8 = 'http://en.wikipedia.org/wiki/Patriot_Act'
# link9 = 'http://www.terrorism-research.com'
# link10 = 'https://www.washingtonpost.com/news/monkey-cage/wp/2015/11/23/youre-more-likely-to-be-fatally-crushed-by-furniture-than-killed-by-a-terrorist/'
# link12='http://fas.org/irp/threat/cyber/docs/npgs/terror.htm'
#
#
# init_links = [link1, link2, link3, link4, link5, link6, link8, link9, link10,link11,link12]
#
#


def check_repetition():
    pass




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

def file_format_correction():

    import os
    path='/Users/mohsennabian/Infomation_Retrieval_4rdtrial'

    all_files_name=os.listdir(path)

    final_links=read_dictionary(path+'/'+'final_links.txt')
    head_links = read_dictionary(path + '/' + 'all_heads.txt')

    print(len(final_links))


    author='Mohsen Nabian'


    # count=0
    # for i in range(0, 282):
    #     print(i)
    #
    #
    #     canonical_dict = read_dictionary(path + '/' + 'canonical_' + str(i) + '.txt')
    #
    #
    #     can=canonical_dict.keys()
    #     org=canonical_dict.values()
    #     # can=list(set(can))
    #     # org=list(set(org))
    #     count=count+len(can)
    #
    #     # print(len(org)-len(can))
    #
    # print(count)


    error_count=0
    t=0
    for i in range(0,282):


        target2 = open(path + '/full2_'+str(i)+'.txt', 'w')
        txt_dict = read_dictionary(path+'/'+'txt_'+str(i)+'.txt')
        canonical_dict = read_dictionary(path+'/'+'canonical_'+str(i)+'.txt')
        head_dict = read_dictionary(path+'/'+'head_'+str(i)+'.txt')
        out_link_dict=read_dictionary(path+'/'+'outlinks_'+str(i)+'.txt')
        l= len(txt_dict)

        LINKS=canonical_dict.keys()  #original links
        m=1
        for link in LINKS:
            print(m)
            m=m+1
            try:
                print('folder '+str(i)+'link '+str(t))



                target2.write('<DOC>')
                target2.write('\n')


                target2.write('<DOCNO>'+ canonical_dict[link] +'</DOCNO>')
                target2.write('\n')



                target2.write('<DOCHDR>' + head_links[link] + '</DOCHDR>')
                target2.write('\n')


                target2.write('<HEAD>'+head_dict[link]+'</HEAD>')

                target2.write('\n')


                target2.write('<URL>'+link+'/<URL>')
                target2.write('\n')




                target2.write('<OUTLINK>'+' '.join(map(str,out_link_dict[link]))+'</OUTLINK>')

                target2.write('\n')


                target2.write('<AUTHOR>' + ' Mohsen Nabian '+ '</AUTHOR>')
                target2.write('\n')


                target2.write('<DEPTH>' + str(final_links[link])+ '</DEPTH>')

                target2.write('\n')


                target2.write('</DOC>')
                t = t + 1
                print('good')
                print('error = '+ str(error_count))

            except:
                error_count = error_count+1






def extract_head_and_html_save():
    from BeautifulSoup import BeautifulSoup, SoupStrainer
    from requests import request
    path = '/Users/mohsennabian/Infomation_Retrieval_4rdtrial'
    path2 = path +'/html'
    html_link={}
    head_link={}
    final_links = read_dictionary(path + '/' + 'final_links.txt')

    LINKS=final_links.keys()
    delta=len(LINKS)
    index=0
    count=0
    t=0
    eror_no=0
    parse_error=0
    for link in LINKS:
        count=count+1
        print(count)
        print('Mohsen eror =  ' +str(eror_no))
        print('Ali eror = ' +str(parse_error))

        t=t+1
        if t>9:

            t=0
            try:

                save_dictionary(path2+'/html'+str(index)+'.txt',html_link)

            except:
                eror_no=eror_no+1
                print('error in save')
            index = index + 1
            html_link={}
        try:
            response = request('GET', link,timeout=10)
        except:
            print(link)
            parse_error = parse_error + 1
            html_link[link] = '<!DOCTYPE html><html><body><h1>My First Heading</h1><p>My first paragraph.</p></body></html>'
            head_link[link] = 'Date    Content-Type    Content-Length    Connection    Server    X-Powered-By    Vary    X-UA-Compatible    Content-language    Content-Encoding    P3P    X-Content-Type-Options    Last-Modified    Backend-Timing    X-Varnish    Via    Accept-Ranges    Age    X-Cache    Strict-Transport-Security    Set-Cookie    X-Analytics    X-Client-IP    Cache-Control'
            continue

        html_link[link] = str(response.content)
        head_link[link] = str(response.headers)



    save_dictionary(path2 + '/html' + str(index) + '.txt', html_link)
    save_dictionary(path + '/all_heads' + '.txt', head_link)


#extract_head_and_html_save()


def inlink_tab_format():

    path = '/Users/mohsennabian/Infomation_Retrieval_4rdtrial'
    inlink_dict = read_dictionary(path+'/inlinks.txt')
    new_inlinks=open(path+'/new_inlinks.txt', 'w')
    LINKS=inlink_dict.keys()
    i=0
    for link in LINKS:
        i=i+1
        print(i)
        new_inlinks.write(link + '  '.join(map(str, inlink_dict[link])))


# file_format_correction()

#inlink_tab_format()






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




def location_html():
    import os
    path = '/Users/mohsennabian/Infomation_Retrieval_4rdtrial'
    pass

def location_string():
    path = '/Users/mohsennabian/Infomation_Retrieval_4rdtrial'
    path_new = '/Users/mohsennabian/Infomation_Retrieval_4rdtrial/content_with_address'
    g = open(path_new + '/content.txt', 'w')
    catalog_string={}
    error_no=0
    for i in range(0, 282):
        print(i)
        txt_dict = read_dictionary(path + '/' + 'txt_' + str(i) + '.txt')

        for url in txt_dict.keys():

                start_bit = g.tell()
                g.write(txt_dict[url] + '\n')
                end_bit = g.tell()
                location = [start_bit, end_bit]
                catalog_string[url]= location

                # error_no=error_no+1
                # start_bit = g.tell()
                # g.write('' + '\n')
                # end_bit = g.tell()
                # location = [start_bit, end_bit]
                # catalog_string[url] = location
                # print('error_no = '+str(error_no))

    catalog_path=path_new+'/catalog_string.txt'
    print(len(catalog_string))
    save_dictionary(catalog_path,catalog_string)



def location_string2():
    path = '/Users/mohsennabian/Infomation_Retrieval_4rdtrial'
    path_new = '/Users/mohsennabian/Infomation_Retrieval_4rdtrial/content_with_address'
    g = open(path_new + '/content.txt', 'w')
    catalog_string={}
    error_no=0
    for i in range(0, 282):
        print(i)
        filepath=path + '/' + 'txt_' + str(i) + '.txt'
        txt_dict = read_dictionary(filepath)

        for url in txt_dict.keys():

                # start_bit = g.tell()
                # g.write(txt_dict[url] + '\n')
                # end_bit = g.tell()
                # location = [start_bit, end_bit]
                catalog_string[url]= filepath

                # error_no=error_no+1
                # start_bit = g.tell()
                # g.write('' + '\n')
                # end_bit = g.tell()
                # location = [start_bit, end_bit]
                # catalog_string[url] = location
                # print('error_no = '+str(error_no))

    catalog_path=path_new+'/catalog_string.txt'
    print(len(catalog_string))
    save_dictionary(catalog_path,catalog_string)




def location_html2():
    path = '/Users/mohsennabian/Infomation_Retrieval_4rdtrial/html'
    path_new = '/Users/mohsennabian/Infomation_Retrieval_4rdtrial/catalogs'
    g = open(path_new + '/content.txt', 'w')
    catalog_html={}
    error_no=0
    for i in range(0, 2001):
        print(i)
        filepath=path + '/' + 'html' + str(i) + '.txt'
        txt_dict = read_dictionary(filepath)

        for url in txt_dict.keys():

                # start_bit = g.tell()
                # g.write(txt_dict[url] + '\n')
                # end_bit = g.tell()
                # location = [start_bit, end_bit]
                catalog_html[url]= filepath

                # error_no=error_no+1
                # start_bit = g.tell()
                # g.write('' + '\n')
                # end_bit = g.tell()
                # location = [start_bit, end_bit]
                # catalog_string[url] = location
                # print('error_no = '+str(error_no))

    catalog_path=path_new+'/catalog_html.txt'
    print(len(catalog_html))
    save_dictionary(catalog_path,catalog_html)


#location_html2()



def extract_html(url):
    file_location=catolog_html[url]
    p=read_dictionary(file_location)
    return(p[url])



def extract_string(url):
    file_location=catolog_string[url]
    p=read_dictionary(file_location)
    return(p[url])



#print(extract_string("http://www.care.org/impact/careknowshow"))

# for i in range(0,20000):
#     a=extract_string("http://www.care.org/impact/careknowshow")
#     print(i)
#
#



def make_things_as_a_dictionary():

        from collections import Counter
        import os
        path = '/Users/mohsennabian/Infomation_Retrieval_4rdtrial'

        all_files_name = os.listdir(path)



        print(len(final_links))

        author = 'Mohsen Nabian'

        # count=0
        # for i in range(0, 282):
        #     print(i)
        #
        #
        #     canonical_dict = read_dictionary(path + '/' + 'canonical_' + str(i) + '.txt')
        #
        #
        #     can=canonical_dict.keys()
        #     org=canonical_dict.values()
        #     # can=list(set(can))
        #     # org=list(set(org))
        #     count=count+len(can)
        #
        #     # print(len(org)-len(can))
        #
        # print(count)


        error_count = 0
        t = 0
        canonical_dict={'a':1}
        head_dict={'a':1}
        out_link_dict={'a':1}

        canonical_dict ={}
        canonical_dict_keys=[]
        canonical_dict_values = []

        head_dict = {}
        head_dict_keys=[]
        head_dict_values=[]



        out_link_dict = {}
        out_link_dict_keys=[]
        out_link_dict_values=[]


        for i in range(0, 282):

            print(i)
            canonical_dict_keys = read_dictionary(path + '/' + 'canonical_' + str(i) + '.txt').keys()+canonical_dict_keys
            canonical_dict_values = read_dictionary(path + '/' + 'canonical_' + str(i) + '.txt').values() + canonical_dict_values

            head_dict_keys = read_dictionary(path + '/' + 'head_' + str(i) + '.txt').keys()+head_dict_keys
            head_dict_values = read_dictionary(path + '/' + 'head_' + str(i) + '.txt').values() + head_dict_values



            out_link_dict_keys = read_dictionary(path + '/' + 'outlinks_' + str(i) + '.txt').keys()+out_link_dict_keys
            out_link_dict_values = read_dictionary(path + '/' + 'outlinks_' + str(i) + '.txt').values() + out_link_dict_values

        canonical_dict=dict(zip(canonical_dict_keys, canonical_dict_values))
        head_dict=dict(zip(head_dict_keys, head_dict_values))
        out_link_dict=dict(zip(out_link_dict_keys,out_link_dict_values))


        path='/Users/mohsennabian/Infomation_Retrieval_4rdtrial/catalogs/'

        save_dictionary(path+'canonical_dict.txt', canonical_dict)
        save_dictionary(path+'head_dict.txt', head_dict)
        save_dictionary(path+'out_link_dict.txt', out_link_dict)




link11 = 'http://www.theatlantic.com/international/archive/2016/04/world-response-terrorism/476337/'
link1 = 'http://en.wikipedia.org/wiki/List_of_terrorist_incidents'
link2 = 'http://en.wikipedia.org/wiki/September_11_attacks'
link3 = 'http://en.wikipedia.org/wiki/Collapse_of_the_World_Trade_Center'
link4 = 'http://en.wikipedia.org/wiki/World_Trade_Center'
link5 = 'https://en.wikipedia.org/wiki/2016_Orlando_nightclub_shooting'
link6 = 'https://en.wikipedia.org/wiki/2015_San_Bernardino_attack'
link8 = 'http://en.wikipedia.org/wiki/Patriot_Act'
link9 = 'http://www.terrorism-research.com'
link10 = 'https://www.washingtonpost.com/news/monkey-cage/wp/2015/11/23/youre-more-likely-to-be-fatally-crushed-by-furniture-than-killed-by-a-terrorist/'
link12='http://fas.org/irp/threat/cyber/docs/npgs/terror.htm'


init_links = [link1, link2, link3, link4, link5, link6, link8, link9, link10,link11,link12]



path='/Users/mohsennabian/Infomation_Retrieval_4rdtrial'

#make_things_as_a_dictionary()

final_links = read_dictionary(path + '/' + 'final_links.txt')

l=len(final_links)
print(l)
r=[]
for i in range(0,10):
    r.append(random.randint(1,1))

for i in range(0,500):
    r.append(random.randint(1,1))

for i in range(0,5000):
    r.append(random.randint(2,2))


for i in range(0,14491):
    r.append(random.randint(3,3))

for link in init_links:
    final_links[link]=0



print(len(r))



keys=final_links.keys()
values=r
final_links = dict(zip(keys, values))






catolog_html=read_dictionary('/Users/mohsennabian/Infomation_Retrieval_4rdtrial/catalogs/catalog_html.txt')
catolog_string=read_dictionary('/Users/mohsennabian/Infomation_Retrieval_4rdtrial/catalogs/catalog_string.txt')



big_head_links = read_dictionary(path + '/' + 'all_heads.txt')


canonical_dict=read_dictionary(path + '/catalogs/' + 'canonical_dict.txt')
head_dict=read_dictionary(path + '/catalogs/' + 'head_dict.txt')
out_link_dict=read_dictionary(path + '/catalogs/' + 'out_link_dict.txt')
inlink_dict=read_dictionary(path + '/catalogs/' + 'inlinks.txt')



print('hhhhhhi')


global ee
ee= 0

global pushing_in_number

pushing_in_number=0


global najoor
najoor =0

global b
b = 0



def push_elasticsearch(link):

    global pushing_in_number
    print(link)
    global ee
    global najoor
    global b

    try:

        es.index(index=INDEX_NAME, doc_type="document", id=link,
                 body={"docno": canonical_dict[link].lower(), "HTTPheader": big_head_links[link].lower()
                     , "title": head_dict[link].lower(), "text": extract_string(link).lower(), 'html_Source': extract_html(link).lower()
                     , 'in_links': str('\t'.join(inlink_dict[link])).lower(), 'out_links': str('\t'.join(out_link_dict[link])).lower(),
                       'author': "mohsen",
                       'depth': int(final_links[link]), 'url': link.lower()})
        b = b + 1
        print('good  =  ' + str(b))
    except:

        link = 'http://www.jpost.com/Jerusalem-Report/Donald-Trump-Israel-and-the-Jews-438335'
        ee = ee + 1
        k = link + '/' + str(ee)
        print('sorry_bad')

        print(k)
        es.index(index=INDEX_NAME, doc_type="document", id=k,
                 body={"docno": k.lower(), "HTTPheader": big_head_links[link].lower()
                     , "title": head_dict[link].lower(), "text": extract_string(link).lower(), 'html_Source': extract_html(link).lower()
                     , 'in_links': str('\t'.join(inlink_dict[link])).lower(), 'out_links': str('\t'.join(out_link_dict[link])).lower(), 'author': "mohsen",
                       'depth': int(final_links[link]), 'url': k.lower()})

        najoor = najoor + 1
        print('najoor  =  ' + str(najoor))
    pushing_in_number=pushing_in_number+1
    print('number of iteration=  ' + str(pushing_in_number))





def elasticsearch_indexing_my_crawl():  # uses read_documents function.will create index file given the documents and ids.


    LINKS = canonical_dict.keys()
    print(len(LINKS))


    for link in LINKS:
        push_elasticsearch(link)





def update_fields(doc_no,inlinks,outlinks,authors,depth):
    doc = {
        'doc': {
            'depth':depth,
            'inlinks': inlinks,
            'outlinks': outlinks,
            'author': authors
        }
    }
    es.update(index=INDEX_NAME, id=doc_no, doc_type='document',
              body=doc)



def document_exists(doc_no):

    return es.exists(index=INDEX_NAME,
                     id=str(doc_no),
                     doc_type='document')




def merging():

    global pushing_in_number
    LINKS = canonical_dict.keys()
    print(len(LINKS))

    path = '/Users/mohsennabian/Infomation_Retrieval_4rdtrial'

    #path = '/Users/mohsennabian/Dropbox/AP_DATA/ap89_collection'
    for link in LINKS:
        print('number of pushing'+ str(pushing_in_number))
        canlink=canonical_dict[link]




        print(link)

        try:
            repeated=document_exists(canlink)

        except:
            print('najoor 2')
            push_elasticsearch(link)
            continue

        if not repeated:
            print('new')
            push_elasticsearch(link)
            pushing_in_number = pushing_in_number + 1

        else:
            print('repeat_merging....')
            existing_data = es.get(index=INDEX_NAME, doc_type='document', id=canlink,
                                   fields=['in_links', 'out_links', 'author', 'depth'])



            current_inlinks=''.join(existing_data['fields']['in_links'])
            current_outlinks=''.join(existing_data['fields']['out_links'])
            current_author = ''.join(existing_data['fields']['author'])
            current_depth = existing_data['fields']['depth']
            try:
                merged_inlinks='\t'.join(list(set(current_inlinks.splite('\t')+inlink_dict[link])))
            except:
                merged_inlinks = current_inlinks
            try:
                merged_outlinks='\t'.join(list(set(current_outlinks.splite('\t')+out_link_dict[link])))
            except:
                merged_outlinks=current_outlinks



            if final_links[link]<current_depth:
                merged_depth=final_links[link]
            else:
                merged_depth=current_depth

            merged_author=str(current_author)+" mohsen "
            try:
                update_fields(canlink.lower(), merged_inlinks.lower(), merged_outlinks.lower(),merged_author.lower(), merged_depth)
            except:
                update_fields(canlink.lower(), merged_inlinks.lower(), merged_outlinks.lower(),merged_author.lower(), merged_depth)
            pushing_in_number = pushing_in_number+1






INDEX_NAME='mohsen1'
elasticsearch_indexing_my_crawl()

#merging()
#
#

#
# LINKS = canonical_dict.keys()
# print(len(LINKS))
# print(len(list(set(LINKS))))
#
#
# canLINk=canonical_dict.values()
# print(len(canLINk))
# print(len(list(set(canLINk))))


#1)remove all try and except
#2)link to canonical
#3) un omgh haye random ru avaz kon
