from django.test import SimpleTestCase, TestCase

from microlearning.forms import LoginForm, UserSettingsForm, UserRegistrationForm, UserEditForm, ProfileEditForm


class TestForms(SimpleTestCase):

    def test_LoginForm(self):
        form = LoginForm(data={
            'username': 'olla',
            'password': 'ollapass'
        })

        self.assertTrue(form.is_valid())

    def test_LoginForm_bad_data(self):
        form = LoginForm(data={
            'username': 'olla',
            'password': ''
        })

        self.assertFalse(form.is_valid())
        self.assertEqual(len(form.errors), 1)
        self.assertEqual(form.errors['password'][0], 'This field is required.')

    def test_LoginForm_no_data(self):
        form = LoginForm(data={})

        self.assertFalse(form.is_valid())
        self.assertEqual(len(form.errors), 2)
        self.assertEqual(form.errors['username'][0], 'This field is required.')
        self.assertEqual(form.errors['password'][0], 'This field is required.')

    def test_UserSettingsForm(self):
        form = UserSettingsForm(data={'category': 'pediatrics'})

        self.assertTrue(form.is_valid())

    def test_UserSettingsForm_no_data(self):
        form = UserSettingsForm(data={'category': ''})

        self.assertTrue(form.is_valid())

    def test_UserSettingsForm_bad_data(self):
        form = UserSettingsForm(data={'category': 'Pediatrics'})

        self.assertFalse(form.is_valid())

    def test_UserEditForm(self):
        form = UserEditForm(data={'first_name': 'olla',
                                  'last_name': 'olla2',
                                  'email': 'olla@tut.by'
                                  })

        self.assertTrue(form.is_valid())

    def test_UserEditForm_bad_data(self):
        form = UserEditForm(data={'first_name': 'olla',
                                  'last_name': 'olla2',
                                  'email': '2'
                                  })

        self.assertFalse(form.is_valid())
        self.assertEqual(len(form.errors), 1)
        self.assertEqual(form.errors['email'][0], 'Enter a valid email address.')

    def test_ProfileEditForm(self):
        form = ProfileEditForm(data={'subscribed_category': 'pediatrics'})

        self.assertTrue(form.is_valid())

    def test_ProfileEditForm_no_data(self):
        form = ProfileEditForm(data={'subscribed_category': ''})

        self.assertTrue(form.is_valid())

    def test_ProfileEditForm_bad_data(self):
        form = ProfileEditForm(data={'subscribed_category': 'str'})

        self.assertFalse(form.is_valid())
        self.assertEqual(len(form.errors), 1)
        self.assertEqual(form.errors['subscribed_category'][0], 'Select a valid choice. str is not one of the available choices.')


class TestUserRegistrationForm(TestCase):

    def test_UserRegistrationForm(self):
        form = UserRegistrationForm(data={
            'password': 'pass',
            'password2': 'pass',
            'username': 'olla',
            'first_name': 'olla2',
            'email': 'olla@tut.by'
        })

        self.assertTrue(form.is_valid())

    def test_UserRegistrationForm_bad_pass(self):
        form = UserRegistrationForm(data={
            'password': 'pass',
            'password2': 'pass2',
            'username': 'olla',
            'first_name': 'olla2',
            'email': 'olla@tut.by'
        })

        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['password2'][0], 'bad pass')

    def test_UserRegistrationForm_bad_data(self):
        form = UserRegistrationForm(data={
            'password': 'pass',
            'password2': 'pass2',
            'username': '',
            'first_name': 'olla2',
            'email': '2'
        })

        self.assertFalse(form.is_valid())
        self.assertEqual(len(form.errors), 3)
        self.assertEqual(form.errors['username'][0], 'This field is required.')
        self.assertEqual(form.errors['email'][0], 'Enter a valid email address.')
        self.assertEqual(form.errors['password2'][0], 'bad pass')

    def test_UserRegistrationForm_bad_data_empty(self):
        form = UserRegistrationForm(data={
            'password': '',
            'password2': '',
            'username': '',
            'first_name': '',
            'email': ''
        })

        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['password'][0], 'This field is required.')
        self.assertEqual(form.errors['password2'][0], 'This field is required.')
        self.assertEqual(form.errors['username'][0], 'This field is required.')
