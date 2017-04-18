from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c, currency_range
)
import random
import time
import datetime
import channels
from django_celery_beat.models import PeriodicTask, PeriodicTasks, IntervalSchedule
author = 'Filipp Chapkovskii, UZH, chapkovski@gmail.com'

doc = """
ebay auction example
"""


class Constants(BaseConstants):
    name_in_url = 'ebay'
    players_per_group = None
    num_rounds = 1
    # starting_time = 30
    # extra_time = 20
    endowment = 100
    prize = 200
    # num_others = players_per_group - 1


class Subsession(BaseSubsession):
    def before_session_starts(self):
         PeriodicTask.objects.all().delete()


class Group(BaseGroup):
    price = models.IntegerField(initial=0)


    def set_payoffs(self):
        ...

class Player(BasePlayer):
    ...


from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver

@receiver(pre_save)
def incident_post_save(sender, **kwargs):
    print('GROUP MODEL HAS BEEN JUST SAVED YOUPTA!:::', sender)
    channels.Channel("braintree_process").send({
        "group_pk": 'sender.pk',
        "price": 'sender.price',
    })
    print('SENDING MESSAGE TO GROUP>>>>>>{}')
