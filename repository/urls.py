from django.conf.urls import url

from repository.views import RepositoryDataView

urlpatterns = [
    url('^(?P<username>\w+)/(?P<repository>\w+)$', RepositoryDataView.as_view(), name='commits'),
    url(
        '^(?P<username>\w+)/(?P<repository>\w+)/(?P<fromdate>\d{4}-\d{2}-\d{2})$',
        RepositoryDataView.as_view(), name='commits-for-period'
    ),
]
