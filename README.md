# a prototype to build an auction with n-seconds update of a price

Filipp Chapkovski, University of Zurich

---

The general task: to make an auction where the price for the group is updated
each n seconds (in our case each 2 seconds).

This is a ___***prototype***___ - it works but some crucial parts are missing.
What is missing are channels (websockets), to update the price shown to the
final users so they can leave the auction when they want to.

You can see how to implement it in other examples.
like here: https://github.com/chapkovski/for-max-upd-ebay-second-price
or here: https://github.com/chapkovski/miniebay
(a working app for an example above is here: https://mini-ebay-otree.herokuapp.com/)

To update the price at the server side at the regular basis we need to use
periodic tasks (http://docs.celeryproject.org/en/latest/userguide/periodic-tasks.html)

So we need a separate process (called Celery beat) that will look regulary in our
database, in the data table with periodic tasks, and if there are any, it would run
it every n seconds.

If somebody would change the database adding more periodic tasks or deleting/deactivating
existing ones, the Beat process would adjust its behaviour.

It makes the situation a bit complicated. In the development (locally), oTree needs only
one process to run: you start it in a terminal by running `otree runserver` command.

In a production (for example when you deploy it to Heroku), you need one more process,
which is responsible for timeouts (it is called Huey).

Additionaly in production you need also a tool to via which this timeout process will communicate
with your database and oTree process (it is called Redis, and if you deploy your app to Heroku
you need to add it as an addon).

In our case however we need **TWO** more processes. One is celery worker that will
go through our database changing the price at a group level.
and another is a celery beat that will tell to a celery worker to do something every 2 seconds.

so, if you'd like to run this app locally and see how it works, you need:

``` bash
pip install git+git://github.com/HealthTechDevelopers/celery@master#celery
pip install django_celery_beat
```
(you need to install celery from the git rip instead of `pip install celery` because
of the weird error in Celery 4 that does not allow to dynamically update _Periodic Task_ table).
and you also need to add them in `settings.py` in a section `INSTALLED_APPS`.

when they are installed you need to run two separete processes (in two different terminals):

```
celery --app=ebay worker --loglevel=info
celery --app=ebay beat --loglevel=info -S django
```

when the session starts it deletes all the items from the _Periodic Task_ table
(not the most elegant solution, so think about something more smart when you do it with the real app).

then as soon as the guy reaches the `Auction` page it adds a periodic task that run a function
`price_increase` from `tasks.py` every 2 seconds.
As soon as the guy leaves the page, it deactivates the task (otherwise the price keeps on increasing endlessly
until you stop the beat process).

Of course, in a real life app you need to add the periodic task in the waiting page so
it would start when all the players in a group arrive at the Auction page, and it would stop
as soon as the last player leaves the page, but that's easy to do.


So if you start this app, start the processes, and you'll navigate to the Auction page,
you will see in the admin - data page, that the price keeps growing every 2 seconds.

The only thing you need to do is to add the channels: each time the price is changed, the
message should be pushed via channels so the players can see the price update.
