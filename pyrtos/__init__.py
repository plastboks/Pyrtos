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
    groupfinder,
    can_i,
)
from pyrtos.models.meta import (
    DBSession,
    Base,
)


def main(global_config, **settings):
    engine = engine_from_config(settings, 'sqlalchemy.')
    DBSession.configure(bind=engine)
    Base.metadata.bind = engine
    
    authenPol = AuthTktAuthenticationPolicy('somesecret',
                                            callback=groupfinder,
                                            hashalg='sha512')
    authorPol = ACLAuthorizationPolicy()
    sess_factory = UnencryptedCookieSessionFactoryConfig('someothersecret')

    config = Configurator(settings=settings,
                          authentication_policy=authenPol,
                          authorization_policy=authorPol,
                          root_factory='pyrtos.security.EntryFactory',
                          session_factory=sess_factory,)


    config.add_static_view('static', 'static', cache_max_age=3600)
    config.add_request_method(can_i, 'can_i')
  
    # index
    config.add_route('index', '/')

    # auth
    config.add_route('login', '/login')
    config.add_route('logout', '/logout')

    # category
    config.add_route('categories', '/categories')
    config.add_route('categories_private', '/categories/private')
    config.add_route('categories_archived', '/categories/archived')
    config.add_route('category_new', '/category/new')
    config.add_route('category_edit', '/category/edit/{id}')
    config.add_route('category_archive', '/category/archive/{id}')
    config.add_route('category_restore', '/category/restore/{id}')
    
    # tag
    config.add_route('tags', '/tags')

    # user
    config.add_route('users', '/users')
    config.add_route('users_archived', '/users/archived')
    config.add_route('user_new', '/user/new')
    config.add_route('user_edit', '/user/edit/{id}')
    config.add_route('user_archive', '/user/archive/{id}')
    config.add_route('user_restore', '/user/restore/{id}')

    # creditor
    config.add_route('creditors', '/creditors')
    config.add_route('creditors_private', '/creditors/private')
    config.add_route('creditors_archived', '/creditors/archived')
    config.add_route('creditor_new', '/creditor/new')
    config.add_route('creditor_edit', '/creditor/edit/{id}')
    config.add_route('creditor_archive', '/creditor/archive/{id}')
    config.add_route('creditor_restore', '/creditor/restore/{id}')

    # income
    config.add_route('incomes', '/incomes')
    config.add_route('incomes_archived', '/incomes/archived')
    config.add_route('income_new', '/income/new')
    config.add_route('income_edit', '/income/edit/{id}')
    config.add_route('income_archive', '/income/archive/{id}')
    config.add_route('income_restore', '/income/restore/{id}')

    # expenditure
    config.add_route('expenditures', '/expenditures')
    config.add_route('expenditures_private', '/expenditures/private')
    config.add_route('expenditures_archived', '/expenditures/archived')
    config.add_route('expenditure_new', '/expenditure/new')
    config.add_route('expenditure_edit', '/expenditure/edit/{id}')
    config.add_route('expenditure_archive', '/expenditure/archive/{id}')
    config.add_route('expenditure_restore', '/expenditure/restore/{id}')

    # invoice
    config.add_route('invoices', '/invoices')
    config.add_route('invoices_private', '/invoices/private')
    config.add_route('invoices_archived', '/invoices/archived')
    config.add_route('invoices_search', '/invoices/search')
    config.add_route('invoice_new', '/invoice/new')
    config.add_route('invoice_edit', '/invoice/edit/{id}')
    config.add_route('invoice_quickpay', '/invoice/quickpay/{id}')
    config.add_route('invoice_archive', '/invoice/archive/{id}')
    config.add_route('invoice_restore', '/invoice/restore/{id}')

    config.scan()
    return config.make_wsgi_app()

