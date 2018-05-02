from django import forms
from .models import Post,Comment

#처음에는 validator를 forms.py에 저장하여 PostForm에 적용하였으나
#PostModelForm에는 적용할 수 가 없어서 models.py 로 이동시켜야 한다.
# def min_length_3_validator(value):
#     if len(value) < 3:
#         raise forms.ValidationError('3글자 이상 입력해 주세요.')

class PostForm(forms.Form):
    #title = forms.CharField(validators=[min_length_3_validator])
    title = forms.CharField()
    text = forms.CharField(widget=forms.Textarea)

class PostModelForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title','text']

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('author', 'text',)
