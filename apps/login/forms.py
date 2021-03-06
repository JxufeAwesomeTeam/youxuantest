from django import forms

class UserForm(forms.Form):
    username = forms.CharField(label='用户名',max_length=20,widget=forms.TextInput(attrs={'class':'form-control'}))
    password = forms.CharField(label='密码',max_length=20,widget=forms.PasswordInput(attrs={'class':'form-control'}))

class RegisterForm(forms.Form):
    gender = (
        ('male', "男"),
        ('female', "女"),
    )
    username = forms.CharField(label="用户名", max_length=128, widget=forms.TextInput(attrs={'class': 'form-control'}))
    password1 = forms.CharField(label="密码", max_length=256, widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password2 = forms.CharField(label="确认密码", max_length=256, widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(label="邮箱地址", widget=forms.EmailInput(attrs={'class': 'form-control'}))
    sex = forms.ChoiceField(label='性别', choices=gender)
    #icon = forms.ImageField(label="头像",widget=forms.ClearableFileInput(attrs={'class':'form-control','placeholder':'请上传小于5M的jpg图片'}))