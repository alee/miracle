from django.conf.urls import url
from django.views.generic import TemplateView, RedirectView

from rest_framework.urlpatterns import format_suffix_patterns

from . import views


urlpatterns = [
    # Examples:
    # url(r'^$', 'miracle.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^$', TemplateView.as_view(template_name='index.html'), name='home'),
    # FIXME: replace these with forms if needed
    url(r'^contact$', RedirectView.as_view(url='https://groups.google.com/forum/#!forum/comses-dev', permanent=False),
        name='contact'),
    url(r'^report-bug$', RedirectView.as_view(url='https://github.com/comses/miracle/issues/new', permanent=False),
        name='report_bug'),
]

urlpatterns += format_suffix_patterns([
    url(r'^projects/?$', views.ProjectListView.as_view()),
    url(r'^projects/(?P<pk>[\d]+)/$', views.ProjectDetailView.as_view()),
])
