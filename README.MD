## timabilov / django-social-sample [![Build Status](https://travis-ci.org/timabilov/django-social-sample.svg?branch=master)](https://travis-ci.org/timabilov/django-social-sample)



1. docker-compose build
2. docker-compose run --rm ./manage.py makemigrations
3. docker-compose run --rm ./manage.py migrate
4. docker-compose run --rm ./manage.py createsuperuser *(Optional)*
5. docker-compose up

Add your `CLEARBIT_KEY` to configuration `env.secret` if you want.  

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
  ]
}
```

**POST**    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;  */v1.0/posts/{id}/like/*

**DELETE** &nbsp; */v1.0/posts/{id}/like/*

