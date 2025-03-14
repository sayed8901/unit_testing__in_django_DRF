from account.models import User
from account.serializers import UserSerializer

from rest_framework.test import APITestCase





class UserSerializerTestCase(APITestCase):
    def test_user_serializer_valid_data(self):
        data = {
            'email': 'test@example.com',
            'name': 'Test User',
            'password': 'testpassword',
            'confirm_password': 'testpassword',
        }

        serializer = UserSerializer(data = data)


        # checking that the serializer is valid
        self.assertTrue(serializer.is_valid())

        # checking that the serializer has no errors
        self.assertEqual(serializer.errors, {})




    def test_user_serializer_password_mismatch(self):
        data = {
            'email':'test@example.com',
            'name': 'Test User',
            'password': 'testpassword',
            'confirm_password': 'mismatch_password'
        }

        serializer = UserSerializer(data = data)


        # checking that the serializer is not valid due to password mismatch
        self.assertFalse(serializer.is_valid())

        # checking that, if the password mismatched, the serializer shows exactly the following error
        self.assertEqual(
            serializer.errors['non_field_errors'][0], 
            "Password and Confirm_Password doesn't match."
        )




    def test_user_serializer_duplicate_email(self):
        exist_email='existinguser@example.com'
        password='testpassword'
        name='Test User'

        User.objects.create_user(
            email=exist_email, password=password, name=name
        )

        data = {
            'email': exist_email,  # Duplicate email
            'name': name,
            'password': password,
            'confirm_password': password
        }

        serializer = UserSerializer(data=data)


        # checking that the serializer is not valid due to duplicate email address
        self.assertFalse(serializer.is_valid())

        # checking that, if the password mismatched, the serializer shows exactly the following error
        self.assertEqual(
            serializer.errors['email'][0], 
            'user with this Email already exists.'
        )





    def test_user_serializer_create(self):
        data = {
            'email': 'test@example.com',
            'name': 'Test User',
            'password': 'testpassword',
            'confirm_password': 'testpassword'
        }

        serializer = UserSerializer(data=data)


        # checking that the serializer is valid
        self.assertTrue(serializer.is_valid())

        # creating an user using the user serializer
        user = serializer.create(serializer.validated_data)


        # finally, checking that, newly created user name and email is correct or not
        self.assertEqual(user.email, 'test@example.com')
        self.assertEqual(user.name, 'Test User')

        self.assertFalse(user.is_active)




    def test_user_serializer_update(self):
        user = User.objects.create_user(
            email='existinguser@example.com', 
            password='testpassword', 
            name='Test User'
        )

        # updating the user name
        data = {
            'name': 'Updated User'
        }

        serializer = UserSerializer(
            instance=user, data=data, partial=True
        )


        # checking that the serializer is valid
        self.assertTrue(serializer.is_valid())


        # updating the user info..
        updated_user = serializer.update(user, serializer.validated_data)


        # checking that the serializer has updated the user name or not
        self.assertEqual(updated_user.name, 'Updated User')
