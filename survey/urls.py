from django.conf.urls import patterns, include, url

urlpatterns = patterns('survey.views',
    url(r'^$', 'index'),
    url(r'^register/$', 'register'),
    url(r'^register_success/$', 'register_success'),
    url(r'^login_page/$', 'login_page'),
    url(r'^logging_in/$', 'logging_in'),
    url(r'^login_success/$', 'login_success'),
    url(r'^logout_view/$', 'logout_view'),
    url(r'^logout_success/$', 'logout_success'),
    url(r'^paper_creator/$', 'paper_creator'),
    url(r'^(?P<surveypaper_id>\d+)/$', 'detail'),
    url(r'^(?P<surveypaper_id>\d+)/results/$', 'results'),
    url(r'^(?P<surveypaper_id>\d+)/vote/$', 'vote'),
    url(r'^(?P<surveypaper_id>\d+)/created_success/$', 'created_success'),
    url(r'^(?P<surveypaper_id>\d+)/add_question/$', 'add_question'),
)
