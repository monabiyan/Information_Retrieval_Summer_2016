

global url_txt
url_txt = {}

global url_inlinks
url_inlinks={}

global url_outlinks
url_outlinks={}

global url_domain
url_domain={}

global url_wave_number
url_wave_number={}

global url_score
url_score={}

global parent
parent={}

global start_link
start_link=[]

global all_links
all_links=[]

global current_links
current_links=[]

global query_list


global DM_robot
DM_robot={}

global anchor
anchor={}

global url_soup
url_soup={}



global index
index=1

global url_visited
url_visited={}

global final_corpus
final_corpus={}

global PQ
from pqdict import pqdict
PQ=pqdict({})


global max_link
max_link=25000

global visited
visited={}

global url_all_outlinks
url_all_outlinks={}

global url_head
url_head={}

global url_canonical
url_canonical={}


global query_lower
query_lower = []


global canonical_url_visited
canonical_url_visited={}

global count
count=1

global bad_list
global bad_list1
global bad_list2

global domain_time_visited
domain_time_visited={}


from reppy.cache import RobotsCache

global MOZILLA_USER_AGENT
MOZILLA_USER_AGENT = "Mozilla/5.0"


ROBOTS = RobotsCache()

url_html={}

url_big_head={}


bad_list1 = ['20010920', 'lefigaro', 'module', 'module', '(', ')', ':80', '..', '404', '.pdf', '.jpg','.mp4','irishtimes.com'
             '.jpeg', '.svg', 'about','fb', 'whatsapp','crimson','JPG','Ideology#mw-head','.flv','.wmv','.tif','.exif','.bmp','.png']


bad_list2 = ['youtube','linkdin', 'categor', 'template', 'facebook', 'google', 'png', 'img','.gov'
         'twitter', 'linkdin','thinkquest','User_talk','user_talk','instagram','twitter','apple.com','.mov','.avi','.webm']

bad_list = bad_list1 + bad_list2



import time
import httplib2
from BeautifulSoup import BeautifulSoup, SoupStrainer
import re
from django.core.validators import URLValidator
from django.core.exceptions import ValidationError
import operator
from reppy.cache import RobotsCache

http = httplib2.Http()
from sys import getsizeof

import requests
from requests import request
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


def push_pq(key,value):
    PQ[key]=value

def pop_pq():
    return(PQ.pop())

########################################################################################
########################################################################################
########################################################################################
########################################################################################



def visible(element):
    if element.parent.name in ['style', 'script', '[document]', 'head', 'title']:
        return False
    elif re.match('<!--.*-->', str(element)):
        return False
    elif re.match('\n', str(element)):
        return False
    return True



########################################################################################
########################################################################################
########################################################################################
########################################################################################



def tf_score(query_list, text_str):
    if any(word in text_str for word in query_list):
        return (1)
    else:
        return (0)

########################################################################################
########################################################################################
########################################################################################
########################################################################################


def extract_only_text(link,soup):

    ################################
    TEXTS = soup.findAll(text=True)
    visible_texts = filter(visible, TEXTS)
    all_txt = ''
    for txt in visible_texts:
        all_txt = all_txt + txt + ' '

    return(all_txt)
    ################################

########################################################################################
########################################################################################
########################################################################################
########################################################################################




def extract_only_all_outlink(url,soup):

    LINKS = soup.findAll('a')

    all_outlink = []
    for l in LINKS:
        if l.has_key('href'):
            try:
                l = str(l['href'])
                if l[0] == '#':
                    continue
                if l[0] == '/':
                    l=extract_only_domain(url)+l

                check = good_link(l)
                if check:


                     if url not in url_outlinks:
                         url_outlinks[url] = []

                     url_outlinks[url].append(l)

                     if l not in url_inlinks:
                         url_inlinks[l] = []

                         url_inlinks[l].append(url)



                     if canonocal(l) in url_visited:

                        print('visited before')
                        continue
                     else:

                       url_visited[canonocal(l)]=True

                       print('to check  ' + str(l))

                       all_outlink.append(l)



            except:
                continue

    return(all_outlink)

########################################################################################
########################################################################################
########################################################################################
########################################################################################


def extract_only_head(soup):
    return(soup.title.string)
########################################################################################
########################################################################################
########################################################################################
########################################################################################



