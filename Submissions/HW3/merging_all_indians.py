from elasticsearch import Elasticsearch
es = Elasticsearch()




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


def merge_two_dicts(x, y):
    '''Given two dicts, merge them into a new dict as a shallow copy.'''
    z = x.copy()
    z.update(y)
    return z


def save_dictionary(path,data):
    print('saving catalog...')
    #open('u.item', encoding="utf-8")
    import json
    with open(path,'w') as outfile:
        json.dump(data, fp=outfile)
    # save to file:
    print(' catalog saved')

def extract_all_texts():

    text_files_list=['txt_ 1','txt_ 2','txt_ 3','txt_ 4','txt_ 5','txt_ 6','txt_ 7','txt_ 8','txt_ 9','txt_ 10']
    all_txt_dict={}
    for text_file in text_files_list:
        path='/Users/mohsennabian/Infomation_Retrieval_HW3/'+text_file+'.txt'
        all_txt_dict = merge_two_dicts(all_txt_dict,read_dictionary(path))



corpus_path='/Users/mohsennabian/Infomation_Retrieval_HW3/final_links.txt'

corpus=read_dictionary(corpus_path)

inlink_path='/Users/mohsennabian/Infomation_Retrieval_HW3/inlinks.txt'
INLINKS_DICT=read_dictionary(inlink_path)

print(len(corpus))
print(len(INLINKS_DICT))

inlink_keys=INLINKS_DICT.keys()

with open("/Users/mohsennabian/Infomation_Retrieval_HW3/inlinks_with_tabs.txt","w") as fp:
    for url in INLINKS_DICT:
        fp.write(url + '    '+'    '.join('{}'.format(val) for val in INLINKS_DICT[url]))
        fp.write("\n")




