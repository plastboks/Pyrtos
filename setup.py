import os

from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))
README = open(os.path.join(here, 'readme.md')).read()
CHANGES = open(os.path.join(here, 'changes.md')).read()

requires = [
    'pyramid',
    'SQLAlchemy',
    'transaction',
    'pyramid_tm',
    'pyramid_debugtoolbar',
    'pyramid_mailer',
    'zope.sqlalchemy',
    'waitress',
    'alembic',
    'cryptacular',
    'wtforms',
    'webhelpers',
    'webtest',
    'nose',
    'coverage',
    'slugify',
    'pep8',
    'python-hoiio',
    #'hoiio',
    'Celery',
    ]

setup(name='pyrtos',
      version='0.0.6',
      description='pyrtos',
      long_description=README + '\n\n' + CHANGES,
      classifiers=[
        "Programming Language :: Python",
        "Framework :: Pyramid",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Internet :: WWW/HTTP :: WSGI :: Application",
        ],
      author='Alexander Skjolden',
      author_email='alex@plastboks.net',
      url='https://github.com/plastboks',
      keywords='web wsgi bfg pylons pyramid',
      packages=find_packages(),
      include_package_data=True,
      zip_safe=False,
      test_suite='pyrtos',
      install_requires=requires,
      entry_points="""\
      [paste.app_factory]
      main = pyrtos:main
      [console_scripts]
      initialize_pyrtos_db = pyrtos.scripts.initializedb:main
      """,
      )
