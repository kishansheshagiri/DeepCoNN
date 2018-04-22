#!/usr/bin/python2.7

import json
import os.path
from sampler import random_sampler

TP_DIR = '../data'
B_file = os.path.join(TP_DIR, 'business.json')
R_file = os.path.join(TP_DIR, 'restaurants.json')
REV_file = os.path.join(TP_DIR, 'review.json')
RREV_file = os.path.join(TP_DIR, 'restaurant_review.json')
RS_file = os.path.join(TP_DIR, 'yelp', 'sample_restaurant_review.json')

def write_restaurants():
    restaurant_categories = ["Restaurants", "Coffee", "Food", "Cafes", "Nightlife", "Bars", "Juice Bars & Smoothies"]
    with open(B_file, 'r') as yelp_business:
        if os.path.exists(R_file):
            return

        yelp_restaurant_file = open(R_file, 'w')
        yelp_restaurant_file.close()
        for line in yelp_business:
            json_line = json.loads(line)
            if any(item in json_line["categories"] for item in restaurant_categories):
                with open(R_file, 'a') as yelp_restaurant_file:
                    yelp_restaurant_file.write(line)

def get_business_list():
    restaurants = []
    with open(R_file, 'r') as yelp_restaurant_file:
        for line in yelp_restaurant_file:
            json_line = json.loads(line)
            restaurants.append(json_line['business_id'])

    return restaurants

def write_reviews(restaurants):
    with open(REV_file, 'r') as yelp_reviews:
        if os.path.exists(RREV_file):
            return

        yelp_restaurant_file = open(RREV_file, 'w')
        yelp_restaurant_file.close()

        for line in yelp_reviews:
            json_line = json.loads(line)
            if json_line['business_id'] in restaurants:
                with open(RREV_file, 'a') as yelp_restaurant_file:
                    yelp_restaurant_file.write(line)

def main():
    write_restaurants()
    write_reviews(get_business_list())
    random_sampler(RREV_file, RS_file, 1500000)

if __name__ == "__main__":
    main()
