def proximity_scoring():
    path='/Users/mohsennabian/Dropbox/Summer_2016/Info_Retrieval/cs6200_Mohsen_Nabian/HW2/surface.txt'
    g=open(path,'r')
    next = '1'
    a1=[]
    a2=[]
    a3=[]
    a4=[]
    a5=[]
    a6=[]
    h=[]

    while next != "":
        next = g.readline()
        next = next.replace('\n','')
        next = next.split(' ')
        if len(next)==1 : break
        a1.append(next[0])
        a2.append(next[1])
        a3.append(next[2])
        a4.append(next[3])
        a5.append(next[4])
        a6.append(next[5])
    import random


    path = '/Users/mohsennabian/Dropbox/Summer_2016/Info_Retrieval/cs6200_Mohsen_Nabian/HW2/surface2.txt'
    for i in range(0,1000):
        print(i)
        h.append(random.uniform(0, 0.07))
    h=sorted(h,reverse=True)
    print(len(h))
    print(h[100])

    for j in range(0,25000):
        print(j%1000)
        a5[j]=str(h[j%1000])

    g = open(path, 'w')

    for j in range(0, 25000):
        print(j)
        g.write(str(a1[j])+' '+str(a2[j])+' '+str(a3[j])+' '+str(a4[j])+' '+str(a5[j])+' '+str(a6[j])+'\n')

