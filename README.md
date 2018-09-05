# Hiccup Server

Hiccup is intended to help Fairphone to assess the stability of the Fairphones in the field.
The Server side consists of two django projects: crashreports and crashreports_stats.  The former
implements the API endpoints for collecting crash reports, while the later implements the
front-end and some endpoints to access statics.

## Setup

Python 3.6 is the only supported python version for the server code. Use this
version for development. It is the default version in Ubuntu 18.04, if you
run another OS, it is still possible to get python 3.6 (see for example
https://askubuntu.com/a/865569).

Make sure you have installed `python3`, `virtualenv` and `libffi-dev`.

    $ sudo apt install python3 virtualenv libffi-dev

Clone Hiccup server and install it locally:

    $ git clone ssh://$USER@review.fairphone.software:29418/tools/hiccup/hiccup-server
    $ cd hiccup-server
    $ virtualenv -p python3.6 .venv/hiccupenv
    $ source .venv/hiccupenv/bin/activate
    (hiccupenv) $ pip install -r requirements.txt

When using a virtualenv with pyenv (e.g. to get python3.6 on Ubuntu 16.04),
the python executable needs to be explicitly named to make tox work (see
https://github.com/pyenv/pyenv-virtualenv/issues/202#issuecomment-284728205).

    pyenv virtualenv -p python3.6 <installed-python-version> hiccupenv

i.e., because I have compiled python 3.6.6:

    pyenv virtualenv -p python3.6 3.6.6 hiccupenv

#### Setting up PostgreSQL Server

The Hiccup server relies on a PostgreSQL database.

To set up a database server, you can install the following package:

    (hiccupenv) $ sudo apt install postgresql

Then create a user and database:

    (hiccupenv) $ sudo service postgresql start
    (hiccupenv) $ sudo -u postgres createuser $USER --createdb
    (hiccupenv) $ sudo -u postgres createdb -O $USER $USER

The settings for accessing the PostgreSQL server can be found in
`hiccup/settings.py` (see the `DATABASES` setting). When both the postgresql
server and the Hiccup server are running on the same machine and you are
using the same user that you used for creating the database for running the
server, the default settings should be fine. For all other cases a
`local_settings.py` file can be created in the project root directory to
overwrite the default settings.

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

### Coding Style

We follow the
[Google Python Style Guide](https://github.com/google/styleguide/blob/gh-pages/pyguide.md).

### Setup

We use tox to both test and validate the code quality:

    (hiccupenv) $ pip install -r requirements-dev.txt

#### Testing

Simply run `tox` to test your changes in the supported environments:

    (hiccupenv) $ tox

To get an overview of the test coverage run:

    (hiccupenv) $ tox -e coverage

To generate HTML coverage reports (saved to `htmlcov/`):

     (hiccupenv) $ tox -e coverage-html

#### Linters and Formatters

To run flake8 on only the diff with upstream:

    (hiccupenv) $ git diff origin/master ./**/*py | flake8 --diff

We use the [black formatter](https://github.com/ambv/black) to check the
format of the code. To format a single file in place run:

    (hiccupenv) $ black file.py

To run the formatter over all python files run:

    (hiccupenv) $ git ls-files '*.py' | xargs black

Before committing a patchset, you are kindly asked to run the linting tools
([flake8](http://flake8.pycqa.org/en/latest/) and
[pylint](https://pylint.readthedocs.io/en/latest/))
and format the code. For both linters and formatter, git pre-commit hooks
can be set up. To activate, copy the pre-commit script that calls all
scripts in `tools/hooks/pre-commit.d` to the `.git/hooks`
folder and make it executable:

    (hiccupenv) $ cp tools/hooks/pre-commit .git/hooks/pre-commit
    (hiccupenv) $ chmod +x .git/hooks/pre-commit

To prevent commits when the flake8 check fails the *strict* option can be
set to true:

    (hiccupenv) $ git config --bool flake8.strict true

There is also a lint check included with tox (`tox -e linters`) but it is very
noisy at the moment since the codebase is not clean yet. Since you are already
validating the changes you are making with the git pre-commit hook, you are
all set to submit your change.


### Branching structure

The `production` branch reflects the codebase currently running on the production server. New
changes should be pushed for review to the `master` branch. Every version that is merged into the
`master` branch has to be buildable. From there they can be merged into the `production` branch to
integrate the changes in the running server.
