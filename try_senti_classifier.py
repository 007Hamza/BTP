import MySQLdb as mdb
from senti_classifier import senti_classifier
#f = open('trial.txt' , 'r')
#sentences = f.read().rstrip()
#sentence_list = list()
#sentence_list.append(sentences)

#pos_score , neg_score = senti_classifier.polarity_scores(sentence_list)
#print pos_score , neg_score
con = mdb.connect('localhost' , 'root' , 'admin' , 'happiness_index')
cur = con.cursor()
cur.execute("SELECT * from geo_tweets")
con.commit()
numrows = int(cur.rowcount)
cur1 = con.cursor()
for x in range(0 , numrows):
    row = cur.fetchone()
    tweet = row[1]
    tweet_list = list()
    tweet_list.append(tweet)
    pos_score , neg_score = senti_classifier.polarity_scores(tweet_list)
    cur1.execute("update geo_tweets SET sent_pos = %s , sent_neg = %s WHERE id = %s" , (pos_score , neg_score , row[0]))
    print "success\n"
    con.commit()
    


