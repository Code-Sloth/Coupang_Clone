from django.db import models
from django.conf import settings
import os
from django.core.validators import MinValueValidator, MaxValueValidator
from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFill
from django.utils import timezone
from datetime import timedelta,datetime
from ckeditor_uploader.fields import RichTextUploadingField

# Create your models here.

class Product(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    like_users = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='like_products')
    title = models.CharField(max_length=80)
    price = models.IntegerField(default=0)
    star = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    count = models.IntegerField(default=1)
    category_Choices = (('패션의류/잡화', '패션의류/잡화'), ('뷰티', '뷰티'), ('식품', '식품'), ('주방용품', '주방용품'), ('생활용품', '생활용품'))
    category = models.CharField(max_length=20, choices=category_Choices)

    content = RichTextUploadingField(blank=True,null=True)
    delivery_date = models.IntegerField(default=7)

    delivery_Choices = (('로켓배송','로켓배송'), ('제트배송','제트배송'), ('로켓직구','로켓직구'), ('로켓프레시','로켓프레시'))
    delivery = models.CharField(max_length=20, choices=delivery_Choices, null=True, blank=True)
    free_shipping = models.BooleanField(default=False)
    c_avenue = models.BooleanField(default=False)
    discount_rate = models.IntegerField(default=0)

    def count_likes_user(self):
        return self.like_users.count()
    
    def __str__(self):
        return self.title

class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    def product_image_path(instance, filename):
        return f'products/{instance.product.pk}/{filename}'

    image = ProcessedImageField(
        upload_to=product_image_path,
        spec_id='albums:image',
        processors=[ResizeToFill(230,230)],
        format='JPEG',
        options={'quality' : 100},
        blank=True,
        null=True,
    )

    def delete(self, *args, **kargs):
        if self.image:
            os.remove(os.path.join(settings.MEDIA_ROOT, self.image.name))
        super(ProductImage, self).delete(*args, **kargs)

    def save(self, *args, **kwargs):
        if self.id:
            old_post = ProductImage.objects.get(id=self.id)
            if self.image != old_post.image:
                if old_post.image:
                    os.remove(os.path.join(settings.MEDIA_ROOT, old_post.image.name))
        super(ProductImage, self).save(*args, **kwargs)

class Comment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    content = models.TextField(null=False)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    star = models.IntegerField(default=5, validators=[MinValueValidator(1), MaxValueValidator(5)])
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def created_string(self):
        time = datetime.now(tz=timezone.utc) - self.created_at

        if time < timedelta(minutes=1):
            return '방금 전'
        elif time < timedelta(hours=1):
            return str(int(time.seconds / 60)) + '분 전'
        elif time < timedelta(days=1):
            return str(int(time.seconds / 3600)) + '시간 전'
        elif time < timedelta(days=7):
            time = datetime.now(tz=timezone.utc).date() - self.created_at.date()
            return str(time.days) + '일 전'
        else:
            return self.strftime('%Y-%m-%d')

class CommentImage(models.Model):
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE, related_name='comment_img')

    def comment_image_path(instance, filename):
        return f'comments/{instance.comment.pk}/{filename}'
    
    comment_image = ProcessedImageField(
        upload_to=comment_image_path,
        spec_id='albums:image',
        processors=[ResizeToFill(230,230)],
        format='JPEG',
        options={'quality' : 100},
        blank=True,
        null=True,
    )

    def delete(self, *args, **kargs):
        if self.comment_image:
            os.remove(os.path.join(settings.MEDIA_ROOT, self.comment_image.name))
        super(CommentImage, self).delete(*args, **kargs)

    def save(self, *args, **kwargs):
        if self.id:
            old_post = CommentImage.objects.get(id=self.id)
            if self.comment_image != old_post.comment_image:
                if old_post.comment_image:
                    os.remove(os.path.join(settings.MEDIA_ROOT, old_post.comment_image.name))
        super(CommentImage, self).save(*args, **kwargs)
