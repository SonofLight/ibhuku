#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import pytest
import factory
import factory.django

from profiles.models import Profile
from profiles.forms import ProfileUpdateForm
from profiles.tests.factories import UserFactory


@pytest.mark.django_db
class TestUpdateProfileForm:
    """
    Test UpdateProfileForm
    """

    def setup(self):
        """
        Sets up test fixtures using Factory Boy instances. See factories.py module for more information.
        """
        self.user = UserFactory()
        self.profile = Profile.objects.get(user_id=self.user.id)
        self.form = ProfileUpdateForm()
        self.bio_text = 'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Fusce nec mi elementum, vehicula ipsum ac, eleifend magna. Suspendisse vitae aliquet nisl. Nam in lacus viverra, tempor odio eget, tempus ligula. Nullam nec est a enim elementum varius. Praesent libero felis, rutrum id mollis ultricies, imperdiet id nisl. Vestibulum fringilla egestas felis, et facilisis tellus lobortis eu. Donec tempor iaculis diam ac sagittis. Morbi at risus et dui euismod suscipit sed et dui.'

    def test_profile_update_form_is_not_bound(self):
        """
        Test ProfileUpdateForm is bound.
        """
        assert self.form.is_bound == False, 'Returns False if form is not bound.'

    def test_profile_update_form_is_bound(self):
        """
        Test ProfileUpdateForm is bound
        """
        form = ProfileUpdateForm(data={})

        assert form.is_bound == True, 'Returns True if form is bound.'

    def test_profile_update_form_is_not_valid(self):
        """
        Test form.is_valid() method.
        """
        assert self.form.is_valid() == False

    def test_profile_update_form_is_valid(self):
        """
        Test form.is_valid() method.
        """
        form = ProfileUpdateForm(data={'bio': 'Test Text.'})
        assert form.is_valid() == True

    def test_profile_update_form_field_errors(self):
        """
        Test form field errors and validation.
        """
        form = ProfileUpdateForm(data={'bio': self.bio_text})
        assert form.has_error(
            'bio', code='profile_bio_long') == True, 'Returns True if form field has an error.'
        assert form.errors == {
            'bio': ['You have exceeded the maximum length of 140 characters.']}, 'Returns kwargs of form field and error where error is reported.'
