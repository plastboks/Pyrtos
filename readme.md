PyrTos
======
Pyr(amid)(Plou)Tos Household Organizer for keeping track of expenditures, income, invoices and many more.

Pyramid
=======
This application is based on the [Pyramid Python Webframework](http://www.pylonsproject.org/)

Description
===========
Features include:
  * Global categories for use trough the application.
  * Global creditors of invoices an such.
  * Register all expected monthly and yearly expenditures.
  * Upload and register all uses and invoices.
  * All entries have tags in addition to one category.
  * Notify via SMS and Email when an invoice is due to payment.
  * Compare uses against expected numbers.
  * Plot and graphs to visualize budget.
  * Upload and keep track of receipts and documents.
  * +++

Installation
============
  * create a virtualenv (eg: `virtualenv2 venv`). Use Python2.X
  * activate virtualenv `. venv/bin/activate`
  * clone this repository into venv directory (eg: venv/Pyrtos).
  * run `pip install -e .` inside Pyrtos directory.
  * run `initialize_pyrtos_db .ini`
  * run `pserve development.ini`

Package updates
===============
* run: `pip install --upgrade -e .`

Docker
======
Now with a docker automated build. See [the registry](https://registry.hub.docker.com/u/plastboks/pyrtos/) for details.
* change directory into `./docker`
* run: `build` (need superuser)
* run: `debug` or `daemon` (need superuser)

Deploy
======
  * see `example/pyrtos.nginx.example` for nginx example config file.
  * setup and configure nginx.
  * start pserve `../bin/gunicorn --paste production.ini`.
  * restart nginx.

Alembic
=======
To create an alembic migrations do;
  * edit pyramarks/models.py accordingly
  * run `alembic revision --autogenerate -m "migration comment"`
  * run `alembic upgrade head`

Upgrading
=========
While the project is still under development, alembic migrations will not be used to any extent.
Upgrading is done by nuking the database and reconstruction it with `initialize_pyrtos_db .ini`,
this can be as frequent as from one commit to another.

When the project has come out of main development, alembic migrations is done by:
  * run `alembic upgrade head`

Testing
=======
This app will be written with TDD. To test the app run:
  * run `nosetests .`

Branches
========
There will mainly be two branches in this repository (@github) at all times. The master and develop branch.
The master branch will be kept back feature wise of the develop branch. This is to ensure the stability of the master branch.

Useful Links
============
  * [Testing page in wiki2 tutorial](http://docs.pylonsproject.org/projects/pyramid/en/1.4-branch/tutorials/wiki2/tests.html)
  * [Sonteks tests for Pyramid and SQLAlchemy](http://sontek.net/blog/detail/writing-tests-for-pyramid-and-sqlalchemy)
  * [Outgrowing Pyramid Handlers](http://michael.merickel.org/2011/8/23/outgrowing-pyramid-handlers/)

License
=======
The Pyramid framework code is licensed under a BSD-style [PSFL](http://www.pylonsproject.org/about/license) license.
All Pyrtos code is licensed under a BSD-style [PSFL](http://en.wikipedia.org/wiki/Python_Software_Foundation_License) license.

Credits
=======
  * [Pyramid framework](http://www.pylonsproject.org/)
  * [WTForms](http://wtforms.simplecodes.com/docs/1.0.4/)
  * [SQLAlchemy](http://www.sqlalchemy.org/)
  * Icon set from [FAMFAMFAM](http://www.famfamfam.com)
