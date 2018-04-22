#!/usr/bin/python2.7

import json
import os.path

TP_DIR = '../data'
B_file = os.path.join(TP_DIR, 'business.json')
R_file = os.path.join(TP_DIR, 'restaurants.json')
REV_file = os.path.join(TP_DIR, 'review.json')
RREV_file = os.path.join(TP_DIR, 'restaurant_review.json')

def write_restaurants():
<<<<<<< Updated upstream:pro_data/cleanup.py
    restaurant_categories = ["Restaurants", "Coffee", "Food", "Cafes", "Nightlife", "Bars", "Juice Bars & Smoothies"]
    with open(B_file, 'r') as yelp_business:
        if os.path.exists(R_file):
            return

        yelp_restaurant_file = open(R_file, 'w')
=======
    restaurant_categories = ["Restaurants", "Coffee", "Food", "Cafes", "Nightlife"]
    print("Part 1")
    with open('yelp/business.json', 'r') as yelp_business:
        if os.path.exists('yelp/restaurants.json'):
            return
        yelp_restaurant_file = open('yelp/restaurants.json', 'w')
>>>>>>> Stashed changes:data/cleanup.py
        yelp_restaurant_file.close()
        for line in yelp_business:
            json_line = json.loads(line)
            if any(item in json_line["categories"] for item in restaurant_categories):
<<<<<<< Updated upstream:pro_data/cleanup.py
                with open(R_file, 'a') as yelp_restaurant_file:
=======
                with open('yelp/restaurants.json', 'a') as yelp_restaurant_file:
>>>>>>> Stashed changes:data/cleanup.py
                    yelp_restaurant_file.write(line)

def get_business_list():
    restaurants = []
<<<<<<< Updated upstream:pro_data/cleanup.py
    with open(R_file, 'r') as yelp_restaurant_file:
=======
    with open('yelp/restaurants.json', 'r') as yelp_restaurant_file:
>>>>>>> Stashed changes:data/cleanup.py
        for line in yelp_restaurant_file:
            json_line = json.loads(line)
            restaurants.append(json_line['business_id'])

    return restaurants

def write_reviews(restaurants):
<<<<<<< Updated upstream:pro_data/cleanup.py
    with open(REV_file, 'r') as yelp_reviews:
        if os.path.exists(RREV_file):
            return

        yelp_restaurant_file = open(RREV_file, 'w')
=======
    print("Part 2")
    with open('yelp/review.json', 'r') as yelp_reviews:
        if os.path.exists('yelp/restaurant_review.json'):
            return

        yelp_restaurant_file = open('yelp/restaurant_review.json', 'w')
>>>>>>> Stashed changes:data/cleanup.py
        yelp_restaurant_file.close()
        i=0
        for line in yelp_reviews:
            if (i%10000 == 0):
                print(i)
            json_line = json.loads(line)
            if json_line['business_id'] in restaurants:
<<<<<<< Updated upstream:pro_data/cleanup.py
                with open(RREV_file, 'a') as yelp_restaurant_file:
=======
                with open('yelp/restaurant_review.json', 'a') as yelp_restaurant_file:
>>>>>>> Stashed changes:data/cleanup.py
                    yelp_restaurant_file.write(line)
            i+=1

def main():
    write_restaurants()
    write_reviews(get_business_list())

if __name__ == "__main__":
    main()
