import math
import multiprocessing

########################################################################################
########################################################################################
########################################################################################
########################################################################################
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
def save_dictionary(path,data):      # a utility function to save a dictionary in hard drive
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
def read_dictionary(path):      # a utility function to load a dictionary from hard drive
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
def extract_and_save_data():   #This function will read the raw data and will clean them , shuffle them and
                                #seprate data from training and Test data, Finally will save it

    X = []
    Y = []
    file_names = []
    root_path = '/Users/mohsennabian/Datasets/MHEALTHDATASET/mHealth_subject'
    for i in range(1, 11):
        full_path = root_path + str(i) + '.log'
        file_names.append(full_path)
    k = 0
    for i in range(0, 10):
        f = open(file_names[i], 'r')
        whole = f.read()
        sentences = whole.split('\n')
        from random import shuffle
        shuffle(sentences)

        for sentence in sentences:
            k = k + 1
            print(k)
            if (sentence == ' ') | (sentence == ''): continue
            sensors = sentence.split('	')
            sensors = [float(x) for x in sensors]
            if int(sensors[23])==0: continue
            Y.append(int(sensors[23]))
            del sensors[23]
            # sensors.insert(0,1)
            X.append(sensors)


    import numpy as np
    X=np.array(X)
    Y=np.array(Y)
    X= (X - X.min(0)) / X.ptp(0)
    N=len(X)
    X=np.c_[np.ones(N),X]

    X=X.tolist()
    Y=Y.tolist()

    import random
    l = len(X)
    d = int(l * 0.2)
    test_index = random.sample(range(0, l), d)
    train_index = list(set(range(0, l)) - set(test_index))
    X_train, Y_train, X_test, Y_test = [], [], [], []
    for i in train_index:
        X_train.append(X[i])
        Y_train.append(Y[i])
    for i in test_index:
        X_test.append(X[i])
        Y_test.append(Y[i])


    s={}
    s['X_train']=X_train
    s['X_test'] = X_test
    s['Y_train']=Y_train
    s['Y_test']=Y_test
    save_dictionary('/Users/mohsennabian/Datasets/MHEALTHDATASET/my_python_AI_dicts/data_dict.txt',s)

def load_data():    #Here we can load the cleaned data
    import numpy as np
    path='/Users/mohsennabian/Datasets/MHEALTHDATASET/my_python_AI_dicts/data_dict.txt'
    a=read_dictionary(path)
    X_train=a['X_train']
    Y_train=a['Y_train']
    X_test=a['X_test']
    Y_test=a['Y_test']
    X_train = np.array(X_train)
    X_test = np.array(X_test)
    Y_train = np.array(Y_train)
    Y_test = np.array(Y_test)
    return(X_train,Y_train,X_test,Y_test)

########################################################################################
########################################################################################
########################################################################################
########################################################################################
def Converged(Teta_new,Teta_old):   #Will check whether the model converged or not
    import numpy as np
    Teta_old=np.array(Teta_old)
    Teta_new=np.array(Teta_new)
    n=len(Teta_new)
    diff=0
    hh=Teta_new - Teta_old
    hh=np.absolute(hh)
    diff=np.sum(hh)
    diff=diff/float(n)
    print('delta = '+str(diff))
    if diff<0.01 :
        return(True)
    else:
        return(False)



def hyp(Teta,x):  #Sigmoid function
 import numpy as np
 import math
 z=np.dot(Teta,x)
 # print(Teta,z)
 y=1/(1+math.exp(-z))
 return(y)


def log_reg_train(X,Y,alpha):   #This is  logistic regression implementation for tow classes
    import numpy as np
    n=len(X[0])
    m=len(X)
    #
    Teta_new=[1]*n
    Teta_old=[0]*n
    Teta_new=np.array(Teta_new)
    Teta_old=np.array(Teta_old)

    a=0
    while not Converged(Teta_new,Teta_old):
        a=a+1
        Teta_old=list(Teta_new)
        for i in range(0,m):
            # print('convergence try = '+str(a)+'on data point number = '+ str(i))

            Teta_new_new=np.array([0])
            Teta_new_new=Teta_new+alpha*(Y[i]-hyp(Teta_new,X[i]))*X[i]
            Teta_new=list(Teta_new_new)

    # print(Teta_new)
    return(Teta_new)

def train_multi_Y(X_train,Y_train,alpha):  #This is  logistic regression implementation for multi-level classes
    Tetas=[]
    labels=list(set(Y_train))

    for i in range(1,len(labels)+1):  #12
        new_Y = []
        for j in range(0,len(Y_train)):  #100
            if int(Y_train[j])==i:
                new_Y.append(1)
            else:
                new_Y.append(0)

        Teta=log_reg_train(X_train,new_Y,alpha)
        Tetas.append(Teta)
        print ('Teta ='+str(Teta))
        print('--------------------------------------------------------------------')
        # print('Teta Matrix Added for label number = '+str(i))

    return(Tetas)

