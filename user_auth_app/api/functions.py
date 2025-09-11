

def fill_user_data_dict(token, user, user_profile):
    """Return a dictionary with authentication token and user information.

    Args:
        token: The authentication token instance.
        user: The User instance.
        user_profile: The associated UserProfile instance.

    Returns:
        dict: A dictionary containing the token key, username, email, and
              user profile ID.
    """
    return {
        'token': token.key,
        'username': user.username,
        'email': user.email,
        'user_id': user_profile.id
    }


def guest_user_data_dict(token, guest_user, guest_user_profile):
    return {
        'token': token.key,
        'username': guest_user.username,
        'email': guest_user.email,
        'first_name': guest_user.first_name,
        'last_name': guest_user.last_name,
        'user_id': guest_user_profile.id
    }
