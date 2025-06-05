from django import forms
from .models import Post, Category, Comment


choice_list = [(cat.name, cat.name) for cat in Category.objects.all()] 

class PostForm(forms.ModelForm):
    class Meta:
        model= Post
        fields= ['title', 'title_tag', 'author', 'header_image', 'category', 'snippet', 'body']
        widgets= {
            'title': forms.TextInput(attrs={'class':'form-control'}),
            'title_tag': forms.TextInput(attrs={'class':'form-control'}),
            # 'author': forms.TextInput(attrs={'class':'form-control', 'value':'', 'id':'elder', 'type':'hidden'}),
            # 'author': forms.Select(attrs={'class':'form-control'}), # select= dropdown menu
            'author': forms.HiddenInput(), 
            'category': forms.Select(choices=choice_list, attrs={'class':'form-control'}),
            'body': forms.Textarea(attrs={'class':'form-control'}),
            'snippet': forms.Textarea(attrs={'class':'form-control'}),    

        }

    def __init__(self, *args, **kwargs):
        super(PostForm, self).__init__(*args, **kwargs)
        self.fields['category'].widget.choices = [(cat.name, cat.name) for cat in Category.objects.all()]


class EditForm(forms.ModelForm):
    class Meta:
        model= Post
        fields= ['title', 'title_tag', 'header_image', 'snippet', 'body']
        widgets= {
            'title': forms.TextInput(attrs={'class':'form-control'}),
            'title_tag': forms.TextInput(attrs={'class':'form-control'}),
            'snippet': forms.Textarea(attrs={'class':'form-control'}),    
            'body': forms.Textarea(attrs={'class':'form-control'}),    
        }


class CommentForm(forms.ModelForm):
    class Meta:
        model= Comment
        fields= ('name', 'body')
        widgets= {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'body': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),  
        }