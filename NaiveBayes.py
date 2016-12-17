import nltk
import csv
import math

# Load list of stop words
stopwords = nltk.corpus.stopwords.words('english')

#Computed dictionaries for each class/candidate
trump_neg_dict = {}
trump_pos_dict = {}
clinton_neg_dict = {}
clinton_pos_dict = {}

#Build Trump negative sentiment dictionary on training set
with open('trump_neg_training.csv', 'rU') as trump_neg:
    reader = csv.reader(trump_neg, delimiter='|', quotechar='|')
    totalWordsTrumpNegDict = 0
    for row in reader:
        if len(row) > 0:
            rawTweet = row[0]
            filteredTweet = " ".join([w for w in rawTweet.split() if w not in stopwords and w != "RT" and w[0] != "@" and w[0] != "#" and "http" not in w])
            for word in filteredTweet.split():
                if len(word) < 1:
                    continue
                elif word not in trump_neg_dict:
                    trump_neg_dict[word] = 2 #start wordcount at 2 for additive smoothing
                    totalWordsTrumpNegDict += 2
                else:
                    trump_neg_dict[word] += 1
                    totalWordsTrumpNegDict += 1

    #compute natural logs of occurence probabilities
    for key in trump_neg_dict.keys():
        trump_neg_dict[key] = math.log(float(trump_neg_dict[key])/ totalWordsTrumpNegDict)

#Build Trump positive sentiment dictionary on training set
with open('trump_pos_training.csv', 'rU') as trump_pos:
    reader = csv.reader(trump_pos, delimiter='|', quotechar='|')
    totalWordsTrumpPosDict = 0
    for row in reader:
        if len(row) > 0:
            rawTweet = row[0]
            filteredTweet = " ".join([w for w in rawTweet.split() if w not in stopwords and w != "RT" and w[0] != "@" and w[0] != "#" and "http" not in w])
            for word in filteredTweet.split():
                if len(word) < 1:
                    continue
                elif word not in trump_pos_dict:
                    trump_pos_dict[word] = 2 #start wordcount at 2 for additive smoothing
                    totalWordsTrumpPosDict += 2
                else:
                    trump_pos_dict[word] += 1
                    totalWordsTrumpPosDict += 1

    #compute natural logs of occurence probabilities
    for key in trump_pos_dict.keys():
        trump_pos_dict[key] = math.log(float(trump_pos_dict[key])/ totalWordsTrumpPosDict)

#Build Clinton negative sentiment dictionary
with open('clinton_neg_training.csv', 'rU') as clinton_neg:
    reader = csv.reader(clinton_neg, delimiter='|', quotechar='|')
    totalWordsClintonNegDict = 0
    for row in reader:
        if len(row) > 0:
            rawTweet = row[0]
            filteredTweet = " ".join([w for w in rawTweet.split() if w not in stopwords and w != "RT" and w[0] != "@" and w[0] != "#" and "http" not in w])
            for word in filteredTweet.split():
                if len(word) < 3:
                    continue
                elif word not in clinton_neg_dict:
                    clinton_neg_dict[word] = 2 #start wordcount at 2 for additive smoothing
                    totalWordsClintonNegDict += 2
                else:
                    clinton_neg_dict[word] += 1
                    totalWordsClintonNegDict += 1

    #compute natural logs of occurence probabilities
    for key in clinton_neg_dict.keys():
        clinton_neg_dict[key] = math.log(float(clinton_neg_dict[key])/ totalWordsClintonNegDict)

#Build Clinton positive sentiment dictionary
with open('clinton_pos_training.csv', 'rU') as clinton_pos:
    reader = csv.reader(clinton_pos, delimiter='|', quotechar='|')
    totalWordsClintonPosDict = 0
    for row in reader:
        if len(row) > 0:
            rawTweet = row[0]
            filteredTweet = " ".join([w for w in rawTweet.split() if w not in stopwords and w != "RT" and w[0] != "@" and w[0] != "#" and "http" not in w])
            for word in filteredTweet.split():
                if len(word) < 3:
                    continue
                elif word not in clinton_pos_dict:
                    clinton_pos_dict[word] = 2 #start wordcount at 2 for additive smoothing
                    totalWordsClintonPosDict += 2
                else:
                    clinton_pos_dict[word] += 1
                    totalWordsClintonPosDict += 1

    #compute natural logs of occurence probabilities
    for key in clinton_pos_dict.keys():
        clinton_pos_dict[key] = math.log(float(clinton_pos_dict[key])/ totalWordsClintonPosDict)