def predict(Tetas,X_test): # (One-vs_All function) This function will predict as many times as unique labels and will return the maximum probability
    Y_predicted=[]
    for i in range(0,len(X_test)):
        x=X_test[i]
        probs={}
        for j in range(0,len(Tetas)):
            teta=Tetas[j]
            probs[j+1]=hyp(teta,x)
        # print(probs)
        Y_predicted.append(max(probs, key=probs.get))
    return(Y_predicted)


def Mohsen_Logistic_regression(X_train, Y_train, X_test, Y_test): #This is the main function for Logistic regression O(n^2) time  O(n) space
    Tetas=train_multi_Y(X_train,Y_train,1)
    model={}
    model['Tetas']=Tetas
    save_dictionary('/Users/mohsennabian/Datasets/MHEALTHDATASET/my_python_AI_dicts/model_2k_001_dict.txt',model)
    model = read_dictionary('/Users/mohsennabian/Datasets/MHEALTHDATASET/my_python_AI_dicts/model_full_001_dict.txt')
    Tetas = model['Tetas']
    import numpy as np
    print('Tetas = ' + str(Tetas))
    Y_pred = predict(Tetas, X_test)

    from sklearn.metrics import accuracy_score
    print('accuracy score.....')
    print accuracy_score(Y_test, Y_pred)
########################################################################################
########################################################################################
########################################################################################
########################################################################################

def knn_classifier(X_train, Y_train, X_test_one_point, Y_test_one_point, k):  #This is a subfunction for KNN
                                                        #This will returns the most voted label of K-NEAREST-NEIGHBORS
    import math
    import numpy as np

    X_train = np.array(X_train)
    Y_train = np.array(Y_train)
    X_test_one_point = np.array(X_test_one_point)
    Y_test_one_point = np.array(Y_test_one_point)

    l = len(X_test_one_point)

    m = len(X_train)

    d = 0

    dist_list = []

    for i in range(0, m):
        d = math.sqrt(sum((X_test_one_point - X_train[i]) ** 2))
        dist_list.append(-d)
    dist_list=np.array(dist_list)
    indexes = np.argpartition(dist_list, -k)[-k:]
    neighburs = []
    for i in indexes:
        neighburs.append(Y_train[i])
    from statistics import mode
    return (mode(neighburs))


def Mohsen_knn(X_train, Y_train, X_test, Y_test, k):    #The main function for KNN  O(n^2) Time
    m=len(Y_test)
    Y_pred=[]
    for i in range(0,m):
        print(i)
        Y_pred.append(knn_classifier(X_train, Y_train,X_test[i],  Y_test[i], k))

    from sklearn.metrics import accuracy_score
    print(Y_test)
    print(Y_pred)
    print accuracy_score( Y_test, Y_pred)
########################################################################################
########################################################################################
########################################################################################
########################################################################################

def build_in_ML_logreg(X_train,Y_train,X_test,Y_test):   #Logistic Regression
    from sklearn import linear_model
    logreg = linear_model.LogisticRegression()
    print('training...')
    logreg.fit(X_train,Y_train)
    print('testing......')
    Y_predict=logreg.predict(X_test)
    from sklearn.metrics import accuracy_score
    print('accuracy score  .....')
    print accuracy_score(Y_test, Y_predict)

def build_in_ML_neural_network(X_train,Y_train,X_test,Y_test):  #Neural Network
    from sklearn.neural_network import BernoulliRBM
    from sklearn import linear_model
    from sklearn.pipeline import Pipeline
    logistic = linear_model.LogisticRegression()
    rbm = BernoulliRBM()
    clf = Pipeline(steps=[('rbm', rbm), ('clf', logistic)])
    print('training...')
    clf.fit(X_train, Y_train)
    print('testing......')
    Y_predict = clf.predict(X_test)
    from sklearn.metrics import accuracy_score
    print('accuracy score  .....')
    print accuracy_score(Y_test, Y_predict)

def build_in_ML_knn(X_train,Y_train,X_test,Y_test):    #KNN
    from sklearn.neighbors import KNeighborsClassifier
    neigh = KNeighborsClassifier()
    print('training...')
    neigh.fit(X_train,Y_train)
    print('testing......')
    Y_predict=neigh.predict(X_test)
    from sklearn.metrics import accuracy_score
    print('accuracy score  .....')
    print accuracy_score(Y_test, Y_predict)



def build_in_ML_svm(X_train,Y_train,X_test,Y_test):        #SVM
    from sklearn import svm
    clf = svm.SVC()
    print('training...')
    clf.fit(X_train,Y_train)
    print('testing......')
    Y_predict=clf.predict(X_test)
    from sklearn.metrics import accuracy_score
    print('accuracy score  .....')
    print accuracy_score(Y_test, Y_predict)



def build_in_ML_randomforest(X_train,Y_train,X_test,Y_test):  #RAndom Forest
    from sklearn.ensemble import RandomForestClassifier
    rf = RandomForestClassifier()
    print('training...')
    rf.fit(X_train,Y_train)
    print('testing......')
    Y_predict=rf.predict(X_test)
    from sklearn.metrics import accuracy_score
    print('accuracy score  .....')
    print accuracy_score(Y_test, Y_predict)