def extract_only_domain(url_adrs):
        domain = 'http://' + url_adrs.split('//')[1].split('/')[0]
        return (domain)


########################################################################################
########################################################################################
########################################################################################
########################################################################################


def good_link(link):  # preliinary check 1)  if the has bad characters  2) check robot 3)check_visited


    if link[1] == '/':
        return (False)
    # if link.count('#')>3:
    #     return(False)

    if (link == 'javascript:;'):
        print('contain javascript')
        return (False)

    if any(word in link for word in bad_list):
        return (False)
    # if not check_robot(link):
    #     return (False)

    if ('http://' in link):
        return (True)


########################################################################################
########################################################################################
########################################################################################
########################################################################################




def canonocal(url):
    url=url.lower()
    url=url.split('#')[0]
    if 'http://' in url:
        second_half=url.split('http://')[1].replace('//','/')
        url='http://'+second_half
    return(url)


########################################################################################
########################################################################################
########################################################################################
########################################################################################



########################################################################################
########################################################################################
########################################################################################
########################################################################################
import urllib
def parse_initial_links(Root_links):

    global url_big_head
    for link in Root_links:
        #link=canonocal(link)
        print(link)
        # status, response = http.request(link)

        response2 = request('GET',link,timeout=10)
        response=response2.content
        soup = BeautifulSoup(response)

        txt = extract_only_text(link, soup)
        url_txt[link] = txt

        url_wave_number[link]=0

        url_canonical[link]=canonocal(link)

        url_head[link] = soup.title.string

        url_all_outlinks[link] = extract_only_all_outlink(link, soup)

        url_inlinks[link] = ''

        url_score[link] = 999999
        url_domain[link] = extract_only_domain(link)
        url_html[link] = unicode(str(response2.content), errors='ignore').encode("utf-8")
        url_big_head[link] = unicode(str(response2.headers), errors='ignore').encode("utf-8")

        url_visited[link]=True
        canonical_url_visited[url_canonical[link]]=True




        print('push to Q' + link)
        PQ[link] = url_wave_number[link]+1/1+len(url_inlinks)



########################################################################################
########################################################################################
########################################################################################
########################################################################################
import urllib
def Mohsen_relevent_outlinks(PQ_link):
    global url_big_head
    global count
    #PQ_link has already the followings:
    #1) url_text[PQ_link] 2) url_wave[PQ_link] 3) url_canonical[PQ_link] 4)url_head[PQ_link]
    #5) url_all_outlink[PQ_link]   6)url_inlink[PQ_link] 7)url_domain[PQ_link] 8)url_score[PQ_link]
    #9

    print('parse the rest')
    all_out_links = url_all_outlinks[PQ_link]
    #print(all_out_links)
    for link in all_out_links:
        a = 0
        b = 0
        c = 0

        path = '/Users/mohsennabian/Infomation_Retrieval_5rdtrial' + '/big_head_' + str(index) + '.txt'

        try:
            print ('robot check')
            if not ROBOTS.allowed(link, MOZILLA_USER_AGENT):
                continue

            if '.wikipedia.' in link and 'en' not in link:
                continue
            print(link)
            print 'longg..........'
            status, response = http.request(link)
            tt=time.time()
            print(tt)
            if extract_only_domain(link) in domain_time_visited:

                if (tt-domain_time_visited[extract_only_domain(link)])>1:

                    response = request('GET',link,timeout=10).content
                    tt = time.time()
                    domain_time_visited[extract_only_domain(link)]=tt
                else :
                    time.sleep(1-tt+domain_time_visited[url_domain[link]])
                    response = request('GET', link, timeout=10).content
                    tt = time.time()
                    domain_time_visited[extract_only_domain(link)] = tt

            else:
                response = request('GET', link, timeout=10).content
                tt = time.time()
                domain_time_visited[extract_only_domain(link)] = tt


            # response2 = request('GET', link, timeout=10)
            # response=response2.content
            print 'fast....'

            soup = BeautifulSoup(response)


            print('check lang')
            LL = (soup.findAll('html'))
            for l in LL:
                if l.has_key('lang'):
                    l = str(l['lang'])
                    if ('en' not in  l):
                        print('not eng')
                        continue


            txt=extract_only_text(link,soup)
        except:
            print('kharab ast soup')
            continue


        if len(url_inlinks[link]) > 5:
            c=1
            print('popular')

        # if any(word in link for word in query_list):
        #     b=1
        #     print('nice link')
        # if  tf_score('404', txt)==1:
        #     print('ghasem')
        #     continue
        if c==0:
            if b==0:
                a = tf_score(query_lower, txt)
                print('good word found')
                print(a)
                if a==0:
                    print('not relevent:' + str(link))
                    try:
                        del url_inlinks[link]
                        url_outlinks[PQ_link].remove(link)
                        continue
                    except:
                        continue

        try:
            a1=soup.title.string
            a2=txt
            a3=url_wave_number[PQ_link]+1
            a4=canonocal(link)
            a5=extract_only_all_outlink(link, soup)
            a6=2*a+ 15*a3
            a7=extract_only_domain(link)
            a8=unicode(str(response2.content), errors='ignore').encode("utf-8")
            a9=unicode(str(response2.headers), errors='ignore').encode("utf-8")

        except:
            print('pushing problem')
            continue


        url_head[link] = a1
        url_txt[link]=a2
        url_wave_number[link]=a3
        url_canonical[link]=a4

        url_all_outlinks[link]=a5
        # url_inlinks[link]=PQ_link
        url_score[link]=a6
        url_domain[link]=a7
        url_html[link] = a8
        url_big_head[link] = a9
        print(url_big_head[link])
        print('match ' + str(a)+str(b)+str(c))
        print('link selected')
        print('push to Q ' +'  '+ link)
        print('len Q=   '+str(len(PQ)))

        print('len corpus=   '+str(len(final_corpus)))
        print('url_txt-size =  '+str(len(url_txt)))
        print('url_inlink_size =  '+str(len(url_inlinks)))
        print('memory for inlink = '+str(getsizeof(url_inlinks)))
        print('url_outlinks_size =  '+str(len(url_outlinks)))
        print('wave = ' +str(url_wave_number[link]))
        PQ[link]=url_wave_number[link]+1/(1+len(url_inlinks))

        # except:
        #     print('pushing problem')
        #     continue

