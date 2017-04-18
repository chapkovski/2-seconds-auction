from __future__ import absolute_import, unicode_literals
from .celery import app
from .models import Constants, Player, Group
from celery import shared_task
import channels
import json

from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

@receiver(post_save, sender=Group)
def incident_post_save(sender, **kwargs):
    print('GROUP MODEL HAS BEEN JUST SAVED YOUPTA!:::', sender)
    channels.Channel("braintree_process").send({
        "group_pk": 'sender.pk',
        "price": 'sender.price',
    })
    # print('SENDING MESSAGE TO GROUP>>>>>>{}'.format(group_pk))

@shared_task
def price_increase(group_pk):
    print('########I am changing group {} price'.format(group_pk))
    curgroup = Group.objects.get(pk=group_pk)
    curgroup.price += 1
    curgroup.save()



@shared_task
def test(arg):
    print('YOUR ARG WAS::: {}'.format(arg))


# @app.task
# def sec3(job_id, reply_channel):
#     # time sleep represent some long running process
#     time.sleep(3)
#     # Change task status to completed
#     job = Job.objects.get(pk=job_id)
#     log.debug("Running job_name=%s", job.name)
#
#     job.status = "completed"
#     job.save()
#
#     # Send status update back to browser client
#     if reply_channel is not None:
#         Channel(reply_channel).send({
#             "text": json.dumps ({
#                 "action": "completed",
#                 "job_id": job.id,
#                 "job_name": job.name,
#                 "job_status": job.status,
#             })
#         })
