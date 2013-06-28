Pyrtos
======
Pyr(amid)(Plou)tos Household Organizer build on Pyramid python framework. 

Description
===========
Pyrtos is a Household organizer for keeping track of expenditures, income, invoices and many more.

Install
=======
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

