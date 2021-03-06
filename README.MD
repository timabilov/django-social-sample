## timabilov / django-social-sample [![Build Status](https://travis-ci.org/timabilov/django-social-sample.svg?branch=master)](https://travis-ci.org/timabilov/django-social-sample)

Required `docker` and `docker-compose` 
###### docker-compose-prod.yml  is not production ready. used for `uwsgi bot setup`  ONLY. 


`./startup.sh`


Add your `CLEARBIT_KEY` to configuration `env.secret` if you want.

Open `http://localhost/` 

For spamming/testing API in `bot/` directory:

`python social_bot.py -u 100 -p 20 -l 20`  
`python social_bot.py --config config.json`  
 

>### API

**POST** */v1.0/signup/*
```json
{
  "username": "username" ,
  "password": "validatedpass"
}
```

**POST** */v1.0/token/*

Use your credentials. JWT used. 
```json
{
  "username": "username" ,
  "password": "validatedpass"
}
```



**POST** */v1.0/posts/*

Create post. 
```json
{
  "content": "Summertime sadness?"
}
```

**GET** */v1.0/posts/*

Posts list 
```json
{
  "posts": [
        {
            "id": 1,
            "user": {
                "id": 4,
                "username": "willsmith",
                "img": null
            },
            "content": "Summertime sadness?",
            "date": "just now",
            "likes": 0,
            "liked": false
        }
  ],
  "count": 1
}
```

**POST**    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;  */v1.0/posts/{id}/like/*

**DELETE** &nbsp; */v1.0/posts/{id}/like/*

