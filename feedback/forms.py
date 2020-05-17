from django import forms

# Log In Form for Student
class StudentLogin(forms.Form):
    username = forms.CharField(
        min_length=3, max_length=20, widget=forms.TextInput(
        attrs = {
            'name': 'username',
            'id': 'username',
            'class': 'form-control mt-3',
            'placeholder': 'Username',
            'required':'True',
            'autocomplete':'off',
            'autofocus':'True'
            }
        )
    )

    password = forms.CharField(
        min_length=7, max_length=11, widget=forms.PasswordInput(
        attrs = {
            'name': 'password',
            'id': 'password',
            'class': 'form-control',
            'placeholder': 'Password',
            'required':'True'
            }
        )
    )

# Log In Form for Teacher
class TeacherLogin(forms.Form):
    username = forms.CharField(
        min_length=3, max_length=15, widget=forms.TextInput(
        attrs = {
            'name': 'username',
            'id': 'username',
            'class': 'form-control',
            'placeholder': 'Username',
            'required':'True',
            'autocomplete':'off',
            'autofocus':'True'
            }
        )
    )

    password = forms.CharField(
        min_length=8, max_length=20, widget=forms.PasswordInput(
        attrs = {
            'name': 'password',
            'id': 'password',
            'class': 'form-control',
            'placeholder': 'Password',
            'required':'True'
            }
        )
    )

# Register Form for Teacher
class TeacherRegister(forms.Form):
    first_name = forms.CharField(
        min_length=3, max_length=20, widget=forms.TextInput(
        attrs = {
            'name': 'first_name',
            'id': 'first_name',
            'class': 'form-control',
            'placeholder': 'First Name',
            'required':'True',
            'autofocus':'True',
            'autocomplete':'off'
            }
        )
    )
    
    last_name = forms.CharField(
        min_length=3, max_length=20, widget=forms.TextInput(
        attrs = {
            'name': 'last_name',
            'id': 'last_name',
            'class': 'form-control',
            'placeholder': 'Last Name',
            'required':'True',
            'autocomplete':'off'
            }
        )
    )

    email = forms.EmailField(
        min_length=8, max_length=50, widget=forms.EmailInput(
        attrs = {
            'name': 'email',
            'id': 'email',
            'class': 'form-control',
            'placeholder': 'E-mail Address',
            'required':'True',
            'autocomplete':'off'
            }
        )
    )

    username = forms.CharField(
        min_length=3, max_length=20, widget=forms.TextInput(
        attrs = {
            'name': 'username',
            'id': 'username',
            'class': 'form-control',
            'placeholder': 'Username',
            'required':'True',
            'autocomplete':'off'
            }
        )
    )

    department = forms.CharField(
        min_length=4, max_length=20, widget=forms.TextInput(
        attrs = {
            'name': 'department',
            'id': 'department',
            'class': 'form-control',
            'placeholder': 'Department',
            'required':'True',
            'autocomplete':'off'
            }
        )
    )

    password = forms.CharField(
        min_length=7, max_length=20, widget=forms.PasswordInput(
        attrs = {
            'name': 'password',
            'id': 'password',
            'class': 'form-control',
            'placeholder': 'Password',
            'required':'True'
            }
        )
    )

    image = forms.ImageField(required=False,
        widget=forms.FileInput(
            attrs = {
                'name': 'image',
                'id': 'image',
                'class': 'custom-file-input',
                'title': 'Please choose an image file...',
                'accept': '.jpeg, .png, .jpg',
            }
        )
    )

# Log in Form for Admin
class AdminLogin(forms.Form):
    username = forms.CharField(
        min_length=3, max_length=15, widget=forms.TextInput(
            attrs={
                'name': 'username',
                'id': 'username',
                'class': 'form-control',
            'placeholder': 'Username',
            'required':'True',
            'autocomplete':'off',
            'autofocus':'True'
            }
        )
    )

    password = forms.CharField(
        min_length=3, max_length=20, widget=forms.PasswordInput(
            attrs={
                'name': 'password',
                'id': 'password',
                'class': 'form-control',
                'placeholder': 'Password',
                'required':'True',
            }
        )
    )

# CSV Input
class csvFile(forms.Form):
    csv_file = forms.FileField(
        widget=forms.FileInput(
            attrs = {
                'name': 'csv_file',
                'id': 'csv_file',
                'class': 'custom-file-input',
                'title': 'Please choose a csv file to upload...',
                'accept': '.csv',
                'required':'True',
            }
        )
    )
