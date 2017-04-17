from __future__ import absolute_import, unicode_literals
from .celery import app
from .models import Constants, Player, Group
# app = Celery(broker='redis://localhost:6379/0')



@app.task
def price_increase(group_pk):
    print('########I am changing group {} price'.format(group_pk))
    curgroup = Group.objects.get(pk=group_pk)
    curgroup.price += 1
    curgroup.save()
    # return x + y


@app.task
def test(arg):
    print('YOUR ARG WAS::: {}'.format(arg))
    
