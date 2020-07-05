from django import forms
from .models import ImageUploadModel

class ImageUploadForm(forms.ModelForm):
    # Form을 통해 받아들여야 할 데이터가 명시되어 있는 메타 데이터 (DB 테이블을 연결)
    class Meta:
        model = ImageUploadModel
        # Form을 통해 사용자로부터 입력 받으려는 Model Class의 field 리스트
        fields = ('description', 'document', ) # uploaded_at


class TestForm(forms.Form):
    """
    Form to upload the screenshot of a webpage
    """

    image_data = forms.CharField(widget=forms.HiddenInput(), required=False)

    def save_screenshot(self):
        dataUrlPattern = re.compile('data:image/(png|jpeg);base64,(.*)$')
        image_data = self.cleaned_data['image_data']
        image_data = dataUrlPattern.match(image_data).group(2)
        image_data = image_data.encode()
        image_data = base64.b64decode(image_data)

        with open('screenshot.jpg', 'wb') as f:
            f.write(image_data)

class ImgeVessel(forms.ModelForm):
    title = forms.CharField(max_length=50)
    # ImageField Inherits all attributes and methods from FileField, but also validates that the uploaded object is a valid image.
    # file = forms.FileField()
    image = forms.ImageField()

class SimpleUploadForm(forms.Form):
    # title = forms.CharField(max_length=50)
    image = forms.ImageField()
