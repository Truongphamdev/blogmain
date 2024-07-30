from django import forms
from .models import Comment,Post

class FormComment(forms.ModelForm):
    class Meta:
        model = Comment
        exclude = ['post']
        labels = {
            'user_name':'Your Name',
            'user_email':'Your Email',
            'text':'Your Text'
        }
class PostForm(forms.ModelForm):
    author_first_name = forms.CharField(max_length=100,label='Your first name')
    author_last_name = forms.CharField(max_length=100,label='Your last name')
    author_email = forms.EmailField(label='Your email')
    class Meta:
        model = Post
        fields = ['title', 'excerpt', 'image', 'content', 'tags']
        labels = {
            'title':'Your title',
            'excerpt':'Your excerpt',
            'image':'Your image',
            'content':'Your content',
            'tag':'Your tag',
        }
    
    def clean_title(self):
        title = self.cleaned_data.get('title')
        return title.strip()