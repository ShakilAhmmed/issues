def pagination_url(request):
    full_url = request.GET.copy()
    if 'page' in full_url:
        del full_url['page']
    return {'pagination_url': '&{0}'.format(full_url.urlencode())}
