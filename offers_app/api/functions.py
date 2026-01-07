from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework import status, serializers
from offers_app.models import OfferDetails


def min_dev_time_validation(min_delivery_time):
    """
    Validate that the minimum delivery time is a positive integer.

    Args:
        min_delivery_time: Value to validate.

    Returns:
        int: Validated minimum delivery time.

    Raises:
        ValidationError: If the value is invalid.
    """
    try:
        min_delivery_time = int(min_delivery_time)
        if min_delivery_time <= 0:
            raise ValueError()
    except ValueError:
        raise ValidationError(
            {"max_delivery_time": "Must be an integer number or greater than 0"})
    return min_delivery_time


def validate_details_function(details, allowed_types):
    """
    Validate offer details list and allowed offer types.

    Args:
        details (list): List of offer detail dictionaries.

    Raises:
        serializers.ValidationError: If validation fails.
    """
    if len(details) != 3:
        raise serializers.ValidationError(
            {"details": "Ein Offer muss 3 Details enthalten"})

    types = []
    for index, detail in enumerate(details):
        offer_type = detail.get("offer_type")
        types.append(offer_type)
        check_if_offer_type_exist_and_is_an_allowed_type(
            index, offer_type, allowed_types)

    check_if_a_type_appears_more_than_one_time(types, allowed_types)


def check_if_offer_type_exist_and_is_an_allowed_type(index, offer_type, allowed_types):
    """
    Validate that the offer_type exists and is one of the allowed types.

    Args:
        index (int): Position of the current detail (used in the error message).
        offer_type (str): The offer_type to validate.
        allowed_types (set/list): Set or list of allowed offer_type values.

    Raises:
        serializers.ValidationError: If offer_type is missing or invalid.
    """
    if not offer_type:
        raise serializers.ValidationError(
            {"details": f"offer_type ist im Detail {index + 1} erforderlich"})

    if not offer_type in allowed_types:
        raise serializers.ValidationError(
            {"details": f"Der offer_type im Detail {index + 1} ist ungültig. "
             f"Zulässige Werte sind: basic, standard, premium"})


def check_if_a_type_appears_more_than_one_time(types, allowed_types):
    """
    Ensure that each allowed offer_type appears at most once in the list.

    Args:
        types (list): List of offer_type values to check.
        allowed_types (set/list): Set or list of allowed offer_type values.

    Raises:
        serializers.ValidationError: If any allowed type appears more than once.
    """
    for type in allowed_types:
        if types.count(type) > 1:
            raise serializers.ValidationError(
                {"details": f"Du kannst den Wert: '{type}' nur für ein einzelnes Offer Detail verwenden"})


def create_offer_instance(instance, validated_data):
    """
    Update a model instance with validated data and save it.

    Args:
        instance: Django model instance to update.
        validated_data (dict): Fields and values to update.
    """
    for attr, value in validated_data.items():
        setattr(instance, attr, value)
    instance.save()
