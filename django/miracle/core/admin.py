from django.contrib import admin

from . import models

for model_class in (models.Project, models.DataTableGroup, models.MiracleUser, models.Author, models.DataAnalysisScript,
                    models.DataColumn, models.ActivityLog, models.AnalysisOutput, models.AnalysisParameter,
                    models.AnalysisOutputFile):
    admin.site.register(model_class)
