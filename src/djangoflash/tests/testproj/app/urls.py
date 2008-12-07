from django.conf.urls.defaults import *

from testproj.app import views

urlpatterns = patterns('',
    (r'^invalid-flash/$', views.invalid_flash),
    (r'^flash-early-access/$', views.flash_early_access),
    (r'^variable-lifecycle/$', views.variable_lifecycle),
    (r'^several-variable-lifecycle/$', views.several_variables_lifecycle),
    (r'^now/$', views.now),
    (r'^dict-syntax/$', views.dict_syntax),
    (r'^keep-variables/$', views.keep_variables),
    (r'^keep-invalid-variables/$', views.keep_invalid_variables),
    (r'^keep-all-variables/$', views.keep_all_variables),
    (r'^default/$', views.render_template),
)
