# naive-bayes-sentiment-analysis
Python implementation of Naive Bayes to predict sentiment of Election 2016 tweets relating to Trump/Clinton.
FetchTweets.py pulls down tweets containing various search terms and tosses them into a CSV.
NaiveBayes.py runs Naive Bayes using the bag-of-words model, additive smoothing, and Python's NLTK to eliminate stopwords.
Results: this simple algorithm predicted positive tweets correctly about 80% of the time and negative tweets about 65% of the time. I suspect this difference is due to sarcasm in negative tweets being hard to detect by the bag-of-words model.
