# -*- coding: utf-8 -*-

from runserver import app

with app.test_request_context():
    from app.models import User, Campus

    if Campus.objects(name='Arras').count() == 0:
        c = Campus(name='Arras')
        c.save()

    else:
        c = Campus.objects(name='Arras').first()

    if User.objects(username='averdier').count() == 0:
        u = User(
            campus=c,
            username='averdier',
            type='admin'
        )
        u.secret = 'averdier'
        u.save()

    print('db created.')
