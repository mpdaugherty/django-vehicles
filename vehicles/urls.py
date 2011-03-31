"""
URLconf for web services to get the makes and models available in particular years.
"""
from django.conf.urls.defaults import *
from vehicles.views import makes_for_year, models_for_make_and_year

urlpatterns = patterns('',
                       url(r'^(?P<year>\d\d\d\d)/makes$',
                           makes_for_year,
                           name='vehicles_makes_in_year'),
                       url(r'^(?P<year>\d\d\d\d)/(?P<make>.+)/models$',
                           models_for_make_and_year,
                           name='vehicles_models_for_make_in_year'),
                       )
