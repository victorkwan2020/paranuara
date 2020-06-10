# Paranuara Challenge

## Main Features

* Given a company, the API needs to return all their employees. Provide the appropriate solution if the company does not have any employees.
* Given 2 people, provide their information (Name, Age, Address, phone) and the list of their friends in common which have brown eyes and are still alive.
* Given 1 people, provide a list of fruits and vegetables they like. This endpoint must respect this interface for the output: `{"username": "Ahi", "age": "30", "fruits": ["banana", "apple"], "vegetables": ["beetroot", "lettuce"]}`

## Prerequistes

* Docker
* docker-compose
* internet connection (to pull down base image for building the app containers)
* Port 27017 and 27016 on localhost will need to be vacant as they get used by the services

## Installation

To keep things simple, the building of containers are part of the docker-compose config. So everytime you bring the services up, it will attempt to build the image on-spot. This shouldn't add too much to the startup time except for the first run where the base images gets pull down from dockerhub. As the last step of the build process, the automated test included will be run and the buildwill fail if any tests fails. 

### To run the API services (and building it)

In the root directory where the docker-compose.yaml file is run

```sh
docker-compose up -d 
```

### To stop the API services

```sh
docker-compose down
```

### To populate DB with data

The provided people.json, companies.json has been copied to the resource folder. A food.json was also introduced as mean of hadrdcoding in a list of known vegetables and fruits. Feel free to replace them for testing purpose. Add new fruits or vegetables to food.json if required. Any food that cannot be classified by the service will raise a warning in the log and only known food will be put forward to the output.

To insert the data from these 3 files, cd into the resources folder. While the API service (the mongo service) is up run:

```sh
./import.sh
```

The scripts just wraps 3 mongoimport command and expect mongo to be running at localhost:27017

## Tests

Mongomock was use for mocking out the real DB, so you should be able to run them without a DB server, as long as you install all the requirements and have python 3.8.3 and pip installed

In the application root folder run:
```sh
python -m unittest -vvv test.test_app
```

## Other notes

* Code design is quite simple as the service is simple. I try to keep code in 3 layers to separate concerns:
  * RESTFUL frontend (app.py)
  * business logic (people_info.py)
  * storage/domain model (models.py)
* Mongo was used for a few reasons:
 * easy to setup, very little db admin invovled
 * data already in json like format, which make importing very straight forward
 * scope of service don't required modelling complex relationship between many different entities
 * there are other factors that could change this decsions eg. volume of data, performance requirments, likelihood of other data being added,  other potential future usecases of the services. With all of those not known and base on the KISS pricipal, i chose the option that requires the least code to implement with.
* Preprocess steps may simplify the code:
  * Veg and Fruit classes are being read into the service once and being cached at the moment. And each time food list was requested the Fruits and Vegetable list get generated on the fly. This could have been done for each person's record straight after the import
  * Friends list for each person contains self references and friends that are potentially dead or don't have brown eyes. We could also clean the friends list for every person on startup so it only contains friends that is still alive and have brown eyes, then the querying code will also be simplified. But its really a micro-opitmization that you need to undo as soon as a new query required base on friends.
* To fulfill the 3 requirements, you can actually do it without importing the companies data. I currently import it and only uses it to validate rather a company index provided exists(which is not really a requirement specified). Without this validation, a company index that don't exist could simply return no employees and that technically still make senses, but i added the validation for completeness 
