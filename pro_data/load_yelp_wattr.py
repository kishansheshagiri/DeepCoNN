'''
Data pre process

@author:
Chong Chen (cstchenc@163.com)

@ created:
25/8/2017
@references:
'''
import os
import json
import pandas as pd
import pickle
import numpy as np
TPS_DIR = '../data/yelp/penn'
TP_file = os.path.join(TPS_DIR, 'restaurant_review.json')

f= open(TP_file)
users_id=[]
items_id=[]
ratings=[]
reviews=[]
np.random.seed(2017)
adding_attributes = True

############################################################################################################
if (adding_attributes):
    # extra code for managing context
    fh = open('../data/yelp/penn/restaurant_review.json', 'r')
    i=0
    review_ids = []
    business_ids = []
    for line in fh:
        json_line = json.loads(line)
        #print(json_line.keys())
        review_ids.append(json_line['review_id'])
        business_ids.append(json_line['business_id'])
    fh.close()

    def stringify_dict(dictionary):
        if (type(dictionary) is str):
            return dictionary
        if (type(dictionary) is bool):
            return str(dictionary)
        if (type(dictionary) is int):
            return str(dictionary)
        if (type(dictionary) is unicode):
	    return dictionary.encode('ascii', 'ignore')
        else:
            strings = []
            for key, value in dictionary.items():
                strings.append(stringify_dict(key))
                strings.append(stringify_dict(value))
            return ' '.join(str(i) for i in strings)

    fh = open('../data/yelp/business.json', 'r')
    i=0
    temp_attributes = {}
    for line in fh:
        json_line = json.loads(line)
        temp_attributes[json_line['business_id']] = stringify_dict(json_line['attributes'])
    fh.close()
    attributes = []
    for i in business_ids:
        attributes.append(temp_attributes[i])
    print(len(attributes))
    print(len(business_ids))
    #print(attributes[1:10])

    #split the words on seeing a uppercase
    import re
    revised_attributes = []
    for at in attributes:
        words = at.split(' ')
        revised_words = []
        for w in words:
            if (sum(1 for c in w if c.isupper()) > 1):
                revised_words.append(' '.join(str(i) for i in re.findall('[A-Z][^A-Z]*', w)))
            else:
                revised_words.append(w)
        revised_attributes.append(' '.join(str(i) for i in revised_words))

    #print(revised_attributes[1:10])
    print(len(revised_attributes))

    #adding the stringified attributes to the reviews
    #fh = open('business.json', 'r')
    fh = open('../data/yelp/penn/restaurant_review.json', 'r')
    i=0
    js_ = []
    for line in fh:
        data = json.loads(line)
        data['text'] = data['text'] + " " + revised_attributes[i]
        jsondata = json.dumps(data)
        js_.append(data)
        i+=1
    fh.close()
    print(len(js_))

##########################################################################################################
#for index, line in enumerate(f):
#    print(index) 
for js in js_:
    #js=json.loads(line)
    if str(js['user_id'])=='unknown':
        print("unknown")
        continue
    if str(js['business_id'])=='unknown':
        print("unknown2")
        continue

    reviews.append(js['text'])
    users_id.append(str(js['user_id'])+',')
    items_id.append(str(js['business_id'])+',')
    ratings.append(str(js['stars']))
data=pd.DataFrame({'user_id':pd.Series(users_id),
                   'item_id':pd.Series(items_id),
                   'ratings':pd.Series(ratings),
                   'reviews':pd.Series(reviews)})[['user_id','item_id','ratings','reviews']]
print data

def get_count(tp, id):
    playcount_groupbyid = tp[[id, 'ratings']].groupby(id, as_index=False)
    count = playcount_groupbyid.size()
    return count

