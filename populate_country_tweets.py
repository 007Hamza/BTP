import MySQLdb as mdb

con = mdb.connect('localhost' , 'root' , 'admin' , 'happiness_index')
cur1 = con.cursor()
cur1.execute("SELECT * FROM geo_tweets")
con.commit() 
numrows = int(cur.rowcount)
cur2 = con.cursor()
for x in range(0 , numrows):
    row = cur1.fetchone()
    country = row[4]
    sent_pos = row[2]
    sent_neg = row[3]
    cur2.execute("SELECT * from country_tweets WHERE country = %s" , (row[4]))
    rs = cur2.fetchAll()
    no_of_tweets = None
    sent_pos = None
    sent_neg = None
    for r in rs:
        no_of_tweets = r[1]
        sent_pos_t = r[2]
        sent_neg_t = r[3] 
        cur2.execute("UPDATE country_tweets SET no_of_tweets = %d , sent_pos = %s , sent_neg = %s WHERE country = %s" , (no_of_tweets+1 , sent_pos+sent_pos_t , sent_neg+sent_pos_t , row[4]))
    if len(rs) == 0 :
        cur2.execute("INSERT INTO country_tweets values (%s , %s , %s , %s)" , (row[4] , 1 , sent_pos , sent_neg)) 
    print "success\n"
    con.commit()
