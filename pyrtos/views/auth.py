from pyramid.response import Response
from sqlalchemy.exc import DBAPIError

from pyramid.httpexceptions import (
    HTTPNotFound,
    HTTPFound,
)
from pyramid.security import (
    remember,
    forget,
    authenticated_userid
)
from pyramid.view import (
    view_config,
)
from pyrtos.models import (
    User,
)
from pyrtos.forms import (
    LoginForm,
)

class AuthViews(object):

  def __init__(self,request):
      self.request = request

  @view_config(route_name='login',
               renderer='pyrtos:templates/login.mako')
  def login(self):
      form = LoginForm(self.request.POST, csrf_context=self.request.session)
      if self.request.method == 'POST' and form.validate():
          user = User.by_email(self.request.POST.get('email'))
          if user\
          and user.verify_password(self.request.POST.get('password'))\
          and user.blocked is not True\
          and user.archived is not True:
              headers = remember(self.request, user.id)
              self.request.session.flash('Welcome back %s' % (user.email), 'success')
              return HTTPFound(location=self.request.route_url('index'),
                               headers=headers)
          headers = forget(self.request)
          self.request.session.flash('Login failed', 'error')
          return {'title' : 'Login',
                  'form' : form}
      if authenticated_userid(self.request):
          self.request.session.flash('You are already logged in', 'status')
          return HTTPFound(location=self.request.route_url('index'))

      return {'title' : 'Login',
              'form' : form}

  @view_config(route_name='logout',
               renderer='string')
  def logout(self):
      headers = forget(self.request)
      return HTTPFound(location=self.request.route_url('login'),
                       headers=headers)

