from otree.api import Currency as c, currency_range
from . import models
from ._builtin import Page, WaitPage
from .models import Constants
# from datetime import datetime
import time
import datetime
import json
from django_celery_beat.models import PeriodicTask, PeriodicTasks, IntervalSchedule

class Auction(Page):

    def is_displayed(self):
        schedule, created = IntervalSchedule.objects.get_or_create(
             every=2,
             period=IntervalSchedule.SECONDS,
        )
        ppp10, created = PeriodicTask.objects.get_or_create(
                                    name='price_increase_p_{}'.format(self.player.pk),
                                    defaults={'interval': schedule,
                                              'task': 'ebay.tasks.price_increase',
                                              'args': json.dumps([self.group.pk])},
                                 )
        if not created:
            ppp10.args = json.dumps([self.player.pk])
        ppp10.enabled = True
        ppp10.save()
        return True

    def vars_for_template(self):
        ...        # return {'time_left': self.group.time_left()}

    def before_next_page(self):
        schedule, created = IntervalSchedule.objects.get_or_create(
             every=2,
             period=IntervalSchedule.SECONDS,
        )
        ppp10, created = PeriodicTask.objects.get_or_create(
                                    name='price_increase_p_{}'.format(self.player.pk),
                                    defaults={'interval': schedule,
                                              'task': 'ebay.tasks.price_increase',
                                              'args': json.dumps([self.player.pk])},
                                 )
        ppp10.enabled = False
        ppp10.save()


class Results(Page):
    ...


page_sequence = [
    Auction,
    Results
]
