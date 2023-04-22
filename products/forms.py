from django import forms
from .models import Product,Comment,ProductImage,CommentImage

class ProductForm(forms.ModelForm):

    class Meta:
        model = Product
        fields = ('title', 'content', 'price', 'discount_rate', 'delivery_date', 'category', 'delivery', 'free_shipping', 'c_avenue',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['title'].widget.attrs['class'] = 'form-control mt-1'

        self.fields['price'].widget.attrs['class'] = 'form-control'

        self.fields['discount_rate'].widget.attrs['class'] = 'form-control'

        self.fields['delivery_date'].widget.attrs['class'] = 'form-control'

        self.fields['category'].widget.attrs['class'] = 'form-control'

        self.fields['delivery'].widget.attrs['class'] = 'form-control'

class ProductImageForm(forms.ModelForm):
    class Meta:
        model = ProductImage
        fields = ('image',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['image'].widget.attrs['multiple'] = True
        self.fields['image'].widget.attrs['class'] = 'form-control ps-1'

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('title', 'content',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['title'].widget.attrs['class'] = 'form-control my-3'

        self.fields['content'].widget.attrs['class'] = 'form-control my-3'

class CommentImageForm(forms.ModelForm):
    class Meta:
        model = CommentImage
        fields = ('comment_image',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['comment_image'].widget.attrs['multiple'] = True