########################################################################################
########################################################################################
########################################################################################
########################################################################################



index=0
query_list = [ 'TERRORISM', 'terror', 'bomb', 'Woolwich', 'murder',  'bomb', 'terro','terror', 'al-Qaeda', 'hostage', 'siege', 'extremist', 'Chechen',
              'wahabi', 'explod','massacres','isis','gun violence','shoot','bloodshed','11 september']
query_list2 = ['suicide', 'assasinat', 'tavistock', 'silique', 'Bin Laden', 'Breivik', 'Woolwich','kidnap'
                'extremism', 'refugee', 'suicid', 'middle east'
               , 'explosion','murder']
query_list4 = query_list + query_list2

tight_query_list=['terrorism','terrorist','assasinat','bombing','al-Qaeda','massacres','gun violence','jihadi','suicide attack','taliban','Bin Laden','islamic extremist','explosives','murder']
query_list = tight_query_list


for word in query_list:
    query_lower.append(word.lower())



# link00 = 'https://www.theguardian.com/world/2016/feb/25/how-changing-media-changing-terrorism'

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


parse_initial_links(init_links)



print(len(PQ))

i = 0




while ((len(final_corpus) + len(PQ)) < max_link):
    summ=len(final_corpus) + len(PQ)

    if summ>10000:
        query_lower=query_list4


    print('sum =   '+ str(summ))

    i = i + 1
    print('Que= ' + str(len(PQ)))
    print('final= ' + str(len(final_corpus)))



    if (len(url_txt) > (100)):

        print('save TXT file')


        path = '/Users/mohsennabian/Infomation_Retrieval_5rdtrial' + '/txt_' + str(index) + '.txt'
        save_dictionary(path, url_txt)
        url_txt={}

        path = '/Users/mohsennabian/Infomation_Retrieval_5rdtrial' + '/outlinks_' + str(index) + '.txt'
        save_dictionary(path, url_outlinks)
        url_outlinks={}

        path = '/Users/mohsennabian/Infomation_Retrieval_5rdtrial' + '/head_' + str(index) + '.txt'
        save_dictionary(path, url_head)
        url_head={}


        path = '/Users/mohsennabian/Infomation_Retrieval_5rdtrial' + '/canonical_' + str(index) + '.txt'
        save_dictionary(path, url_canonical)
        url_canonical={}

        path = '/Users/mohsennabian/Infomation_Retrieval_5rdtrial' + '/html_' + str(index) + '.txt'
        save_dictionary(path, url_html)
        url_html = {}
        print('ta inja OK ast')


        path = '/Users/mohsennabian/Infomation_Retrieval_5rdtrial' + '/big_head_' + str(index) + '.txt'
        save_dictionary(path, url_big_head)
        url_big_head = {}


        index = index + 1





    new_link = PQ.pop()
    print('go to corpus    '+ new_link)
    final_corpus[new_link] = url_wave_number[new_link]
    Mohsen_relevent_outlinks(new_link)



