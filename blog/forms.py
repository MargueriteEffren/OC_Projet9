from django import forms
from . import models
from django.contrib.auth import get_user_model


class TicketForm(forms.ModelForm):
    edit_ticket = forms.BooleanField(widget=forms.HiddenInput, initial=True)
    title = forms.CharField(label='',
                            widget=forms.TextInput(attrs={'class': 'form-control',
                                                          'placeholder': 'Titre'}))
    description = forms.CharField(label='',
                                  widget=forms.TextInput(attrs={'class': 'form-control',
                                                                'placeholder': 'Description'}))

    class Meta:
        model = models.Ticket
        fields = ['title', 'description', 'image']


class DeleteTicketForm(forms.Form):
    delete_ticket = forms.BooleanField(widget=forms.HiddenInput, initial=True)


class TicketReviewForm(forms.ModelForm):
    edit_review = forms.BooleanField(widget=forms.HiddenInput, initial=True)
    RATING_CHOICES = [
        (0, "- 0"), (1, "- 1"), (2, "- 2"), (3, "- 3"), (4, "- 4"), (5, "- 5")
    ]
    rating = forms.ChoiceField(widget=forms.RadioSelect,
                               choices=RATING_CHOICES)

    class Meta:
        model = models.Review
        fields = ['ticket', 'headline',
                  'content', 'body', 'rating']


class DeleteTicketReviewForm(forms.Form):
    delete_review = forms.BooleanField(widget=forms.HiddenInput, initial=True)


class DeleteSubscriptionForm(forms.Form):
    delete_subscription = forms.BooleanField(widget=forms.HiddenInput, initial=True)


User = get_user_model()


class UserFollowsForm(forms.ModelForm):
    followed_user = forms.CharField(label='',
                                    max_length=256,
                                    widget=forms.TextInput(attrs={"placeholder": " Nom d'utilisateur"}),
                                    )

    class Meta:
        model = models.UserFollows
        fields = ['followed_user']

    def clean(self):
        cleaned_data = super(UserFollowsForm, self).clean()
        followed_user = cleaned_data.get('followed_user')
        if models.UserFollows.objects.filter(followed_user=followed_user).exists():
            raise forms.ValidationError('Category already exists')
