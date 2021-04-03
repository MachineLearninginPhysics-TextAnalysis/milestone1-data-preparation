# milestone1-data-preparation
This repository gathers tools and files needed for extraction text data from Twitter, building corpora and representing documents in various representations. Some basic transformations (models like TF-IDF, LSI, LDA, etc.) would be briefly implemented here.

We use machine learning to analyze the text of Twitter tweets, to categorize them. The language we use is Python, and our research is directly related to concepts such as data collection, BOW, NLP, topic recognition, etc. The first goal is to categorize and analyze the tweets supervisory, and the second goal is to do these for unsupervised format.

1. Downloading_and_init_processing.ipynb:
With the file entitled 'Downloading_and_init_processing.ipynb' yo can download and do some initial processing on data. Please not that you have to use your access_token, access_token_secret, consumer_key, and consumer_secret, according to your developer Twitter account. There are two outputs for this code: first, there is a file entitled 'tweet_information.csv'; and second, there is a file entitled 'most_words_list_result.csv'. First file contains the information about tweets (such as the text, ID, date, etc.). Second file contains the frequency of "the most repetitious words in each class" in all classes. For example, if the frequency of the word 'the' is 27, it means that this word has been repetitious in 27 classes; and if the frequency of the word 'close' is 1, it means that this word has been repetitious in 1 class. Being repetitious means being one of the 266 repetitious words, in one class or more. Also, other advanced processing on data, will be applied in another Jupiter file.

2. tweet_information.csv:
The file entitled 'tweet_information.csv' contains 7 columns about tweets of Twitter users. The number of tweets is 98681, and all of them has been collected in March 2021, by our team. The columns in this file are ID, user name, date of creation, text of tweet, length of text of tweet, the target tag, and the kind of data collecting filtering (all of them are 'filter:retweets'). Some initial processing has been performed on the tweets, such as lowercasing the text, eliminating emojis and replicas, etc. This file, is one of the outputs of "Downloading_and_init_processing.ipynb" file. Other processing will be considered in the next Jupiter file.

3. most_words_list_result.csv:

4. most_words_list_result: By Group:
The files in "most_words_list_result: By Group" are some CSV files, that contains some information about the file 'most_words_list_result.csv' by group. Actually, we have put the related "the most repetitious words" in smaller files, that each of theme contains 4 classes (instead of 27 classes). So, each of these CSV files contains the most repetitious words of 4 classes (the last file contains 3 classes).
