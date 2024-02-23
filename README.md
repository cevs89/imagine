# Imagine

## Python Version
`>3.10`

## Docker | Run server
> You had to have installed  `docker` and `docker-compose`
>
> Docker: https://docs.docker.com/engine/install/ubuntu/
>
> Docker-compose: https://docs.docker.com/compose/install/

**Run the command**

If you need to deploy through Docker I did development a script in bash for make this easier

### Start Project

```
./imagine.sh runserver
```

> This command has works with permission to execute.  If this command does not work, please execute: `chmod +x imagine.sh`

This command `build`, `migrations`, and will run the `server`, if you want to development in docker environment


**Comment:**

Sometimes you need to run the command with `sudo` in that way you have to run the follows command:

```
> ./imagine.sh help

imagine.sh commands:
  runserver: run the development stack"
  migrate: run migrate to DB"
  run: Just run de server"
  exec: run a command inside a running container
  manage.py: run a manage.py command"
```


## Virtual Environment | Development
> You had to have installed `virtualenv` and `pip`

**1- Initial your virtualenv**

`virtualenv <path> --python=python3.10`

**2- Active your virtualenv**

`source <path>/bin/activate`

**3- Install Dependency**

`pip install -r requirements/base.txt`

**4- load User Admin and Group Users**

`python manage.py loaddata fixtures/users_admin.json`
___


## User Admin Default

You have to use the following credentials

| user                 | password    |
|----------------------|-------------|
| imagine@example.com  | imagine123  |

___

## Documentation API
#### Imagine API (v1)

Auto Docs by Schema swagger: [http://localhost:8000/docs/](http://localhost:8000/docs/)

Imagine API ReDoc: [http://localhost:8000/redoc/](http://localhost:8000/redoc/)

___

## Install this if you need to development
> Before you has to install Virtual Enviroment

### 1- How to set up dev tools
* install dev requirements  `pip install -r requirements/dev.txt`
* run  `pre-commit install`

### 2- How to set up linters tools
* install linters requirements  `pip install -r requirements/linters.txt`

### 3- How to run linters?
There are 3 types of linters:

* **Black:** Which formats the python code to black style: `black apps/`

* **Flake8:** which analyze code: `flake8 apps/`

* **Isort:** isort your imports, so you don't have to: `isort apps/ --profile black`

### 4- You can also run all linters as follows:

* `pre-commit run --all-files`

Details before run
```
Check Yaml...............................................................Passed
Fix End of Files.........................................................Passed
Trim Trailing Whitespace.................................................Passed
black....................................................................Passed
flake8...................................................................Passed
isort....................................................................Passed
```
