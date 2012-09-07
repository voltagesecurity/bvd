from django import forms
from django.contrib.auth.models import User


class SignupForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('email','username',)
        
    password1 = forms.CharField(required=True)
    password2 = forms.CharField(required=True)
    
    def clean_username(self):
        try:
            user = User.objects.get(username=self.cleaned_data.get('username'))
            raise forms.ValidationError('User exists')
        except User.DoesNotExist:
            pass
        return self.cleaned_data['username']
    
    def save(self):
        user = super(SignupForm,self).save(commit=False)
        if self.cleaned_data.get('password1',None):
            user.set_password(self.cleaned_data.get('password1'))
        user.save()