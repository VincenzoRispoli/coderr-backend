

def fill_user_data_dict(token, user):
    """Return a dictionary with authentication token and user information.

    Args:
        token: The authentication token instance.
        user: The User instance.

    Returns:
        dict: A dictionary containing the token key, username, email, and
              user profile ID.
    """
    return {
    'token': token.key,
    'username': user.username,
    'email': user.email,
    'user_id': user.id
    }


def guest_user_data_dict(token, guest_user):
    return {
        'token': token.key,
        'username': guest_user.username,
        'email': guest_user.email,
        'first_name': guest_user.first_name,
        'last_name': guest_user.last_name,
        'user_id': guest_user.id
    }
