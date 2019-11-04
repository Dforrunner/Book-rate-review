from myapp.models import Books, User


def test_new_user():
    """
    GIVEN a User model
    WHEN a new User is created
    THEN check the email, hashed_password, authenticated, and role fields are defined correctly
    """
    user = User(
     email='login.confirmation.email+0@gmail.com',
     username='Testing',
     password='Test-pass-12'

    )