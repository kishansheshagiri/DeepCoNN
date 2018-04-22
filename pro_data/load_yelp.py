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
from operator import add
from sklearn.decomposition import NMF

TPS_DIR = '../data/yelp'
TP_file = os.path.join(TPS_DIR, 'review.json')
SR_file = os.path.join('../data/yelp', 'business.json')
OUP_DIR = "../data/yelp/all"

f= open(TP_file)
users_id=[]
items_id=[]
ratings=[]
reviews=[]
attributes=[]
np.random.seed(2017)

sr_attr = dict()
sr_attr_set = set()
with open(SR_file) as sr_f:
    for line in sr_f:
        js = json.loads(line)
        cat = js["categories"]
        state_attr = cat
        js_attr = js["attributes"]
        if js_attr.get("Alcohol") and js_attr["Alcohol"] != "none":
            state_attr.append("Alcohol")
        if js_attr.get("OutdoorSeating") and js_attr["OutdoorSeating"] == True:
            state_attr.append("OutdoorSeating")
        if js_attr.get("RestaurantsDelivery") and js_attr["RestaurantsDelivery"] == True:
            state_attr.append("RestaurantsDelivery")
        if js_attr.get("RestaurantsTakeOut") and js_attr["RestaurantsTakeOut"] == True:
            state_attr.append("RestaurantsTakeOut")
        if js_attr.get("BusinessParking") and js_attr["BusinessParking"]["valet"] == True:
            state_attr.append("Valet")

        sr_attr_set.update(state_attr)
        sr_attr[js["business_id"]] = state_attr

sr_attr_list = sorted(sr_attr_set)
business_attributes = dict()
for sr, value in sr_attr.iteritems():
    attribute = [0] * len(sr_attr_list)
    for attr in value:
        attribute[sr_attr_list.index(attr)] = 1
    business_attributes[sr] = attribute

for index, line in enumerate(f):
    #print(index) 

    js=json.loads(line)
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
    attributes.append(business_attributes[js['business_id']])

data=pd.DataFrame({'user_id':pd.Series(users_id),
                   'item_id':pd.Series(items_id),
                   'ratings':pd.Series(ratings),
                   'reviews':pd.Series(reviews),
                   'attr':pd.Series(attributes)})[['user_id','item_id','ratings','reviews', 'attr']]

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
print(data.values)
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
tp_train.to_csv(os.path.join(OUP_DIR, 'yelp_train.csv'), index=False,header=None)
tp_valid.to_csv(os.path.join(OUP_DIR, 'yelp_valid.csv'), index=False,header=None)
tp_test.to_csv(os.path.join(OUP_DIR, 'yelp_test.csv'), index=False,header=None)

user_reviews={}
item_reviews={}
user_rid={}
user_attr={}
item_rid={}
item_attr={}
#print(type(data))
iter=0
for i in data.values:
    if (iter%100000==0):
        print(iter)
        print("Data")
        print(len(data))
    if user_reviews.has_key(i[0]):
        user_reviews[i[0]].append(i[3])
        user_rid[i[0]].append(i[1])
        user_attr[i[0]] = map(add, user_attr[i[0]], i[4])
    else:
        user_rid[i[0]]=[i[1]]
        user_reviews[i[0]]=[i[3]]
        user_attr[i[0]]=i[4]
    if item_reviews.has_key(i[1]):
        item_reviews[i[1]].append(i[3])
        item_rid[i[1]].append(i[0])
    else:
        item_reviews[i[1]] = [i[3]]
        item_rid[i[1]]=[i[0]]
        item_attr[i[1]]=i[4]
    iter += 1
#print(data.values)
#print("Item review keys")
for i in item_reviews.keys():
        print(i)
print(item_reviews[11])
#print(data.values)
#print(len(data.values))
#storing the files in respective files

## NMF on the user_attr list
#user_attr_mat = np.array(user_attr.values())
#model = NMF(n_components=8, init='random', random_state=0)
#uattr_topwise = model.fit_transform(user_attr_mat)
#print uattr_topwise
#print uattr_topwise.shape
#i = 0
#for key in user_attr.keys():
#    user_attr[key] = uattr_topwise[i,:]
#    i += 1

pickle.dump(user_reviews, open(os.path.join(OUP_DIR, 'user_review'), 'wb'))
pickle.dump(item_reviews, open(os.path.join(OUP_DIR, 'item_review'), 'wb'))
pickle.dump(user_rid, open(os.path.join(OUP_DIR, 'user_rid'), 'wb'))
pickle.dump(item_rid, open(os.path.join(OUP_DIR, 'item_rid'), 'wb'))
pickle.dump(user_attr, open(os.path.join(OUP_DIR, 'user_attr'), 'wb'))
pickle.dump(item_attr, open(os.path.join(OUP_DIR, 'item_attr'), 'wb'))

usercount, itemcount = get_count(data, 'user_id'), get_count(data, 'item_id')


print(np.sort(np.array(usercount.values)))

print(np.sort(np.array(itemcount.values)))
