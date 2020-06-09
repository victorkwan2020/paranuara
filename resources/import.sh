#!/bin/bash

mongoimport --db paranuaraDB --collection company --drop --jsonArray --file companies.json
mongoimport --db paranuaraDB --collection people --drop --jsonArray --file people.json
mongoimport --db paranuaraDB --collection food --drop --jsonArray --file food.json
