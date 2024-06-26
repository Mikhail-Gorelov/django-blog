## Django Blog project


#### Project features:
* Docker/Docker-compose environment
* Environment variables
* Separated settings for Dev and Prod django version
* Docker configuration for nginx for 80 and/or 443 ports (dev/stage/prod) (Let's Encrypt certbot)
* Celery worker
* Redis service for caching using socket. Also message broker for queue
* RabbitMQ configuration
* ASGI support
* Linters integration (flake8, black, isort)
* Swagger in Django Admin Panel
* Ready for deploy by one click
* Separated configuration for dev and prod (requirements and settings)
* CI/CD: GitHub Actions/GitlabCI
* Redefined default User model (main.models.py)
* MailHog, Jaeger, RabbitMQ integrations
* Multi-stage build for prod versions
* PostgreSql Backup
* Sentry

### How to use:

#### Clone the repo or click "Use this template" button:

    git clone https://github.com/Mikhail-Gorelov/django-blog.git


#### Before running add your superuser email/password and project name in docker/prod/env/.data.env file

    SUPERUSER_EMAIL=example@email.com
    SUPERUSER_PASSWORD=secretp@ssword
    MICROSERVICE_TITLE=MyProject

#### Run the local develop server:

    docker-compose up -d --build
    docker-compose logs -f

##### Server will bind 8000 port. You can get access to server by browser [http://localhost:8000](http://localhost:8000)

Run django commands through exec:
```shell
docker-compose exec blog python manage.py makemigrations

docker-compose exec blog python manage.py shell
```

##### For testing mail backend you can use MailHog service
    docker-compose -f docker-compose.yml -f docker/modules/mailhog.yml up -d --build

<b>Don't forget to set SMTP mail backend in settings</b>


### Production environment

If your server under LoadBalancer with SSL/TLS certificate you could run simple `prod.yml` configuration

    docker-compose -f prod.yml up -d --build


#### For set https connection you should have a domain name
<b> In prod.certbot.yml: </b>

Change the envs:
CERTBOT_EMAIL: your real email
ENVSUBST_VARS: list of variables which set in nginx.conf files
APP: value of the variable from list ENVSUBST_VARS

To set https for 2 and more nginx servers:

    ENVSUBST_VARS: API UI
    API: api.domain.com
    UI: domain.com

Run command:

    docker-compose -f prod.yml -f prod.certbot.yml up -d --build

### Sentry

Sentry's Python SDK enables automatic reporting of errors and performance data in your application.
Setup in the project and register in senty.io to watch services performance and errors.
