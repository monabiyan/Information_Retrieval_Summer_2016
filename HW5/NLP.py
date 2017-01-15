def part1():


    ###############   Part 1  #######################
    import nltk
    posts = nltk.corpus.nps_chat.xml_posts()[:1000]     #extraction of data
    def dialogue_act_features(post):                    #this function provides the features based on specific words
         features = {}
         for word in nltk.word_tokenize(post):
             features['contains({})'.format(word.lower())] = True
         return features


    featuresets = [(dialogue_act_features(post.text), post.get('class')) for post in posts]  #make the features

    size = int(len(featuresets) * 0.1)
    train_set, test_set = featuresets[size:], featuresets[:size]           # Test and Train Data
    print('training......')
    classifier_naieve = nltk.NaiveBayesClassifier.train(train_set)          #training naive base
    print('training dec..')
    classifier_decision_tree = nltk.DecisionTreeClassifier.train(train_set)  #training decision tree
    print('training nltk..')
    classifier_maxent=nltk.MaxentClassifier.train(train_set)                #training max_entropy

    print('testing......')
    import time

    start_time = time.time()
    print("accuracy for naieve base"+str(nltk.classify.accuracy(classifier_naieve, test_set)))   #provide accuracy
    print("--- %s seconds for naieve base --- " % (time.time() - start_time))   #calculate time

    start_time = time.time()
    print("accuracy for decision tree "+str(nltk.classify.accuracy(classifier_decision_tree, test_set)))  #provide accuracy
    print("--- %s seconds for decision tree ---" % (time.time() - start_time))  #calculate time


    start_time = time.time()
    print("accuracy for max-entropy "+str(nltk.classify.accuracy(classifier_maxent, test_set)))  #provide accuracy
    print("--- %s seconds for max entropy ---" % (time.time() - start_time))    #calculate time

    # After running I got :
    #accuracy:   naive_base=0.5   decision_tree=0.75      max_entropy=0.68
    #time:      naive_base=0.0129020214081 seconds       decision_tree=0.00261306762695 seconds      max_entropy=0.00981712341309 seconds



def part2():
    ###############   Part 2  #######################
    import nltk
    posts = nltk.corpus.nps_chat.xml_posts()[:1000]

    def dialogue_act_features1(post):     #this function provides the features based on specific sentences
        features = {}
        for word in nltk.sent_tokenize(post):
            features['contains({})'.format(word.lower())] = True
        return features


    def dialogue_act_features2(post):    #this function provides the features based on specific punctuations and word
        features = {}
        for word in nltk.wordpunct_tokenize(post):
            features['contains({})'.format(word.lower())] = True
        return features

    featuresets = [(dialogue_act_features1(post.text), post.get('class')) for post in posts]
    size = int(len(featuresets) * 0.1)
    train_set, test_set = featuresets[size:], featuresets[:size]


    print('training  naieve......')
    classifier_naieve = nltk.NaiveBayesClassifier.train(train_set)

    print('testing......')

    print('accuracy for sentence features  =  '+str(nltk.classify.accuracy(classifier_naieve, test_set)))



    featuresets = [(dialogue_act_features2(post.text), post.get('class')) for post in posts]
    size = int(len(featuresets) * 0.1)
    train_set, test_set = featuresets[size:], featuresets[:size]

    print('training naieve......')
    classifier_naieve = nltk.NaiveBayesClassifier.train(train_set)

    print('testing......')

    print('accuracy  for punctiation features =  ' + str(nltk.classify.accuracy(classifier_naieve, test_set)))


    # after running :

        #accuracy of sentence_tokenizer feature is : 0.65
        #accuracy of punctuation_tokenizer feature is : 0.46
        # for this small training dataset sentence feature works than punctuation
        #However, with higher amount of training data I have checked that punctuation based feature works better.




part1()
part2()



# After running part 1  I got the followings :
# accuracy:   naive_base=0.5   decision_tree=0.75      max_entropy=0.68
# time:      naive_base=0.0129020214081 seconds       decision_tree=0.00261306762695 seconds      max_entropy=0.00981712341309 seconds


# after running part 2 :

        #accuracy of sentence_tokenizer feature is : 0.65
        #accuracy of punctuation_tokenizer feature is : 0.46
        # for this small training dataset sentence feature works than punctuation
        #However, with higher amount of training data I have checked that punctuation based feature works better.




# comparing part 1 and part 2 with naieve base classifier, accuarcy for sentence is the highest(0.65)
    # then accuracy of words is higher(0.5) and lastly the puctuation accuracy is (0.46)

#Although these numbers are not scientific at all since we only have 1000 training data set. No generalization


