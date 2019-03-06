# aiohttp and peewee-async testing examples

The project is focused on testing aiohttp apps with pytest. Main points are: testing an asynchronous code which 
is using database; pytest fixtures for a database. 

As the example of an aiohttp application I have made a simple REST API for a pool application from the [standard Django tutorial](https://docs.djangoproject.com/en/2.0/intro/tutorial01/).

## Examples of tasks to be solved

* Working with a database within tests
* Creating pytest fixtures for Peewee models
* Run database migrations automatically before tests 
* Testing an aiohttp code which is works with database using Peewee-async
* A fixture which is helping to get the uri path of an appropriate resource (`route_path()`)

## Built With

* [aiohttp](https://aiohttp.readthedocs.io/) - asynchronous HTTP Client/Server for asyncio and Python
* [Postgresql](https://www.postgresql.org/docs/manuals/) - powerful, open source object-relational database system
* [Async-peewee](https://peewee-async.readthedocs.io/en/latest/) - a library providing asynchronous interface powered by [asyncio](https://docs.python.org/3/library/asyncio.html) for [peewee](https://github.com/coleifer/peewee) ORM
* [peewee-migrate](https://github.com/klen/peewee_migrate) - a simple migration engine for Peewee

### Prerequisites

* Python >= 3.5.3 
* Postgresql or MySQL

It really doesn't matter which relational database you'll use. MySQL or Postgresql will meet the requirements. **Nevertheless the example uses Postgresql.**

## Getting Started

* Clone the repository
* Create a virtual environment with the appropriate version of Python
* Activate the virtual environment and install packages from `requirements.txt`
* Create a `.env` file in the project's root directory (`.env.example` file is provided as the example)
* Create a database for the application. Example: `pool`
* Create a test database with the postfix `_test`. Example: `pool_test`
* Run the tests: `pytest`

## Run tests

Run tests:

```
pytest
``` 

The tests are contain `print()` instructions to support a verbose mode so `pytest` may be running with `-s` flag:

```
pytest -s
```

## Database Migrations

Migrations are **run automatically** on the application start up.

### Examples of usage

#### Create

```
pw_migrate create --database "postgresql://[user]:[password]@[host]/[db_name]" --auto api.models [migration_name]
```

#### Run

##### All

```
pw_migrate migrate --database "postgresql://[user]:[password]@[host]/[db_name]"
```

##### Single

```
pw_migrate migrate --database "postgresql://[user]:[password]@[host]/[db_name]" --name [migration_name]
```


#### Rollback

```
pw_migrate rollback --database "postgresql://[user]:[password]@[host]/[db_name]" migration_name
```

Only one migration from the end would be cancelled


## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

### Code style

* PEP-8 (lines length - 80)

## License

This project is licensed under the MIT License
