from django import forms
from .models import Ticket,Review,UserFollows


class TicketForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = '__all__'
        exclude = ['time_created','user']
        """widgets = {
            'description': forms.Textarea(attrs={'cols': 80, 'rows': 20}),
        }"""


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = '__all__'
        exclude = ['time_created','ticket','user']