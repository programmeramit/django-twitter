# forms.py
from django import forms
from .models import Tweet

class TweetForm(forms.ModelForm):
    class Meta:
        model = Tweet
        fields = ['content', 'media']
       

class EditForm(forms.ModelForm):
    class Meta:
        model = Tweet
        fields = ['content','media']

        def clean_media(self):
            media = self.cleaned_data.get('media')  # Get the media field value
            if media:
                # Check if the uploaded file has a content_type
                if hasattr(media, 'content_type'):
                    if not media.content_type.startswith('image/'):  # Example: Only allow images
                        raise forms.ValidationError("Only image files are allowed.")
                    if media.size > 5 * 1024 * 1024:  # Limit file size to 5 MB
                        raise forms.ValidationError("File size should not exceed 5 MB.")
            return media