MIN_USER_COUNT = 5
MIN_SONG_COUNT = 5
def filter_triplets(tp, min_uc=MIN_USER_COUNT, min_sc=MIN_SONG_COUNT):
    # Only keep the triplets for songs which were listened to by at least min_sc users.
    songcount = get_count(tp, 'item_id')

    tp = tp[tp['item_id'].isin(songcount.index[songcount >= min_sc])]

    # Only keep the triplets for users who listened to at least min_uc songs
    # After doing this, some of the songs will have less than min_uc users, but should only be a small proportion
    usercount = get_count(tp, 'user_id')

    tp = tp[tp['user_id'].isin(usercount.index[usercount >= min_uc])]

    # Update both usercount and songcount after filtering
    usercount, songcount = get_count(tp, 'user_id'), get_count(tp, 'item_id')
    return tp, usercount, songcount

data,usercount, itemcount=filter_triplets(data)
#print(data.values)
#usercount, itemcount = get_count(data, 'user_id'), get_count(data, 'item_id')

print(data.shape[0])
print(usercount.shape[0])
print(itemcount.shape[0])

unique_uid = usercount.index
unique_sid = itemcount.index
item2id = dict((sid, i) for (i, sid) in enumerate(unique_sid))
user2id = dict((uid, i) for (i, uid) in enumerate(unique_uid))
#print(item2id)
def numerize(tp):
    uid = map(lambda x: user2id[x], tp['user_id'])
    sid = map(lambda x: item2id[x], tp['item_id'])
    tp['user_id'] = uid
    tp['item_id'] = sid
    #print(sid)
    return tp

#print(data.values)
data=numerize(data)
#print(data.values)
tp_rating=data[['user_id','item_id','ratings']]


n_ratings = tp_rating.shape[0]
test = np.random.choice(n_ratings, size=int(0.20 * n_ratings), replace=False)
test_idx = np.zeros(n_ratings, dtype=bool)
test_idx[test] = True

tp_1 = tp_rating[test_idx]
tp_train= tp_rating[~test_idx]
data=data[~test_idx]

n_ratings = tp_1.shape[0]
test = np.random.choice(n_ratings, size=int(0.50 * n_ratings), replace=False)

test_idx = np.zeros(n_ratings, dtype=bool)
test_idx[test] = True

tp_test = tp_1[test_idx]
tp_valid = tp_1[~test_idx]
tp_train.to_csv(os.path.join(TPS_DIR, 'yelp_train.csv'), index=False,header=None)
tp_valid.to_csv(os.path.join(TPS_DIR, 'yelp_valid.csv'), index=False,header=None)
tp_test.to_csv(os.path.join(TPS_DIR, 'yelp_test.csv'), index=False,header=None)

user_reviews={}
item_reviews={}
user_rid={}
item_rid={}
#print(type(data))
iter=0
for i in data.values:
    #print(iter)
    #print("Data")
    #print(len(data))
    if i[0] in user_reviews.keys():
        user_reviews[i[0]].append(i[3])
        user_rid[i[0]].append(i[1])
    else:
        user_rid[i[0]]=[i[1]]
        user_reviews[i[0]]=[i[3]]
    if i[1] in item_reviews.keys():
        item_reviews[i[1]].append(i[3])
        item_rid[i[1]].append(i[0])
    else:
        item_reviews[i[1]] = [i[3]]
        item_rid[i[1]]=[i[0]]
    iter += 1
#print(data.values)
#print("Item review keys")
for i in item_reviews.keys():
        print(i)
print(item_reviews[11])
#print(data.values)
#print(len(data.values))
#storing the files in respective files
pickle.dump(user_reviews, open(os.path.join(TPS_DIR, 'user_review'), 'wb'))
pickle.dump(item_reviews, open(os.path.join(TPS_DIR, 'item_review'), 'wb'))
pickle.dump(user_rid, open(os.path.join(TPS_DIR, 'user_rid'), 'wb'))
pickle.dump(item_rid, open(os.path.join(TPS_DIR, 'item_rid'), 'wb'))

usercount, itemcount = get_count(data, 'user_id'), get_count(data, 'item_id')


print(np.sort(np.array(usercount.values)))

print(np.sort(np.array(itemcount.values)))