def build_in_ML_naieveBase(X_train,Y_train,X_test,Y_test):  #Naieve Base
    from sklearn.naive_bayes import GaussianNB
    gnb = GaussianNB()

    print('training...')
    gnb.fit(X_train,Y_train)
    print('testing......')
    Y_predict=gnb.predict(X_test)
    from sklearn.metrics import accuracy_score
    print('accuracy score  .....')
    print accuracy_score(Y_test, Y_predict)

def build_in_ML_decisionTree(X_train,Y_train,X_test,Y_test):  #Decision Tree
    from sklearn.tree import DecisionTreeClassifier
    clf = DecisionTreeClassifier()

    print('training...')
    clf.fit(X_train,Y_train)
    print('testing......')
    Y_predict=clf.predict(X_test)
    from sklearn.metrics import accuracy_score
    print('accuracy score .....')
    print accuracy_score(Y_test, Y_predict)

########################################################################################
########################################################################################
def data_distribution(Y_train):         #Data Visualization
    n=len(list(set(Y_train)))
    print(n)
    s=[0]*n
    for label in Y_train:
        print(label)
        label=int(label)
        s[label-1]=s[label-1]+1
    print ('here is the distribution =  '+ str(s))
########################################################################################
########################################################################################
########################################################################################
########################################################################################


extract_and_save_data()
X_train,Y_train,X_test,Y_test=load_data()

print("number of training data =  "+str(len(Y_train)))
print("number  of test data    =  "+str(len(Y_test)))

import time
start_time = time.time()

Mohsen_Logistic_regression(X_train, Y_train, X_test, Y_test)
# Mohsen_knn (X_train, Y_train, X_test[0:100], Y_test[0:100],5)

# build_in_ML_logreg(X_train,Y_train,X_test,Y_test)
# build_in_ML_knn(X_train,Y_train,X_test,Y_test)
# build_in_ML_svm(X_train,Y_train,X_test,Y_test)
# build_in_ML_randomforest(X_train,Y_train,X_test,Y_test)
# build_in_ML_naieveBase(X_train,Y_train,X_test,Y_test)
# build_in_ML_decisionTree(X_train,Y_train,X_test,Y_test)
# build_in_ML_neural_network(X_train,Y_train,X_test,Y_test)

print("--- %s seconds ---" % (time.time() - start_time))





#################################################
#################################################
#################################################

#Data Information:


# ACTIVITY SET
# The activity set is listed in the following:
# L1: Standing still (1 min)
# L2: Sitting and relaxing (1 min)
# L3: Lying down (1 min)
# L4: Walking (1 min)
# L5: Climbing stairs (1 min)
# L6: Waist bends forward (20x)
# L7: Frontal elevation of arms (20x)
# L8: Knees bending (crouching) (20x)
# L9: Cycling (1 min)
# L10: Jogging (1 min)
# L11: Running (1 min)
# L12: Jump front & back (20x)
# NOTE: In brackets are the number of repetitions (Nx) or the duration of the exercises (min).




# #################################################
# The meaning of each column is detailed next:
# Column 1: acceleration from the chest sensor (X axis)
# Column 2: acceleration from the chest sensor (Y axis)
# Column 3: acceleration from the chest sensor (Z axis)
# Column 4: electrocardiogram signal (lead 1)
# Column 5: electrocardiogram signal (lead 2)
# Column 6: acceleration from the left-ankle sensor (X axis)
# Column 7: acceleration from the left-ankle sensor (Y axis)
# Column 8: acceleration from the left-ankle sensor (Z axis)
# Column 9: gyro from the left-ankle sensor (X axis)
# Column 10: gyro from the left-ankle sensor (Y axis)
# Column 11: gyro from the left-ankle sensor (Z axis)
# Column 13: magnetometer from the left-ankle sensor (X axis)
# Column 13: magnetometer from the left-ankle sensor (Y axis)
# Column 14: magnetometer from the left-ankle sensor (Z axis)
# Column 15: acceleration from the right-lower-arm sensor (X axis)
# Column 16: acceleration from the right-lower-arm sensor (Y axis)
# Column 17: acceleration from the right-lower-arm sensor (Z axis)
# Column 18: gyro from the right-lower-arm sensor (X axis)
# Column 19: gyro from the right-lower-arm sensor (Y axis)
# Column 20: gyro from the right-lower-arm sensor (Z axis)
# Column 21: magnetometer from the right-lower-arm sensor (X axis)
# Column 22: magnetometer from the right-lower-arm sensor (Y axis)
# Column 23: magnetometer from the right-lower-arm sensor (Z axis)
# Column 24: Label (0 for the null class)
#


# http://machinelearningmastery.com/tutorial-to-implement-k-nearest-neighbors-in-python-from-scratch/

