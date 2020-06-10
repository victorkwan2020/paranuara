# API Documentation

Refer to instruction in README.md to install and start the service

Onces started, thed endpoints should be exposed locally on `http://localhost:27016/`


## Heartbeat

An endpoint to check rather the service is up and running

```sh
curl -X GET http://localhost:27016/alive
```

The above should return the string "Alive"


## Company

### List all employees of a company 

The endpoint provided expects the index id of the company

```sh
curl -X GET http://localhost:27016/company/<index id>/employees

example:
curl -X GET http://localhost:27016/company/1/employees
```

The above will try to list all the employees of company with index "1"

Output from above should be in json format similar to :

```json
[
    {
        "index": 289,
        "name": "Frost Foley"
    },
    {
        "index": 580,
        "name": "Luna Rodgers"
    },
    {
        "index": 670,
        "name": "Boyer Raymond"
    },
    {
        "index": 714,
        "name": "Solomon Cooke"
    },
    {
        "index": 828,
        "name": "Walter Avery"
    },
    {
        "index": 928,
        "name": "Hester Malone"
    },
    {
        "index": 985,
        "name": "Arlene Erickson"
    }
]
```
Company with no employees will yield  an empty list [] as result

## People

### Favourite Food

By specifying a person's index id, returns his/her favourite fruits and vegetables.

Food that cannot be classified by system will not be included in the output, a warning will be logged for system admins to update the classification data.

```sh
curl -X GET http://localhost:27016/people/<index id>/favourite_food

example:
curl -X GET http://localhost:27016/people/1/favourite_food
```

Sample output:

```json
{
    "username": "Decker Mckenzie",
    "age": 60,
    "fruits": [],
    "vegetables": [
        "cucumber",
        "beetroot",
        "carrot",
        "celery"
    ]
}
```

### Common friends

By providing the index id of 2 people, this enpoint will return common friends of them whom also is still alive and have brown eyes


```sh
curl -X GET http://localhost:27016/people/<index id>/common_friends_with/<index id>

example:
curl -X GET http://localhost:27016/people/3/common_friends_with/2
```

Sample output:

```json
{
    "person1": {
        "name": "Grace Kelly",
        "age": 24,
        "address": "762 Tabor Court, Ola, Idaho, 4329",
        "phone": "+1 (923) 600-2868"
    },
    "person2": {
        "name": "Cote Booth",
        "age": 26,
        "address": "394 Loring Avenue, Salvo, Maryland, 9396",
        "phone": "+1 (842) 598-3525"
    },
    "common_friends": [
        {
            "age": 60,
            "name": "Decker Mckenzie",
            "phone": "+1 (893) 587-3311",
            "address": "492 Stockton Street, Lawrence, Guam, 4854"
        },
        {
            "age": 62,
            "name": "Mindy Beasley",
            "phone": "+1 (862) 503-2197",
            "address": "628 Brevoort Place, Bellamy, Kansas, 2696"
        }
    ]
}
```

