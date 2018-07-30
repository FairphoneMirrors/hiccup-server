# Hiccup Server

Hiccup is intended to help Fairphone to assess the stability of the Fairphones in the field.
The Server side consists of two django projects: crashreports and crashreports_stats.  The former
implements the API endpoints for collecting crash reports, while the later implements the
front-end and some endpoints to access statics.

## Setup

Make sure you have installed `python3`, `virtualenv` and `libffi-dev`.

    $ sudo apt install python3 virtualenv libffi-dev

Clone Hiccup server and install it locally:

    $ git clone ssh://$USER@review.fairphone.software:29418/tools/hiccup/hiccup-server
    $ cd hiccup-server
    $ virtualenv -p python3 .venv/hiccupenv
    $ source .venv/hiccupenv/bin/activate
    (hiccupenv) $ pip install -r requirements.txt

By default Django will use a SQLite3 database (`db.sqlite3` in the base directory).

#### Using PostgreSQL Server

To use a PostgreSQL database (like the production server is running), you can install the following
packages:

    (hiccupenv) $ sudo apt install postgresql
    (hiccupenv) $ pip install psycopg2

Then create a user and database:

    (hiccupenv) $ sudo service postgresql start
    (hiccupenv) $ sudo -u postgres createuser $USER --createdb
    (hiccupenv) $ sudo -u postgres createdb -O $USER $USER



Copy the following to `local_settings.py` (create the file if it did not exist before) to use the
PostgreSQL database instread of SQLite:

    import os

    DATABASES = {
      'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': os.environ.get('USER'),
        'USER': os.environ.get('USER'),
        'PORT': '',
      }
    }


Test that the configuration is correct:

    (hiccupenv) $ python manage.py test

See the end of the next section to add a super-user.


### Run Hiccup server

The first time you run the server, the database will be empty and the model migrations have yet to
happen:

    (hiccupenv) $ python manage.py migrate

Then, at any later point, start the local server:

    (hiccupenv) $ python manage.py runserver
    ...
    Starting development server at http://127.0.0.1:8000/
    ...

The API is available at `localhost:8000/hiccup/` and the web-front-end at
`localhost:8000/hiccup_stats/`.

The Django admin web-front-end is at `localhost:8000/hiccup/admin`.

If you plan to browse through the Django admin web-front-end (`localhost:8000/hiccup/admin`), you
will need a super-user (admin) account:

    (hiccupenv) $ python manage.py createsuperuser
    ...
    Superuser created successfully.

To browse  through the Hiccup front-end (`localhost:8000/hiccup_stats/`), the account you will
identify with should belong to the group `FairphoneSoftwareTeam`.

Run the following command or perform the manual steps below:

    python manage.py shell -c "
        from django.contrib.auth.models import Group, User
        admin = User.objects.get(username='admin')
        stats_group = Group.objects.create(name='FairphoneSoftwareTeam')
        stats_group.user_set.add(admin)
        "

* You need a running server and a super-user account;
* Head to `http://localhost:8000/hiccup/admin/auth/group/`;
* Create a new group named `FairphoneSoftwareTeam`;
* Go back to the user list at `http://localhost:8000/hiccup/admin/auth/user/` and add your
  super-user to the new group.

## API Documentation

The Hiccup REST API documentation is created automatically using
[drf_yasg](https://github.com/axnsan12/drf-yasg) and
[swagger2markup](https://github.com/Swagger2Markup/swagger2markup).

It can be generated using tox:

    (hiccupenv) $ tox -e docs

The generated documentation file can be found under
`documentation/api-endpoints.md`.

It is also possible to create an HTML version of the docs. Make sure you
have asciidoctor installed:

    (hiccupenv) $ sudo apt install asciidoctor

Then generate the html docs using tox:

    (hiccupenv) $ tox -e docs-html

The generated documentation file can be found under
`documentation/api-endpoints.html`.


## Development

### Setup

We use tox to both test and validate the code quality:

    (hiccupenv) $ pip install -r requirements-dev.txt

Simply run `tox` to test your changes in the supported environments:

    (hiccupenv) $ tox

Before committing a patchset, you are kindly asked to run the linting tools.
The flake8 tool can be run automatically for you with a (strict) git
pre-commit hook:

    (hiccupenv) $ flake8 --install-hook git
    (hiccupenv) $ git config --bool flake8.strict true

Also, running flake8 on only the diff with upstream:

    (hiccupenv) $ git diff origin/master ./**/*py | flake8 --diff

There is also a lint check included with tox (`tox -e linters`) but it is very
noisy at the moment since the codebase is not clean yet. Since you are already
validating the changes you are making with the git pre-commit hook, you are
all set to submit your change.


### Branching structure

The `production` branch reflects the codebase currently running on the production server. New
changes should be pushed for review to the `master` branch. Every version that is merged into the
`master` branch has to be buildable. From there they can be merged into the `production` branch to
integrate the changes in the running server.