#Run model on test set for Trump
#All these tweets should be negative
with open('trump_neg_test.csv', 'rU') as trump_neg_test:
    reader = csv.reader(trump_neg_test, delimiter='|', quotechar='|')
    numPositiveTweets = 0
    numNegativeTweets = 0
    for row in reader:
        if len(row) > 0:
            rawTweet = row[0]
            rawTweet = rawTweet.replace('\n', ' ')
            probPositive = 0.0
            probNegative = 0.0
            filteredTweet = " ".join([w for w in rawTweet.split() if
                                      w not in stopwords and w != "RT" and w[0] != "@" and w[
                                          0] != "#" and "http" not in w])
            for word in filteredTweet.split():
                if len(word) < 1:
                    continue
                if word in trump_pos_dict:
                    probPositive += trump_pos_dict[word]
                else:
                    probPositive += math.log(float(1)/totalWordsTrumpPosDict) #assume new word occurs once as part of additive smoothing

                if word in trump_neg_dict:
                    probNegative += trump_neg_dict[word]
                else:
                    probNegative += math.log(float(1) / totalWordsTrumpNegDict)  #assume new word occurs once as part of additive smoothing

            if probPositive > probNegative:
                # print "Wrong: " + rawTweet
                numPositiveTweets += 1
            else:
                # print "Negative Tweet"
                numNegativeTweets += 1

    print "Trump Negative"
    print "Number positive tweets" + str(numPositiveTweets)
    print "Number negative tweets" + str(numNegativeTweets)

#All these tweets should be positive
with open('trump_pos_test.csv', 'rU') as trump_pos_test:
    reader = csv.reader(trump_pos_test, delimiter='|', quotechar='|')
    numPositiveTweets = 0
    numNegativeTweets = 0
    for row in reader:
        if len(row) > 0:
            rawTweet = row[0]
            rawTweet = rawTweet.replace('\n', ' ')
            probPositive = 0.0
            probNegative = 0.0
            filteredTweet = " ".join([w for w in rawTweet.split() if
                                      w not in stopwords and w != "RT" and w[0] != "@" and w[
                                          0] != "#" and "http" not in w])
            for word in filteredTweet.split():
                if len(word) < 1:
                    continue
                if word in trump_pos_dict:
                    probPositive += trump_pos_dict[word]
                else:
                    probPositive += math.log(float(1)/totalWordsTrumpPosDict) #assume new word occurs once as part of additive smoothing

                if word in trump_neg_dict:
                    probNegative += trump_neg_dict[word]
                else:
                    probNegative += math.log(float(1) / totalWordsTrumpNegDict)  #assume new word occurs once as part of additive smoothing

            if probPositive > probNegative:
                # print "Positive Tweet"
                numPositiveTweets += 1
            else:
                print "Wrong: " + rawTweet
                numNegativeTweets += 1

    print "Trump Positive"
    print "Number positive tweets" + str(numPositiveTweets)
    print "Number negative tweets" + str(numNegativeTweets)

#Run model on test set for Clinton
#All these tweets should be negative
with open('clinton_neg_validation.csv', 'rU') as clinton_neg_test:
    reader = csv.reader(clinton_neg_test, delimiter='|', quotechar='|')
    numPositiveTweets = 0
    numNegativeTweets = 0
    for row in reader:
        if len(row) > 0:
            rawTweet = row[0]
            rawTweet = rawTweet.replace('\n', ' ')
            probPositive = 0.0
            probNegative = 0.0
            filteredTweet = " ".join([w for w in rawTweet.split() if
                                      w not in stopwords and w != "RT" and w[0] != "@" and w[
                                          0] != "#" and "http" not in w])
            for word in filteredTweet.split():
                if len(word) < 1:
                    continue
                if word in clinton_pos_dict:
                    probPositive += clinton_pos_dict[word]
                else:
                    probPositive += math.log(float(1)/totalWordsClintonPosDict) #assume new word occurs once as part of additive smoothing

                if word in clinton_neg_dict:
                    probNegative += clinton_neg_dict[word]
                else:
                    probNegative += math.log(float(1)/totalWordsClintonNegDict)  #assume new word occurs once as part of additive smoothing

            if probPositive > probNegative:
                # print "Wrong: " + rawTweet
                numPositiveTweets += 1
            else:
                # print "Negative Tweet"
                numNegativeTweets += 1

    print "Clinton Negative"
    print "Number positive tweets" + str(numPositiveTweets)
    print "Number negative tweets" + str(numNegativeTweets)

#All these tweets should be positive
with open('clinton_pos_test.csv', 'rU') as clinton_pos_test:
    reader = csv.reader(clinton_pos_test, delimiter='|', quotechar='|')
    numPositiveTweets = 0
    numNegativeTweets = 0
    for row in reader:
        if len(row) > 0:
            rawTweet = row[0]
            rawTweet = rawTweet.replace('\n', ' ')
            probPositive = 0.0
            probNegative = 0.0
            filteredTweet = " ".join([w for w in rawTweet.split() if
                                      w not in stopwords and w != "RT" and w[0] != "@" and w[
                                          0] != "#" and "http" not in w])
            for word in filteredTweet.split():
                if len(word) < 1:
                    continue
                if word in clinton_pos_dict:
                    probPositive += clinton_pos_dict[word]
                else:
                    probPositive += math.log(float(1)/totalWordsClintonPosDict) #assume new word occurs once as part of additive smoothing

                if word in clinton_neg_dict:
                    probNegative += clinton_neg_dict[word]
                else:
                    probNegative += math.log(float(1) / totalWordsClintonNegDict)  #assume new word occurs once as part of additive smoothing

            if probPositive > probNegative:
                # print "Positive Tweet"
                numPositiveTweets += 1
            else:
                print "Wrong: " + rawTweet
                numNegativeTweets += 1

    print "Clinton Positive"
    print "Number positive tweets" + str(numPositiveTweets)
    print "Number negative tweets" + str(numNegativeTweets)