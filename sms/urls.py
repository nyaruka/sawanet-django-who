from django.conf.urls.defaults import *
from .views import receive

urlpatterns = patterns('',
     (r'^receive$', receive))
