import urllib
from django.http import HttpResponse

"""
Input: A Django request object and a destination url (dest_url)
Output: returns a HttpResponse object for immediate use
"""
def json_get(request, dest_url):
    # Check if POST request has parameter 'query'
    if request.method == 'POST' and request.POST.dict().has_key('query'):
        query = request.POST.get('query', '')

        # Check that query is not blank
        if not query.strip():
            return HttpResponse('Query is blank.')

        # Process query
        params = urllib.urlencode(dict(query=query))
        reply = urllib.urlopen(dest_url, params)
        data = reply.read()
        reply.close()

        return HttpResponse(data)
    else:
        return HttpResponse('Invalid request.')


