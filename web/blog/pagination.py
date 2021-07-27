from collections import OrderedDict

from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response


class StandardResultsSetPagination(PageNumberPagination):
    page_size = 5

    def get_paginated_response(self, data):
        response = super().get_paginated_response(data)
        response.data.update(self.get_html_context())
        return response
