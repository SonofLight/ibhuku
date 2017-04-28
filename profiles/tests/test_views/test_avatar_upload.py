#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import pytest
import factory
import factory.django

from django.core.urlresolvers import reverse, resolve
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import override_settings
from django.conf import settings

from users.models import User
from profiles.models import Profile, ProfileAvatar
from profiles.forms import AvatarUploadForm
from profiles.tests.factories import UserFactory
from profiles.views import profile_dashboard, user_update


@pytest.mark.django_db
class TestAvatarUpload:
    """
    Test avatar upload view.
    """

    def setup(self):
        """
        Sets up test fixtures using Factory Boy instances. See factories.py module for more information.
        """
        self.user = UserFactory()
        self.profile = Profile.objects.get(user_id=self.user.id)
        self.avatar = ProfileAvatar.objects.select_related(
            'profile').get(profile_id=self.profile.id)

        self.image = SimpleUploadedFile(name='test.jpg', content=open(
            'profiles/tests/test_images/test.jpg', 'rb').read())

    def test_avatar_upload_view(self, client):
        """
        Test Avatar Upload View.
        """
        response = client.get(reverse(
            'profiles:av-upload', kwargs={'pk': self.user.id, 'username': self.user.username}))

        assert response.status_code == 302, 'Returns 302'
        assert response.resolver_match.url_name == 'av-upload'
        assert response.resolver_match.view_name == 'profiles:av-upload'

    def test_avatar_upload_parameter_kwargs(self, client):
        """
        Test avatar upload kwargs.
        """
        response = client.get(reverse(
            'profiles:av-upload', kwargs={'pk': self.user.id, 'username': self.profile.user.username}))
        assert response.resolver_match.kwargs == {
            'pk': '2', 'username': 'Testy1McT'}

    @override_settings(MEDIA_ROOT='/tmp/django_test')
    def test_avatar_upload_image_saves(self, client):
        """
        Test of profile image upload saves to model.
        """
        image = SimpleUploadedFile(name='test.jpg', content=open(
            'profiles/tests/test_images/test.jpg', 'rb').read())

        response = client.post(reverse('profiles:av-upload', kwargs={
            'pk': self.user.id, 'username': self.user.username}), {'avatar': image}, follow=True)

        avatar = ProfileAvatar.objects.select_related(
            'profile').get(profile_id=self.user.id)

        assert avatar.avatar.name == 'user_Testy2McT_3/avatar/profile_Testy2McT_bzFAwYw.jpg', 'Should return new filename and path.'
