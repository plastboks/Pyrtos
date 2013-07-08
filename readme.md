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
  * Register all expected montly and yearly expenditures.
  * Upload and register all uses and invoices.
  * All entries have tags in addition to one category.
  * Notify via SMS and Email when an invoice is due to payment.
  * Compare uses against expected numbers.
  * Plot and graphs to visualize budget.
  * Upload and keep track of reciepts and documents.
  * +++


Installation
============
  * create a virtualenv (eg: `virtualenv2 venv`). Use Python2.X
  * activate virtualenv `. venv/bin/activate`
  * clone this repo into venv directory (eg: venv/Pyrtos)
  * run `pip install -e .` inside Pyrtos directory
  * run `initialize_pyrtos_db development.ini`
  * run `pserve development.ini`

Alembic
=======
Alembic upgrades and migrations is done by:
  * edit pyramarks/models.py accordingly
  * run `alembic revision --autogenerate -m "migration comment"`
  * run `alembic upgrade head`

Upgrading
=========
While the project is in the initial state, there will be no fancy upgrading. Until then, upgrades will be done by:
  * run `pip install -e .`
  * run `alembic upgrade head`

Testing
=======
This app will be written with TDD. To test the app run:
  * run `nosetests .`

Branches
========
There will mainly be two branches in this repo (@github) at all times. The master and develop branch.
The master branch will be kept back featurewise of the develop branch. This is to ensure the stability of the master branch.

Useful Links
============
  * [Testing page in wiki2 tutorial](http://docs.pylonsproject.org/projects/pyramid/en/1.4-branch/tutorials/wiki2/tests.html)
  * [Sonteks tests for Pyramid and SQLAlchemy](http://sontek.net/blog/detail/writing-tests-for-pyramid-and-sqlalchemy)
  * [Outgrowing Pyramid Handlers](http://michael.merickel.org/2011/8/23/outgrowing-pyramid-handlers/)

License
=======
The Pyramid framework code is licensed under a BSD-style [PSFL](http://www.pylonsprojecct.org/about/license) license.
All Pyrtos code is licensed under a BSD-style [PSFL](http://www.pylonsprojecct.org/about/license) license.

Credits
=======
  * Icon set from [FAMFAMFAM](http://www.famfamfam.com)

