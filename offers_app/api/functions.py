from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework import status, serializers
from offers_app.models import OfferDetails


def check_parameters(query_params):
    print(query_params)
    pass


def filter_with_creator_id_param(queryset, creator_id):
    """
    Filter the queryset by creator ID.

    Validates the `creator_id` and filters the queryset
    to include only offers created by that user.
    """
    validated_creator_id = creator_id_validation(creator_id)
    queryset = queryset.filter(user=validated_creator_id)
    return queryset


def filter_with_min_delivery_time_param(queryset, min_delivery_time):
    """
    Filter the queryset by minimum delivery time.

    Validates `min_delivery_time` and filters the queryset
    to include offers with `min_delivery_time` less than or equal to the value.
    """
    validated_min_delivery_time = min_dev_time_validation(min_delivery_time)
    queryset = queryset.filter(
        min_delivery_time__lte=validated_min_delivery_time)
    return queryset


def filter_with_min_price_param(queryset, min_price):
    """
    Filter the queryset by minimum price.

    Validates `min_price` and filters the queryset
    to include offers matching the specified minimum price.
    """
    validated_min_price = min_price_validation(min_price)
    queryset = queryset.filter(min_price=validated_min_price)
    return queryset


def creator_id_validation(creator_id):
    """
    Validate that `creator_id` is a positive integer (> 0).

    Raises ValidationError if the value is invalid.
    """
    try:
        creator_id = int(creator_id)
        if creator_id <= 0:
            raise ValueError()
        return creator_id
    except ValueError:
        raise ValidationError(
            {"creator_id": "Muss eine integer number sein und größer als 0 sein"})


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
        return min_delivery_time
    except ValueError:
        raise ValidationError(
            {"max_delivery_time": "Muss eine integer number und größer als 0 sein"})


def min_price_validation(min_price):
    """
    Ensure `min_price` is a positive number and return it as a float.

    Raises ValidationError if the value is invalid.
    """
    try:
        min_price = float(min_price)
        if min_price <= 0:
            raise ValueError()
        return min_price
    except ValueError:
        raise ValidationError(
            {"min_price": "Der mindeste Preis muss eine float / integer number und größer als 0 sein"})


def validate_details_function(details, allowed_types, request):
    """
    Validate offer details list and allowed offer types.

    Args:
        details (list): List of offer detail dictionaries.

    Raises:
        serializers.ValidationError: If validation fails.
    """
    if request.method == "POST":
        if not details or len(details) != 3:
            raise serializers.ValidationError(
                {"details": "Ein Offer muss 3 Details enthalten"})
    elif request.method == "PATCH":
        if details is not None and len(details) > 3:
            raise serializers.ValidationError(
                {"details": "Die Angebotsdetails dürfen maximal 3 sein"})

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
