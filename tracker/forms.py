from django import forms
from django.contrib.auth.forms import AuthenticationForm
from .models import User, Couple, MovieTracker,MovieReview, SongMemory, Memory, MemoryPhoto, YourMoodEntry, BucketList, StatusUpdate, Playlist


class RegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Password'}))
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Confirm Password'}))

    class Meta:
        model = User
        fields = ['name', 'email', 'password']
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Your Name'}),
            'email': forms.EmailInput(attrs={'placeholder': 'Email Address'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        if cleaned_data.get('password') != cleaned_data.get('confirm_password'):
            raise forms.ValidationError("Passwords do not match.")
        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.username = user.email
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
        return user


class LoginForm(forms.Form):
    email = forms.EmailField(widget=forms.EmailInput(attrs={'placeholder': 'Email Address'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Password'}))


class CoupleStartDateForm(forms.ModelForm):
    class Meta:
        model = Couple
        fields = ['start_date']
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date'}),
        }


class JoinCoupleForm(forms.Form):
    invite_code = forms.CharField(max_length=8, widget=forms.TextInput(attrs={'placeholder': 'Enter 8-digit invite code'}))


class MovieForm(forms.ModelForm):
    class Meta:
        model = MovieTracker
        # Only include things the user actually types or selects manually
        fields = ['title', 'movie_type', 'status', 'shared_notes']

        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'glass-input',
                'placeholder': 'Movie / Series Title'
            }),
            'movie_type': forms.Select(attrs={'class': 'glass-select'}),
            'status': forms.Select(attrs={'class': 'glass-select'}),
            'shared_notes': forms.Textarea(attrs={
                'class': 'glass-textarea',
                'rows': 3,
                'placeholder': 'Add a note or a favorite quote...'
            }),
        }

class MovieReviewForm(forms.ModelForm):
    class Meta:
        model = MovieReview
        fields = ['rating', 'text']
        widgets = {
            'rating': forms.HiddenInput(attrs={'id': 'ratingInput'}),
            'text': forms.Textarea(attrs={
                'class': 'review-textarea',
                'placeholder': 'What did you think of this film…',
                'rows': '4',
            }),
        }


class SongForm(forms.ModelForm):
    class Meta:
        model = SongMemory
        fields = ['title', 'artist', 'memory_description', 'link']
        widgets = {
            'title': forms.TextInput(attrs={'placeholder': 'Song Title'}),
            'artist': forms.TextInput(attrs={'placeholder': 'Artist Name'}),
            'memory_description': forms.Textarea(attrs={'rows': 3, 'placeholder': 'What memory does this song hold?'}),
            'link': forms.URLInput(attrs={'placeholder': 'YouTube / Spotify link (optional)'}),
        }


class PlaylistForm(forms.ModelForm):
    class Meta:
        model = Playlist
        fields = ['name']
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Playlist Name'}),
        }


class MemoryForm(forms.ModelForm):
    class Meta:
        model = Memory
        fields = ['title', 'description', 'date']
        widgets = {
            'title': forms.TextInput(attrs={'placeholder': 'Trip or Event Title (e.g. Paris Trip)'}),
            'description': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Describe this memory...'}),
            'date': forms.DateInput(attrs={'type': 'date'}),
        }

class MemoryPhotoForm(forms.ModelForm):
    class Meta:
        model = MemoryPhoto
        fields = ['image', 'caption']
        widgets = {
            'caption': forms.TextInput(attrs={'placeholder': 'Caption for this photo'}),
        }


class YourMoodForm(forms.ModelForm):
    class Meta:
        model = YourMoodEntry
        fields = [
            'mood_type',
            'energy_percent',
            'sleep_hours',
            'bedtime',
            'wake_time',
            'journal_text'
        ]

        widgets = {
            'mood_type': forms.HiddenInput(attrs={'id': 'id_mood_type'}),
            'energy_percent': forms.HiddenInput(attrs={'id': 'id_energy_percent'}),
            'sleep_hours': forms.HiddenInput(attrs={'id': 'id_sleep_hours'}),
            'bedtime': forms.HiddenInput(attrs={'id': 'id_bedtime'}),
            'wake_time': forms.HiddenInput(attrs={'id': 'id_wake_time'}),

            'journal_text': forms.Textarea(attrs={
                'class': 'journal-area',
                'id': 'journalText',
                'placeholder': "Write freely... what's on your mind?",
                'rows': 4,
            }),
        }


class BucketListForm(forms.ModelForm):
    class Meta:
        model = BucketList
        fields = ['title', 'priority', 'target_date']
        widgets = {
            'title': forms.TextInput(attrs={'placeholder': 'What do you want to do together?'}),
            'target_date': forms.DateInput(attrs={'type': 'date'}),
        }


class StatusForm(forms.ModelForm):
    class Meta:
        model = StatusUpdate
        fields = ['status_text']
        widgets = {
            'status_text': forms.TextInput(attrs={'placeholder': 'What are you doing right now?'}),
        }