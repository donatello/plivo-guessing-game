from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
                       url(r'guess_game/$', 'guess_game.views.index'),
                       url(r'main_menu_response/$', 'guess_game.views.mm_response'),
                       url(r'how_to_play/$', 'guess_game.views.how_to_play'),
                       url(r'play_game/$', 'guess_game.views.play_game'),

    # Examples:
    # url(r'^$', 'plivo_ivrs_game.views.home', name='home'),
    # url(r'^plivo_ivrs_game/', include('plivo_ivrs_game.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)
