#!/usr/bin/python2.7

import json
import os.path

states = ["PA"]

def write_restaurants():
    restaurant_categories = ["Restaurants", "Coffee", "Food", "Cafes", "Nightlife", "Bars", "Juice Bars & Smoothies"]
    with open('business.json', 'r') as yelp_business:
        if os.path.exists('state_restaurants.json'):
            print("State restaurant file exists.")
            return

        yelp_restaurant_file = open('state_restaurants.json', 'w')
        yelp_restaurant_file.close()
        for line in yelp_business:
            json_line = json.loads(line)
            if any(item in json_line["categories"] for item in restaurant_categories)\
                    and any(state == json_line["state"] for state in states):
                with open('state_restaurants.json', 'a') as yelp_restaurant_file:
                    yelp_restaurant_file.write(line)

def get_business_list():
    restaurants = []
    with open('state_restaurants.json', 'r') as yelp_restaurant_file:
        for line in yelp_restaurant_file:
            json_line = json.loads(line)
            restaurants.append(json_line['business_id'])

    return restaurants

def write_reviews(restaurants):
    with open('yelp/restaurant_review.json', 'r') as yelp_reviews:
        if os.path.exists('yelp/state_restaurant_review.json'):
            return

        yelp_restaurant_file = open('yelp/state_restaurant_review.json', 'w')
        yelp_restaurant_file.close()
        for line in yelp_reviews:
            json_line = json.loads(line)
            if json_line['business_id'] in restaurants:
                with open('yelp/state_restaurant_review.json', 'a') as yelp_restaurant_file:
                    yelp_restaurant_file.write(line)

def main():
    write_restaurants()
    write_reviews(get_business_list())

if __name__ == "__main__":
    main()
