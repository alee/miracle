from django.conf import settings
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.test import TestCase
from django.test.client import RequestFactory, Client
from django.utils.http import urlencode

from ..models import (Project, Dataset, DataTable, DataTableColumn)

import logging
import os

logger = logging.getLogger(__name__)


class BaseMiracleTest(TestCase):

    """
    Base class providing common scaffolding for miracle tests
    """

    TEST_DATA_DIR = os.path.join(settings.BASE_DIR, 'miracle', 'core', 'tests', 'data')

    def setUp(self, **kwargs):
        self.client = Client()
        self.factory = RequestFactory()
        self.logger = logger
        self.default_user = self.create_user()
        self.default_project = self.create_project()

    @property
    def default_project_name(self):
        return "{} Project".format(type(self).__name__)

    @property
    def login_url(self):
        return reverse('core:login')

    @property
    def profile_url(self):
        return reverse('core:profile')

    @property
    def dashboard_url(self):
        return reverse('core:dashboard')

    def get_test_data(self, filename):
        return os.path.join(self.TEST_DATA_DIR, filename)

    def create_user(self, username='testuser', email='miracle-test@mailinator.com',
                    first_name='Default', last_name='Testuser', password='test'):
        return User.objects.create_user(
            username=username,
            email=email,
            first_name=first_name,
            last_name=last_name,
            password=password
        )

    def create_project(self, name=None, user=None):
        if name is None:
            name = self.default_project_name
        if user is None:
            user = self.default_user
        project = Project(name=name, creator=user)
        project.full_clean()
        project.save()
        return project

    def create_dataset(self, project=None, name=None, creator=None, datafile=None):
        if project is None:
            project = self.default_project
        if creator is None:
            creator = project.creator
        if datafile is None:
            datafile = self.get_test_data('head.csv')
        dataset = Dataset(project=project, name=name, creator=creator, datafile=datafile)
        dataset.full_clean()
        dataset.save()
        return dataset

    def create_table(self, dataset=None, name=None):
        if dataset is None:
            self.fail("table requires parent dataset")
        table = DataTable(dataset=dataset, name=name)
        table.full_clean()
        table.save()
        return table

    def create_column(self, datatable=None, name=None):
        if datatable is None:
            self.fail("column requires parent table")
        column = DataTableColumn(table=datatable, name=name)
        column.full_clean()
        column.save()
        return column

    def reverse(self, viewname, query_parameters=None, **kwargs):
        reversed_url = reverse(viewname, **kwargs)
        if query_parameters is not None:
            return '%s?%s' % (reversed_url, urlencode(query_parameters))
        return reversed_url

    def login(self, *args, **kwargs):
        return self.client.login(*args, **kwargs)

    def post(self, url, *args, **kwargs):
        if ':' in url:
            url = self.reverse(url)
        return self.client.post(url, *args, **kwargs)

    def get(self, url, *args, **kwargs):
        if ':' in url:
            url = self.reverse(url)
        return self.client.get(url, *args, **kwargs)

    class Meta:
        abstract = True