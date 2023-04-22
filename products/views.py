from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from .models import Product, Comment, ProductImage, CommentImage
from .forms import ProductForm, CommentForm, ProductImageForm, CommentImageForm
from django.db.models import Q
from django.conf import settings
import os

# import ModelViewSet
# from .serializers import ProductSerializer


# Create your views here.

def index(request):
    products = Product.objects.all()
    product_images = []
    for product in products:
        comments = product.comment_set.all()
        count_star = 0
        sum_comment = comments.count()
        for comment in comments:
            count_star += comment.star
        avg_comment = count_star / sum_comment
        product.star = avg_comment
        images = ProductImage.objects.filter(product=product)
        if images:
            product_images.append((product, images[0]))
        else:
            product_images.append((product, ''))

    context = {
        'product_images': product_images,
    }
    return render(request, 'products/index.html',context)

# def search(request):
#     query = request.GET.get('q','')
#     if query:
#         search = product.objects.filter(
#             Q(author__username=query)|
#             Q(title__icontains=query)|
#             Q(content__icontains=query)|
#             Q(movie__icontains=query)
#             )
#     else:
#         search = product.objects.all()[::-1]
#     return render(request, 'products/index.html',{'products':search})

@login_required
def create(request):
    if request.method == 'POST':
        form = ProductForm(request.POST)
        files = request.FILES.getlist("image")
        if form.is_valid():
            f = form.save(commit=False)
            f.user = request.user
            f.save()
            for i in files:
                ProductImage.objects.create(image=i, product=f)
            return redirect('products:index')
        else:
            print(form.errors)
    else:
        product_form = ProductForm()
        image_form = ProductImageForm()
    context = {'product_form': product_form, 'image_form':image_form,}
    return render(request, 'products/create.html', context)


def detail(request, product_pk):
    product = Product.objects.get(pk=product_pk)
    comments = product.comment_set.all()
    count_star = 0
    sum_comment = comments.count()
    for comment in comments:
        count_star += comment.star
    avg_comment = count_star / sum_comment
    product.star = avg_comment
    product.save()

    product_images = []
    images = ProductImage.objects.filter(product=product)
    if images:
        product_images.append((product, images))
    else:
        product_images.append((product, ''))

    context = {
        'product':product,
        'product_images':product_images,
        'comments':comments,
        'like_count':product.count_likes_user(),
    }
    return render(request, 'products/detail.html',context)

@login_required
def delete(request, product_pk):
    product = Product.objects.get(pk=product_pk)
    if request.user == product.user:
        product.delete()
    return redirect('products:index')

@login_required
def update(request, product_pk):
    product = Product.objects.get(pk=product_pk)
    delete_images = product.image_set.all()
    images = ProductImage.objects.filter(product=product)

    if request.method == 'POST':
        form = ProductForm(request.POST, instance=product)
        files = request.FILES.getlist("image")
        if form.is_valid():
            f = form.save(commit=False)
            f.user = request.user
            f.save()
            if request.FILES.get('image'):
                if request.POST.get('sub') == '수정':
                    for i in delete_images:
                        i.delete()

            for i in files:
                ProductImage.objects.create(image=i, product=f)
            return redirect('products:index')
        else:
            print(form.errors)
    else:
        productform = ProductForm(instance=product)
        imageform = ProductImageForm()
    context = {
        'productform': productform,
        'imageform': imageform,
        'images': images
        }
    return render(request, 'products/update.html', context)

# if request.method == 'POST':
#         form = ProductForm(request.POST)
#         files = request.FILES.getlist("image")
#         if form.is_valid():
#             f = form.save(commit=False)
#             f.user = request.user
#             f.save()
#             for i in files:
#                 ProductImage.objects.create(image=i, product=f)
#             return redirect('products:index')

@login_required
def comment_create(request, product_pk):
    product = Product.objects.get(pk=product_pk)

    if request.method == "POST":
        comment_form = CommentForm(request.POST)
        files = request.FILES.getlist('comment_image')
        
        if comment_form.is_valid():
            c = comment_form.save(commit=False)
            c.product = product
            c.user = request.user
            c.star = request.POST.get('star_rating')
            c.save()

            for i in files:
                CommentImage.objects.create(comment_image=i, comment=c)

            return redirect('products:detail', product_pk)

    else:
        comment_form = CommentForm()
        commentimage_form = CommentImageForm()
    context = {
        'comment_form':comment_form,
        'commentimage_form':commentimage_form,
        'product':product,
    }
    return render(request,'products/comment_create.html', context)

@login_required
def comment_delete(request, product_pk, comment_pk):
    comment = Comment.objects.get(pk=comment_pk)
    if request.user == comment.user:
        comment.delete()
    return redirect('products:detail', product_pk)

@login_required
def likes(request, product_pk):
    product = Product.objects.get(pk=product_pk)
    if product.like_users.filter(pk=request.user.pk).exists():
        product.like_users.remove(request.user)
    else:
        product.like_users.add(request.user)
    return redirect('products:index', product_pk)

