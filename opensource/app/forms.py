from django import forms

class RepoOrOrgForm(forms.Form):
    OPTION_CHOICES = [
        ('repository', 'Repository'),
        ('organization', 'Organization'),
    ]
    
    option = forms.ChoiceField(choices=OPTION_CHOICES, label='Select Option')
    organization = forms.CharField(label='Organization', max_length=100, required=False)
    repo = forms.CharField(label='Repository', max_length=100, required=False)
    key = forms.CharField(label='Key', max_length=300, required=False,widget=forms.TextInput(attrs={'placeholder': 'Optional to enter API key'}))
    
    def clean(self):
        cleaned_data = super().clean()
        option = cleaned_data.get('option')
        repo = cleaned_data.get('repo')
        organization = cleaned_data.get('organization')
        
        if option == 'repository':
            if not organization or not repo:
                raise forms.ValidationError('For a repository, both organization and repository fields are required.')
        elif option == 'organization':
            if not organization:
                raise forms.ValidationError('For an organization, the organization field is required.')
        
        return cleaned_data
