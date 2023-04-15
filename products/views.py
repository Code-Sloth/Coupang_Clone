from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from .models import Product,Comment,ProductImage
from .forms import ProductForm,CommentForm,ProductImageForm,ProductImageFormSet
from django.db.models import Q
from django.http import HttpResponseRedirect
from PIL import Image
from django.conf import settings
import os
# import ModelViewSet
# from .serializers import ProductSerializer


# Create your views here.

def index(request):
    products = Product.objects.all()[::-1]
    return render(request, 'products/index.html',{'products':products})

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
        
        form = ProductForm(request.POST, request.FILES)
        g = []
        if form.is_valid():
            images = request.FILES.getlist('image')

            for image in images:
                img = Image.open(image)
                img = img.resize((800, 800))
                path = os.path.join(settings.MEDIA_ROOT, image.name)
                img.save(path)

            return redirect('products:index')

        return render(request, 'upload_images.html')
    else:
        form = ProductForm()
    return render(request, 'products/create.html',{'form':form})


def detail(request, product_pk):
    product = Product.objects.get(pk=product_pk)
    comment_form = CommentForm()
    # comments = Product.comment_set.all()
    product.save()

    context = {
        'product':product,
        'comment_form':comment_form,
        # 'comments':comments,
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
    if request.user == product.user:
        if request.method == 'POST':
            form = ProductForm(request.POST, request.FILES, instance=product)
            if form.is_valid():
                form.save()
                return redirect('products:detail', product_pk)
        else:
            form = ProductForm(instance=product)
        return render(request, 'products/update.html',{'form':form,'product':product})
    else:
        return redirect('products:detail', product_pk)

@login_required
def comment_create(request, product_pk):
    product = product.objects.get(pk=product_pk)
    comment_form = CommentForm(request.POST)
    if comment_form.is_valid():
        comment = comment_form.save(commit=False)
        comment.product = product
        comment.user = request.user
        comment.save()
        return redirect('products:detail', product.pk)
    context = {
        'product':product,
        'comment_form':comment_form
    }
    return render(request,'products/detail.html', context)

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