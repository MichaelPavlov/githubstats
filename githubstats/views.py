import datetime

from django.urls import reverse_lazy
from django.views.generic.edit import FormView

from githubstats.forms import SubmitGitHubUrlForm


class SubmitGitHubUrlFormView(FormView):
    template_name = "homepage.html"
    form_class = SubmitGitHubUrlForm

    def get_success_url(self):
        repository_url = self.get_form().data['repository']
        username = repository_url.split('/')[-2]
        repository = repository_url.split('/')[-1]
        week_ago = datetime.datetime.now() - datetime.timedelta(days=7)
        url = reverse_lazy(
            'repository-api:commits-for-period',
            kwargs={
                "username": username,
                "repository": repository,
                "fromdate": str(week_ago.date())
            }
        )
        return url
