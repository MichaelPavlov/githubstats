import re

from django import forms


class SubmitGitHubUrlForm(forms.Form):
    repository = forms.CharField()

    def clea_repository(self):
        p = r'http(s?):\/\/github.com\/\w+\/\w+'
        r_str = self.cleaned_data['repository']
        if not re.match(p, r_str):
            raise forms.ValidationError('Invalid github repository url.')
        return r_str
