from rest_framework.decorators import api_view
from rest_framework.response import Response



@api_view()
def test_view(request):
    return Response([
        {
            "title": "Test Title 1",
            "content": "Test Content 1"
        },
        {
            "title": "Test Title 2",
            "content": "Test Content 2"
        },
        {
            "title": "Test Title 3",
            "content": "Test Content 3"
        }
    ])
