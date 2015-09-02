from django.contrib.auth.models import User
from django.utils import timezone
from collections import defaultdict
from rest_framework import serializers
from .models import (Project, Dataset,)

import logging

logger = logging.getLogger(__name__)


class StringListField(serializers.ListField):
    child = serializers.CharField()


class UserSerializer(serializers.ModelSerializer):
    username = serializers.CharField(read_only=True)
    email = serializers.CharField(read_only=True)

    class Meta:
        model = User
        fields = ('username',
                  'email',
                  )


class ProjectSerializer(serializers.ModelSerializer):
    group_members = StringListField()
    group = serializers.StringRelatedField()
    creator = serializers.SlugRelatedField(slug_field='email', read_only=True)
    published = serializers.BooleanField()
    published_on = serializers.DateTimeField(format='%b %d, %Y %H:%M:%S %Z', read_only=True)
    date_created = serializers.DateTimeField(format='%b %d, %Y %H:%M:%S %Z', read_only=True)
    detail_url = serializers.CharField(source='get_absolute_url', read_only=True)
    status = serializers.CharField(read_only=True)
    number_of_datasets = serializers.IntegerField(read_only=True)
    datasets = serializers.HyperlinkedRelatedField(many=True, view_name='core:dataset-detail', read_only=True)

    def validate_group_members(self, value):
        logger.debug("validating group members with value: %s", value)
        return value

    def create(self, validated_data):
        logger.debug("creating project with data %s", validated_data)
        # FIXME: slice validated_data to only take out the name, description, and whether or not it's been published
        group_members = validated_data.pop('group_members')
        published = validated_data.pop('published', False)
        creator = validated_data.get('creator')
        if published:
            validated_data['published_on'] = timezone.now()
            validated_data['published_by'] = creator
        project = Project.objects.create(**validated_data)
        if group_members:
            users = User.objects.filter(username__in=group_members)
            logger.debug("setting group members: %s", users)
            project.set_group_members(User.objects.filter(username__in=group_members))
            project.save()
        return project

    def update(self, instance, validated_data):
        logger.debug("updating instance %s with validated data %s", instance, validated_data)
        self._modified_data = defaultdict(tuple)
        incoming_group_members = validated_data.pop('group_members')
        user = validated_data.pop('user')
        published = validated_data.pop('published')
        for attr, value in validated_data.items():
            original_value = getattr(instance, attr, None)
            if original_value != value:
                self._modified_data[attr] = (original_value, value)
                setattr(instance, attr, value)
        if published and not instance.published:
            self._modified_data['published'] = (True, False)
            instance.publish(user, defer=True)
        elif not published and instance.published:
            self._modified_data['published'] = (False, True)
            instance.unpublish(user, defer=True)
        existing_group_members = frozenset(instance.group_members)
        if existing_group_members.symmetric_difference(incoming_group_members):
            self._modified_data['group_members'] = (existing_group_members, incoming_group_members)
            users = User.objects.filter(username__in=incoming_group_members)
            instance.set_group_members(users)
        instance.save()
        return instance

    @property
    def modified_data(self):
        return getattr(self, '_modified_data', defaultdict(tuple))

    @property
    def modified_data_text(self):
        _convert = lambda v: 'None' if not v else v
        md = self.modified_data
        md_list = ['{}: {} -> {}'.format(key, _convert(pair[0]), _convert(pair[1])) for key, pair in md.items()]
        return ' | '.join(md_list)

    class Meta:
        model = Project


class DatasetSerializer(serializers.HyperlinkedModelSerializer):
    project = serializers.ReadOnlyField(source='project.name')

    class Meta:
        model = Dataset
        fields = ('id', 'name', 'datafile', 'project')