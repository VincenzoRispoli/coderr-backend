

def fill_user_data_dict(token, user):
    """
    Construct a dictionary containing authentication token and user information.

    Args:
        token: The authentication token instance.
        user: The User instance.

    Returns:
        dict: Dictionary with keys 'token', 'username', 'email', and 'user_id'.
    """
    return {
        'token': token.key,
        'username': user.username,
        'email': user.email,
        'user_id': user.id
    }


def guest_user_data_dict(token, guest_user):
    """
    Construct a dictionary for guest users including authentication token and personal info.

    Args:
        token: The authentication token instance.
        guest_user: The guest User instance.

    Returns:
        dict: Dictionary with keys 'token', 'username', 'email', 'first_name', 'last_name', and 'user_id'.
    """
    return {
        'token': token.key,
        'username': guest_user.username,
        'email': guest_user.email,
        'first_name': guest_user.first_name,
        'last_name': guest_user.last_name,
        'user_id': guest_user.id
    }