hh=max_link+1-len(final_corpus)
for i in range(0, hh):
    print('remaining in the que')
    new_link = PQ.pop()
    final_corpus[new_link] = url_wave_number[new_link]



mac = 1
windows = 0

try:

    path = '/Users/mohsennabian/Infomation_Retrieval_5rdtrial' + '/txt_' + str(index) + '.txt'
    save_dictionary(path, url_txt)
    url_txt = {}

    path_outlinks = '/Users/mohsennabian/Infomation_Retrieval_5rdtrial/outlinks'+ str(index) +'.txt'
    save_dictionary(path_outlinks, url_outlinks)
    url_outlinks={}

    path_inlink = '/Users/mohsennabian/Infomation_Retrieval_5rdtrial/inlinks.txt'
    save_dictionary(path_inlink, url_inlinks)
    url_inlinks={}

    path_final_corpus = '/Users/mohsennabian/Infomation_Retrieval_5rdtrial/final_links.txt'
    save_dictionary(path_final_corpus, final_corpus)
    final_corpus={}

    path_canonical= '/Users/mohsennabian/Infomation_Retrieval_5rdtrial/canonical'+ str(index) +'.txt'
    save_dictionary(path_canonical,url_canonical)
    url_canonical={}

    path_head='/Users/mohsennabian/Infomation_Retrieval_5rdtrial/head'+ str(index) +'.txt'
    save_dictionary(path_head, url_head)
    url_head={}

    path = '/Users/mohsennabian/Infomation_Retrieval_5rdtrial' + '/html_' + str(index) + '.txt'
    save_dictionary(path, url_html)
    url_html = {}
    print('ta inja kar kard')
    path = '/Users/mohsennabian/Infomation_Retrieval_5rdtrial' + '/big_head_' + str(index) + '.txt'
    save_dictionary(path, url_big_head)
    url_big_head = {}



except:

    folder = "C:/Users/nabian.m/Desktop/Infomation_Retrieval_HW3"
    path = folder + '/txt_' + str(index) + '.txt'
    save_dictionary(path, url_txt)
    url_txt = {}

    path_outlink = folder + '/outlinks.txt'
    save_dictionary(path_outlink, url_outlinks)

    path_inlink = folder + '/inlinks.txt'
    save_dictionary(path_inlink, url_inlinks)

    path_final_links = folder + '/dfinal_links.txt'
    save_dictionary(path_final_links, final_corpus)

print('length final_links  ' + str(len(final_corpus)))
print('length out_links  ' + str(len(url_outlinks)))
print('length in_links  ' + str(len(url_inlinks)))



########################################################################################
########################################################################################
########################################################################################
########################################################################################





