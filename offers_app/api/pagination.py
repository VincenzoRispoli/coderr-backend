from rest_framework.pagination import PageNumberPagination

"""
    Custom pagination class for offers.

       Attributes:
           page_query_param (str): The query parameter used to specify the page number. Default is 'page'.
           page_size (int): The default number of items per page. Default is 6.
           page_size_query_param (str): The query parameter that allows clients to set a custom page size. Default is 'page_size'.
           max_page_size (int): The maximum number of items allowed per page. Default is 6.
"""
class OfferPagination(PageNumberPagination):
    page_query_param = 'page'
    page_size = 6
    page_size_query_param = 'page_size'
    max_page_size = 6
