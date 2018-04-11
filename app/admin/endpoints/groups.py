# -*- coding: utf-8 -*-

from flask import request, current_app
from flask_restplus import Namespace, Resource, abort
from .. import auth
from ..serializers.groups import group_container, group_post_model, group_model, group_patch_model, group_full_model, \
    group_supply_model
from app.models import Project, Group, Student, Campus
from utils.iota import generate_seed, make_transfer

ns = Namespace('groups', description='Groups related operation')


# ================================================================================================
# ENDPOINTS
# ================================================================================================
#
#   API groups endpoints
#
# ================================================================================================


@ns.route('/')
class GroupCollection(Resource):
    decorators = [auth.login_required]

    @ns.marshal_with(group_container)
    def get(self):
        """
        Return groups
        """
        return {'groups': [gr for gr in Group.objects]}

    @ns.marshal_with(group_full_model)
    @ns.expect(group_post_model)
    def post(self):
        """
        Add group
        """
        data = request.json

        p = Project.objects.get_or_404(id=data['project'])
        if Group.objects(project=p, name=data['name']).count() > 0:
            abort(400, error='Name already exist')

        gr = Group(
            project=p,
            name=data['name'],
            seed=generate_seed()
        )

        d = gr.deposit_address
        gr.save()

        return gr


@ns.route('/<id>')
class GroupItem(Resource):
    decorators = [auth.login_required]

    @ns.marshal_with(group_full_model)
    def get(self, id):
        """
        Return group
        """
        gr = Group.objects.get_or_404(id=id)

        return gr

    @ns.response(204, 'Group successfully patched')
    @ns.expect(group_patch_model)
    def patch(self, id):
        """
        Patch group
        """
        data = request.json
        if len(data) == 0:
            abort(400, error='No data')

        gr = Group.objects.get_or_404(id=id)

        gs = Group.objects(project=gr.project, name=data['name']).first()

        if gs is not None and gs.id != gr.id:
            abort(400, error='Name already exist')

        gr.name = data['name']
        gr.save()

        return 'Group successfully patched', 204

    @ns.response(204, 'Group successfully deleted')
    def delete(self, id):
        """
        Delete group
        """
        gr = Group.objects.get_or_404(id=id)

        gr.delete()

        return 'Group successfully deleted', 204


@ns.route('/<id>/supply')
@ns.response(404, 'Group not found')
class GroupItemSupply(Resource):
    decorators = [auth.login_required]

    @ns.response(204, 'Group successfully supply')
    @ns.expect(group_supply_model)
    def post(self, id):
        """
        Supply account
        """
        data = request.json
        gr = Group.objects.get_or_404(id=id)
        c = Campus.objects.get_or_404(id=data['campus'])

        if gr.project.campus.id != c.id:
            abort(400, error='Not authorized')

        if c.balance < data['value']:
            abort(400, error='Insufficient funds')

        make_transfer(current_app.config['IOTA_HOST'], {
            'recipient_address': gr.deposit_address.address,
            'message': 'From EPSI',
            'tag': 'SUPPLYGROUP',
            'value': data['value'],
            'seed': c.seed,
            'deposit_address': c.deposit_address.address
        })

        return 'Group successfully supply', 204


@ns.route('/<id>/students/<sid>')
@ns.response(404, 'Group not found')
class GroupItemStudent(Resource):
    decorators = [auth.login_required]

    @ns.response(204, 'Student successfully added')
    def post(self, id, sid):
        """
        Add student
        """
        gr = Group.objects.get_or_404(id=id)
        s = Student.objects.get_or_404(id=sid)

        if gr.project.campus.id != s.campus.id:
            abort(400, error='Not authorized')

        if s in gr.students:
            abort(400, error='Student already exist')

        gr.students.append(s)
        gr.save()

        return 'Student successfully added', 204

    @ns.response(204, 'Student successfully removed')
    def delete(self, id, sid):
        """
        Remove student
        """
        gr = Group.objects.get_or_404(id=id)
        s = Student.objects.get_or_404(id=sid)

        if gr.project.campus.id != s.campus.id:
            abort(400, error='Not authorized')

        if s not in gr.students:
            abort(400, error='Student not exist in group')

        gr.students.remove(s)

        gr.save()

        return 'Student successfully removed', 204
