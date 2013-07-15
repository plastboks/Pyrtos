from datetime import datetime
from slugify import slugify
from pyramid.response import (
    Response,
    FileResponse,
)
from sqlalchemy.exc import DBAPIError

from pyramid.httpexceptions import (
    HTTPNotFound,
    HTTPFound,
    HTTPForbidden,
)
from pyramid.security import (
    remember,
    forget,
    authenticated_userid
)
from pyramid.view import (
    view_config,
)
from pyrtos.models.meta import DBSession
from pyrtos.models import (
    File,
)
from pyrtos.forms import (
    FileCreateForm,
    FileEditForm,
)

import os, shutil, hashlib

class FileViews(object):

    def __init__(self,request):
        self.request = request


    @view_config(route_name='files',
                 renderer='pyrtos:templates/file/list.mako',
                 permission='view')
    def files(self):
        page = int (self.request.params.get('page', 1))
        files = File.page(self.request, page)
        return {'paginator': files,
                'title' : 'Files',}

    @view_config(route_name='files_archived',
                 renderer='pyrtos:templates/file/list.mako',
                 permission='view')
    def files_archived(self):
        page = int(self.request.params.get('page', 1))
        files = File.page(self.request, page, archived=True)
        return {'paginator': files,
                'title' : 'Archived files',
                'archived' : True,}

    @view_config(route_name='file_new',
                 renderer='pyrtos:templates/file/edit.mako',
                 permission='create')
    def file_create(self):
        form = FileCreateForm(self.request.POST,
                                  csrf_context=self.request.session)

        if self.request.method == 'POST' and form.validate():
            f = File()
            form.populate_obj(f)
            
            if self.request.POST.get('file'):
                upload = self.request.POST.get('file')
                input_file = upload.file

                tmp_fileparts = os.path.splitext(upload.filename)
            
                final_filename = hashlib.sha1(tmp_fileparts[0])\
                                 .hexdigest()+tmp_fileparts[1]

                file_path = os.path.join('pyrtos/uploads', final_filename)
                with open(file_path, 'wb') as output_file:
                    shutil.copyfileobj(input_file, output_file)

                f.filename = final_filename
            f.user_id = authenticated_userid(self.request)
            DBSession.add(f)
            self.request.session.flash('File %s created' %\
                                            (f.title), 'success')
            return HTTPFound(location=self.request.route_url('files'))
        return {'title': 'New file',
                'form': form,
                'action': 'file_new'}

    @view_config(route_name='file_download',
                  permission='view')
    def file_download(self):
        id = int(self.request.matchdict.get('id'))
        
        f = File.by_id(id)
        if not f:
            return HTTPNotFound()
        if f.private and c.user_id is not authenticated_userid(self.request):
            return HTTPForbidden()

        if f.filename:
            response = FileResponse(
                'pyrtos/uploads/'+f.filename,
                request=self.request,
                content_type='application/pdf'
            )
            return response
        return HTTPNotFound()

