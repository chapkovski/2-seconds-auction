# urls.py
from django.conf.urls import include, url
from django.contrib import admin
from otree.urls import urlpatterns
# urlpatterns = [
#
# ]


# urls.py
# from django.conf.urls import url


urlpatterns.append(url(r'^admin/', include(admin.site.urls)),)
