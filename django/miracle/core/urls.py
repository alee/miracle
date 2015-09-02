from django.conf.urls import url
from django.views.generic import TemplateView, RedirectView

from rest_framework import routers

from . import views


urlpatterns = [
    # Examples:
    # url(r'^$', 'miracle.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^$', TemplateView.as_view(template_name='index.html'), name='home'),
    # FIXME: replace these with forms if needed
    url(r'^contact/$', RedirectView.as_view(url='https://groups.google.com/forum/#!forum/comses-dev', permanent=False),
        name='contact'),
    url(r'^report-bug/$', RedirectView.as_view(url='https://github.com/comses/miracle/issues/new', permanent=False),
        name='report_bug'),
    url(r'^dashboard/$', views.DashboardView.as_view(), name='dashboard'),
    url(r'^search/$', TemplateView.as_view(template_name='search.html'), name='search'),
    url(r'^account/profile/$', views.UserProfileView.as_view(), name='profile'),
    url(r'^file-upload/$', views.FileUploadView.as_view(), name='upload')
]

router = routers.DefaultRouter()
router.register(r'projects', views.ProjectViewSet, base_name='project')
router.register(r'datasets', views.DatasetViewSet, base_name='dataset')
urlpatterns += router.urls