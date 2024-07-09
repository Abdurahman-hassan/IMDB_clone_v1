from rest_framework.pagination import PageNumberPagination, LimitOffsetPagination, CursorPagination


class WatchlistPagination(PageNumberPagination):
    page_size = 1
    page_query_param = 'p'
    page_size_query_param = 'page_size'
    max_page_size = 30
    last_page_strings = ('end',)


class WatchlistOffsetPagination(LimitOffsetPagination):
    # offset means the number of items to skip before starting to return items
    # limit means the maximum number of items to return
    default_limit = 2
    limit_query_param = 'limit'
    offset_query_param = 'skip'
    max_limit = 30


class WatchlistCursorPagination(CursorPagination):
    page_size = 2
    # we must have in view the ordering field
    # ordering = '-avg_rating'  # ordering from oldest to newest if we need the opposite we can use '-field_name'
    ordering = 'created'  # ordering from oldest to newest if we need the opposite we can use '-field_name'
    cursor_query_param = 'record'

