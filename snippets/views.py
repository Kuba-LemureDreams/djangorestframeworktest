from rest_framework import mixins, generics, permissions, renderers, viewsets
from .models import Snippet
from .permissions import isOwnerOrReadOnly
from .serializers import SnippetSerializer, UserSerializer
from django.contrib.auth.models import User
from rest_framework.decorators import api_view, action, renderer_classes
from rest_framework.response import Response
from rest_framework.reverse import reverse

class SnippetViewSet(viewsets.ModelViewSet):
    queryset = Snippet.objects.all()
    serializer_class = SnippetSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, isOwnerOrReadOnly]

    @action(detail=True, renderer_classes=[renderers.StaticHTMLRenderer])
    def highlight(self,request,*args,**kwargs):
        snippet = self.get_object()
        return Response(snippet.highlighted)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

class UserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

@api_view(['GET'])
def api_root(request, format=None):
    return Response({
        'users': reverse('user-list', request=request, format=format),
        'snippets': reverse('snippet-list', request=request, format=format)
    })
