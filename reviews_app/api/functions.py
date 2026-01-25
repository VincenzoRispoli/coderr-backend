
from rest_framework.exceptions import ValidationError


def validate_user_query_param(user_id_param):
    """
    Check if a user ID query parameter is a positive integer.

    Returns True if valid, False otherwise.
    """
    try:
        user_id = int(user_id_param)
        if user_id <= 0:
            raise ValueError
        return True
    except ValueError:
        return False


def filter_reviews_queryset_with_business_user_param(queryset, business_user_param):
    """
    Filter queryset by business user ID if the parameter is valid.

    Raises ValidationError if the ID is invalid.
    """
    business_user_param_is_valid = validate_user_query_param(
        business_user_param)
    if business_user_param_is_valid:
        queryset = queryset.filter(business_user=business_user_param)
        return queryset
    else:
        raise ValidationError(
            {"detail": "Die Business-User-ID muss eine integer und positive number sein"})


def filter_reviews_queryset_with_reviewer_param(queryset, reviewer_param):
    """
    Filter queryset by reviewer ID if the parameter is valid.

    Raises ValidationError if the ID is invalid.
    """
    reviewer_param_is_valid = validate_user_query_param(reviewer_param)
    if reviewer_param_is_valid:
        queryset = queryset.filter(reviewer=reviewer_param)
        return queryset
    else:
        raise ValidationError(
            {"detail": "Die Reviewer-ID muss eine integer und positive number sein"})
