from ckan.common import OrderedDict, _, json, request, c, g, response
from ckan.controllers.package import PackageController
import ckan.logic as logic

import ckan.model as model

import ckan.lib.helpers as h
import ckan.lib.render

from genshi.template import MarkupTemplate
import ckan.lib.base as base
import ckan.lib.jsonp as jsonp
import agls_model
from sqlalchemy import func
NotFound = logic.NotFound
NotAuthorized = logic.NotAuthorized
ValidationError = logic.ValidationError


class AGLSController(PackageController):
    @jsonp.jsonpify
    def geo_autocomplete(self):
        q = request.params.get('q', '')
        limit = request.params.get('limit', 20)
        record_list = []
        if q:
            import ckan.model as model
            context = {'model': model}

            data_dict = {'q': q, 'limit': limit}

            model = context['model']

            q = data_dict['q']
            limit = data_dict.get('limit', 20)

            query = model.Session.query(agls_model.AGLS_Gazetteer).filter(agls_model.AGLS_Gazetteer.name.ilike('%'+func.lower(q)+'%'))
            query = query.limit(limit)

            for record in query.all():
                result_dict = {'name': getattr(record, 'record_id')+": "+getattr(record, 'name')}
                record_list.append(result_dict)
        return record_list

    @jsonp.jsonpify
    def geo_latlon(self):
        q = request.params.get('q', '')
        limit = request.params.get('limit', 1)
        if q:
            import ckan.model as model
            context = {'model': model}

            data_dict = {'q': q, 'limit': limit}

            model = context['model']

            q = data_dict['q']
            limit = data_dict.get('limit', 1)

            query = model.Session.query(agls_model.AGLS_Gazetteer).filter(agls_model.AGLS_Gazetteer.record_id == q)
            query = query.limit(limit)

            for record in query.all():
                result_dict = {'id': getattr(record, 'record_id'),
                               'name': getattr(record, 'record_id')+": "+getattr(record, 'name'),
                               'latitude': getattr(record, 'latitude'),
                               'longitude': getattr(record, 'longitude'),
                               'geojson': '{"type": "Point","coordinates": ['+ str(getattr(record, 'longitude'))+ ','+str(getattr(record, 'latitude'))+']}'}
                return result_dict
        return {}

    def gmd(self, id, package_type="dataset"):
        format = 'html'
        #loader = MarkupTemplate
        #if not format == 'html':
        #    ctype, extension, = \
        #        self._content_type_from_extension(format)
        #    if not ctype:
                # An unknown format, we'll carry on in case it is a
                # revision specifier and re-constitute the original id
        #        id = "%s.%s" % (id, format)
        #        ctype, format = "text/html; charset=utf-8", "html"

        #else:
        #    ctype, format = self._content_type_from_accept()

        # response.headers['Content-Type'] = ctype
        response.headers['Content-Type'] = 'application/vnd.iso.19139+xml; charset=utf-8'.encode("ISO-8859-1")
        response.headers["Content-Disposition"] = ("attachment; filename=" + id + ".xml").encode("ISO-8859-1")
        #package_type = self._get_package_type(id.split('@')[0])
        context = {'model': model, 'session': model.Session,
                   'user': c.user or c.author, 'for_view': True,
                   'auth_user_obj': c.userobj}
        data_dict = {'id': id}

        # interpret @<revision_id> or @<date> suffix
        split = id.split('@')
        if len(split) == 2:
            data_dict['id'], revision_ref = split
            if model.is_id(revision_ref):
                context['revision_id'] = revision_ref
            else:
                try:
                    date = h.date_str_to_datetime(revision_ref)
                    context['revision_date'] = date
                except TypeError, e:
                    base.abort(400, _('Invalid revision format: %r') % e.args)
                except ValueError, e:
                    base.abort(400, _('Invalid revision format: %r') % e.args)
        elif len(split) > 2:
            base.abort(400, _('Invalid revision format: %r') %
                       'Too many "@" symbols')

        # check if package exists
        # try:
        #     c.pkg_dict = logic.get_action('package_show')(context, data_dict)
        #     c.pkg = context['package']
        # except NotFound:
        #     base.abort(404, _('Dataset not found'))
        # except NotAuthorized:
        #     base.abort(401, _('Unauthorized to read package %s') % id)

        # used by disqus plugin
        #c.current_package_id = c.pkg.id
        #c.related_count = c.pkg.related_count

        #self._setup_template_variables(context, {'id': id},
        #                               package_type=package_type)
        data_dict = {'id': id}
        try:
            pkg_dict = logic.get_action("package_show")(context, data_dict)
            pkg = context["package"]
        except tk.ObjectNotFound:
            return tk.abort(404, tk._("Dataset not found"))
        except tk.NotAuthorized:
            return tk.abort(401, tk._("Unauthorized to read package %s") % id)

        # can the resources be previewed?
        for resource in pkg_dict['resources']:
            resource['can_be_previewed'] = self._resource_preview(
                {'resource': resource, 'package': pkg_dict})

        extra_vars = {"dataset_type": package_type, "pkg": pkg, "pkg_dict": pkg_dict}
        template = 'package/read.gmd'

        try:
            return base.render(template, extra_vars)
        except ckan.lib.render.TemplateNotFound:
            msg = _("Viewing {package_type} datasets in {format} format is "
                    "not supported (template file {file} not found).".format(
                package_type=package_type, format=format, file=template))
            base.abort(403, msg)

        assert False, "We should never get here"

    def resource_redefine(self, id, resource_id=None, data=None, errors=None, error_summary=None, original_action=None):
        action = getattr(super(AGLSController, self), original_action)

        if original_action == 'new_resource':
            pargs = id,
            kargs = dict(data=data, errors=errors, error_summary=error_summary)
        elif original_action == 'resource_edit':
            pargs = id, resource_id
            kargs = dict(data=data, errors=errors, error_summary=error_summary)
        elif original_action == 'resource_delete':
            pargs = id, resource_id
            kargs = dict()
        try:
            return action(*pargs, **kargs)
        except KeyError, e:
            if 'resources' in e.args:
                h.flash_error('Some mandatory dataset fields are missing. Please complete before adding a new resource')
                base.redirect(h.url_for('dataset_edit', id=id))
