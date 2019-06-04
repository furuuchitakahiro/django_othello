#!/bin/sh

cd othello

/bin/echo -e '\e[1;32mInstall super user data\e[0m'
python manage.py loaddata ./othello_users/fixtures/dev_superuser_initial_data.json
/bin/echo -e '\e[1;32mInstall fixtures data\e[0m'
python manage.py loaddata dev_initial_data.json
