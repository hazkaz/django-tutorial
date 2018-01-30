from django.conf.urls import url, include
from snippets import views
from rest_framework.urlpatterns import format_suffix_patterns
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    url(r'^auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^snippets/$', views.SnippetList.as_view(), name='list_or_create'),
    url(r'^snippets/(?P<pk>[0-9]+)/$', views.SnippetDetail.as_view(), name='update_or_delete'),
    url(r'get-token/', obtain_auth_token)
]

urlpatterns = format_suffix_patterns(urlpatterns)
