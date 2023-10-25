from rest_framework.pagination import PageNumberPagination,LimitOffsetPagination,CursorPagination

class WatchlistPagination(PageNumberPagination):
    # comment-url-lochost/?page=2
    page_size=10
    # comment-url-lochost/?p=2 |p=last to get last page by defaulut
    # page_query_param='p'
    # comment-url-lochost/?size=10|10 written by client-allows the client to set page size|
    # comment-maxpagezsize also given here
    page_size_query_param='size'
    max_page_size=20
    # comment-to get the end page,this will overwrite default last
    # last_page_strings='end'
    
class WatchlistPaginationLO(LimitOffsetPagination):
    # comment-Here we can change offset in link
    default_limit=5
    max_limit=10
    limit_query_param='limit'
    offset_query_param='start'
    
class WatchlistpaginationCursor(CursorPagination):
    page_size=5
    ordering='created'
    cursor_query_param='record'
