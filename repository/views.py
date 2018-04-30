import datetime

from github import Github
from rest_framework.response import Response
from rest_framework.views import APIView
from social_django.models import UserSocialAuth

from repository.serializers import RepositoryDataSerializer

test_data = [
    {
        "username": "Anthony",
        "commits": [
            {"date": '2013-01-29', "count": 10},
            {"date": '2013-01-29', "count": 11}
        ]
    },
    {
        "username": "Bravo",
        "commits": [
            {"date": '2013-01-29', "count": 20},
            {"date": '2013-01-29', "count": 21}
        ]
    }
]


def get_current_user_access_token(user):
    user_social_auth = UserSocialAuth.objects.get(user=user)
    token = user_social_auth.extra_data['access_token']
    return token


def convert_pygithub_commits(pygithub_commits):
    result = {}
    for date, commits in pygithub_commits.items():
        for username, commits_count in commits.items():
            if not username in result:
                result[username] = {}
            result[username][date] = commits_count

    repository_data = [{
        "username": usr,
        "commits": [{
            "date": d,
            "count": c
        } for d, c in cm.items()]} for usr, cm in result.items()]
    return repository_data


def get_commits_data(token, git_user, git_repo, since=None, until=None):
    since = datetime.datetime.strptime(since, '%Y-%m-%d')
    repo = '{}/{}'.format(git_user, git_repo)
    commits = Github(token).get_repo(repo).get_commits(since=since)
    pygithub_commits = {}
    for commit in commits:
        # date = datetime.datetime.strptime(commit.commit.author.date, '%a, %d %b %Y %H:%M:%S GMT')
        date = commit.commit.author.date
        iso_date = date.date().isoformat()
        commiter = commit.author.login
        if not iso_date in pygithub_commits:
            pygithub_commits[iso_date] = {}
        if commiter in pygithub_commits[iso_date]:
            pygithub_commits[iso_date][commiter] += 1
        else:
            pygithub_commits[iso_date][commiter] = 1

    return convert_pygithub_commits(pygithub_commits)


class RepositoryDataView(APIView):
    serializer_class = RepositoryDataSerializer

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated():
            token = get_current_user_access_token(request.user)

            git_user = self.kwargs.get('username')
            git_repo = self.kwargs.get('repository')
            fromdate = self.kwargs.get('fromdate', None)

            commits = get_commits_data(token, git_user, git_repo, fromdate)

            serializer = RepositoryDataSerializer(
                instance=commits, many=True
            )
            return Response(serializer.data)
