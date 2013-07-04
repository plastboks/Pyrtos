from pyramid.config import Configurator
from sqlalchemy import engine_from_config
from pyramid.authentication import (
    AuthTktAuthenticationPolicy,
)
from pyramid.authorization import (
    ACLAuthorizationPolicy,
)
from pyramid.session import (
    UnencryptedCookieSessionFactoryConfig,
)

from pyrtos.security import (
    EntryFactory,
)
from pyrtos.models.meta import (
    DBSession,
    Base,
)


def main(global_config, **settings):
    engine = engine_from_config(settings, 'sqlalchemy.')
    DBSession.configure(bind=engine)
    Base.metadata.bind = engine
    
    authenPol = AuthTktAuthenticationPolicy('somesecret')
    authorPol = ACLAuthorizationPolicy()
    sess_factory = UnencryptedCookieSessionFactoryConfig('someothersecret')

    config = Configurator(settings=settings,
                          authentication_policy=authenPol,
                          authorization_policy=authorPol,
                          root_factory='pyrtos.security.EntryFactory',
                          session_factory=sess_factory,)


    config.add_static_view('static', 'static', cache_max_age=3600)
  
    # index
    config.add_route('index', '/')

    # auth
    config.add_route('login', '/login')
    config.add_route('logout', '/logout')

    # category
    config.add_route('categories', '/categories')
    config.add_route('categories_archived', '/categories/archived')
    config.add_route('category_new', '/category/new')
    config.add_route('category_edit', '/category/edit/{id}')
    config.add_route('category_delete', '/category/delete/{id}')
    config.add_route('category_restore', '/category/restore/{id}')
    
    # tag
    config.add_route('tags', '/tags')

    # user
    config.add_route('users', '/users')

    config.scan()
    return config.make_wsgi_app()

