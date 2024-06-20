# How to install:

## Clone git repository:
```
 git clone https://github.com/berestianyi/pet-help.git
```
## Initialize poetry

```commandline
$ poetry init

$ poetry start

$ poetry update
```

## Add .env file with your database data

```commandline
$ echo DATABASE_URL=postgres://user:password@localhost:5432/dbname > .env
$ echo SECRET_KEY=mysecretkey >> .env
```

## Connect to database

```commandline
poerty run flask db init
```

```commandline
poerty run flask db migrate
```

```commandline
poerty run flask db upgrade
```


# Load fixtures of pets

```commandline
python load_fixtures.py
```