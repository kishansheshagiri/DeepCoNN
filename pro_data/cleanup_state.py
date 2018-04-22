#!/usr/bin/python2.7

import json
import os.path

TP_DIR = '../data'
TPS_DIR = '../data/yelp'
B_file = os.path.join(TP_DIR, 'business.json')
SR_file = os.path.join(TP_DIR, 'state_restaurants.json')
RREV_file = os.path.join(TP_DIR, 'restaurant_review.json')
SRREV_file = os.path.join(TPS_DIR, 'state_restaurant_review.json')

states = ["PA"]

def write_restaurants():
    restaurant_categories = ["Restaurants", "Coffee", "Food", "Cafes", "Nightlife", "Bars", "Juice Bars & Smoothies"]
    with open(B_file, 'r') as yelp_business:
        if os.path.exists(SR_file):
            print("State restaurant file exists.")
            return

        yelp_restaurant_file = open(SR_file, 'w')
        yelp_restaurant_file.close()
        for line in yelp_business:
            json_line = json.loads(line)
            if any(item in json_line["categories"] for item in restaurant_categories)\
                    and any(state == json_line["state"] for state in states):
                with open(SR_file, 'a') as yelp_restaurant_file:
                    yelp_restaurant_file.write(line)

def get_business_list():
    restaurants = []
    with open(SR_file, 'r') as yelp_restaurant_file:
        for line in yelp_restaurant_file:
            json_line = json.loads(line)
            restaurants.append(json_line['business_id'])

    return restaurants

def write_reviews(restaurants):
    with open(RREV_file, 'r') as yelp_reviews:
        if os.path.exists(SRREV_file):
            return

        yelp_restaurant_file = open(SRREV_file, 'w')
        yelp_restaurant_file.close()
        for line in yelp_reviews:
            json_line = json.loads(line)
            if json_line['business_id'] in restaurants:
                with open(SRREV_file, 'a') as yelp_restaurant_file:
                    yelp_restaurant_file.write(line)

def main():
    write_restaurants()
    write_reviews(get_business_list())

if __name__ == "__main__":
    main()
