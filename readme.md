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
  * Upload and keep track of reciepts.
  * Upload and keep track of documents.
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
  * `alembic revision --autogenerate -m "comment"`
  * `alembic upgrade head`

Testing
=======
This app will be written with TDD. To test the app run:
  * `nosetest .`

Branches
========
There will mainly be two branches in this repo (@github) at all times. The master and develop branch.
The master branch will be kept back featurewise of the develop branch. This is to ensure the stability of the master branch.

Useful Links
============
  * [Testing page in wiki2 tutorial](http://docs.pylonsproject.org/projects/pyramid/en/1.4-branch/tutorials/wiki2/tests.html)