#
#
# # def scoring(link):
# #     score = url_inlinks[link]*1/url_wave_number[link]
# #     url_score.keys[link]=score
# #     print(url_score.keys(), url_score.values())
# #
#
#
#
#
#
#
#
#
#
#
#
# def url_validity_check():
#  pass
#
#
#
#
#
#
#
#
#
#
#
# def mohsen_html_parse(url_adrs):      #input the new_address, parents_url and parents_wave number
#
#
#
#
#     # print(status)
#     ###################################################
#     # soup_uploaded = url_soup[url_adrs]
#     # url_soup[url_adrs]=''
#     ###################################################
#
#     ########################################  extract domain
#
#     domain=url_domain[url_adrs]
#
#
#
#
#     # url_domain[url_adrs]=''
#     ######################################## finding links for url_adrs
#
#
#     # LINKS = soup_uploaded.findAll('a')
#
#     # if len(LINKS)>10:
#     #     LINKS=LINKS[0:10]
#     LINKS=url_outlinks[url_adrs]
#
#     # LINKS=url_all_links[url_adrs]
#     # url_all_links[url_adrs]=[]
#     links_list_cleaned = []
#
#     for link in LINKS:
#
#         try:
#             status, response = http.request(link)
#         except:
#
#             print('invalid URL mohsen')
#             return []
#         print(link)
#
#         soup = BeautifulSoup(response)
#
#
#
#         try:
#             TEXTS = soup.findAll(text=True)
#             visible_texts = filter(visible, TEXTS)
#         except:
#             continue
#
#
#
#         all_txt = ''
#         for txt in visible_texts:
#             all_txt = all_txt + txt + ' '
#         all_txt = all_txt.lower()
#
#         a = tf_score(query_lower, all_txt)
#
#         # print(a)
#         # b=tf_score(query_list,link_ancher)
#         b = 50
#         relevence_score = a * 10 + b
#         if (relevence_score < 70):
#             print('link_rejected')
#             print(relevence_score)
#             continue
#         else:
#             print(relevence_score)
#
#             LINKS = soup.findAll('a')
#             h = []
#             for link in LINKS:
#                 if link.has_key('href'):
#                     try:
#                         link = str(link['href'])
#                         h.append(link)
#                     except:
#                         continue
#
#
#
#
#
#
#
#
#         if link in visited :
#            print('repeated omid jan')
#            continue
#
#         visited[link]=''
#
#
#         try:
#             if (link[0] == '#'):
#                 continue
#         except:
#             continue
#
#         if (link == 'javascript:;'):
#             continue
#         # if link[1]=='/' : continue
#         if (link[0] == '/'):
#             # link = domain + link
#             # if (link == url_adrs):  # not reference to itself
#             continue
#             # links_list_cleaned.append(canonocal(link))
#             # anchor[link]=ancher_str
#
#         if (link == url_adrs):  # not reference to itself
#             continue
#
#         if ('http://' in link):
#             if good_link(link) :
#
#
#             # anchor[link] = ancher_str
#
#
#     # links_list_cleaned = list(set(links_list_cleaned))  # Find Unique Links
#     #url_outlinks[url_adrs] = links_list_cleaned
#     ########################################
#
#     # out_urls=links_list_cleaned
#
#     # for link in out_urls:
#
#                 if link in list(PQ.keys()):
#                     print('repeated omidi')
#                     continue
#                 if link in final_link:
#                     print('repeated omid jigari')
#                     continue
#
#
#
#
#                 #Robot check:
#
#                 # try:
#                 #     allow=check_robot(link)
#                 # except:
#                 #     continue
#                 #
#                 # if not (allow):
#                 #     return []
#
#
#
#
#
#                 #
#                 # link_ancher = anchor[url_adrs]
#                 ##################################################################
#
#
#
#
#                     url_all_links[link]=h
#
#
#
#
#                     url_txt[link] = all_txt
#                     url_wave_number[link] = wave_number + 1
#                     url_domain[link] = extract_domain(url_adrs)
#                     url_score[link] = 700 * a + 10000 * url_wave_number[link]
#                     if link not in url_inlinks.keys():
#                         url_inlinks[link]=[]
#                     url_inlinks[link].append(url_adrs)
#                     if url_adrs not in url_outlinks.keys():
#                         url_outlinks[url_adrs] = []
#                     url_outlinks[url_adrs].append(link)
#                     #push to priority Quequ?
#                     PQ[link]=url_score[link]
#                     if (len(final_link)+len(PQ)) > max_link:
#                         break
#
#
#     ##################################################################
#
#
#
#
#             ##################################################################
#             print('accepted and parsed')
#             # parent_url=[]
#
#
#
# ########################################################################################
# ########################################################################################
# ########################################################################################
# ########################################################################################
#
#
#
#
#
#
#
# # def scoring(current_links):
# #     link_dict={}
# #     score_link = {}
# #     for link in current_links:
# #         inlink = len(url_inlinks[a])
# #         wave = url_wave_number[link]
# #         txt_relev = tf_score(query_list,hashtag[link])
# #         score_link[link]=txt_relev*10+inlink*1
# #         sorted_link = sorted(score_link.items(), key=operator.itemgetter(1))
# #     pass
#
#
# # def running():
# #     while (len(all_links<20000)):
# #         hhh=current_links
# #         current_links=[]
# #         for link in hhh:
# #             mohsen_html_parse(link, parent_url, parent_wave)
# #
#
#
#
#
#
# # print(PQ)
#
#
#
#     print('ghasem')
#     final_link[new_link]=url_wave_number[new_link]
#
#     print('one link recorded')
#
#     print(new_link)
#     mohsen_html_parse(new_link, url_wave_number[new_link])
#
#     if len(url_txt)>(max_link/10):
#
#         try:
#             path='/Users/mohsennabian/Infomation_Retrieval_HW3'+'/txt_'+' '+str(index)+'.txt'
#             save_dictionary(path, url_txt)
#
#         except:
#             folder = "C:/Users/nabian.m/Desktop/Infomation_Retrieval_HW3"
#             path = folder + '/txt_' + ' ' + str(index) + '.txt'
#             save_dictionary(path, url_txt)
#
#         index = index + 1
#         url_txt={}
#
#
# l=len(PQ)
# for i in range(0,l):
#     print('remaining in the que')
#     new_link = PQ.pop()
#     final_link[new_link]=url_wave_number[new_link]
#
#
#
#
#
# mac=1
# windows=0
#
# try:
#
#
#     path = '/Users/mohsennabian/Infomation_Retrieval_HW3' + '/txt_' + str(index) + '.txt'
#     save_dictionary(path, url_txt)
#     url_txt = {}
#
#     path_outlink='/Users/mohsennabian/Infomation_Retrieval_HW3/outlinks.txt'
#     save_dictionary(path_outlink, url_outlinks)
#
#     path_inlink='/Users/mohsennabian/Infomation_Retrieval_HW3/inlinks.txt'
#     save_dictionary(path_inlink, url_inlinks)
#
#
#     path_final_links='/Users/mohsennabian/Infomation_Retrieval_HW3/final_links.txt'
#     save_dictionary(path_final_links, final_link)
#
# except:
#
#     folder = "C:/Users/nabian.m/Desktop/Infomation_Retrieval_HW3"
#     path = folder+ '/txt_' + str(index) + '.txt'
#     save_dictionary(path, url_txt)
#     url_txt = {}
#
#
#
#     path_outlink = folder+'/outlinks.txt'
#     save_dictionary(path_outlink, url_outlinks)
#
#     path_inlink = folder+'/inlinks.txt'
#     save_dictionary(path_inlink, url_inlinks)
#
#     path_final_links = folder+'/dfinal_links.txt'
#     save_dictionary(path_final_links, final_link)
#
#
#
# print('length final_links'+str(len(final_link)))
# print('length out_links'+str(len(url_outlinks)))
# print('length in_links'+str(len(url_inlinks)))
#
#
# # print(check_robot(test))
# #print(url_txt.keys(), url_txt.values())
#
# #print(url_domain.keys(), url_domain.values())
# #print(url_wave_number.keys(), url_wave_number.values())
# #print(url_inlinks.keys(), url_inlinks.values())
#
#
#
# # print(url_txt.keys(), url_txt.values())
#
# # verify_link('https://en.wikipedia.org/wiki/Renewable_energy')
# #
#
# #
# #
# # html = urllib.urlopen('http://www.nytimes.com/2009/12/21/us/21storm.html').read()
# # soup = BeautifulSoup(html, 'html.parser')
# # texts = soup.findAll(text=True)
# #
# # def visible(element):
# #     if element.parent.name in ['style', 'script', '[document]', 'head', 'title']:
# #         return False
# #     elif re.match('<!--.*-->', str(element)):
# #         return False
# #     return True
# #
# # visible_texts = filter(visible, texts)
#
#
#
# #
# #
# # import re
# # import urllib
# # from bs4 import BeautifulSoup
# #
# # html = urllib.urlopen('http://bgr.com/2014/10/15/google-android-5-0-lollipop-release/')
# # soup = BeautifulSoup(html)
# # data = soup.findAll(text=True)
# #
# #
# # def visible(element):
# #     if element.parent.name in ['style', 'script', '[document]', 'head', 'title']:
# #         return False
# #     elif re.match('<!--.*-->', str(element.encode('utf-8'))):
# #         return False
# #     return True
# #
# #
# # result = filter(visible, data)
# #
# # print visible_texts
