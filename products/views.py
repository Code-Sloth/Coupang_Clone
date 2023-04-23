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
        images = ProductImage.objects.filter(product=product)
        if images:
            product_images.append((product, images[0]))
        else:
            product_images.append((product, ''))
    
    context = {
        'product_images': product_images,
        'sor': None,
        'cate': None,
        'sta': None,
        'pri': None,
        'query1': '',
        'query2': '',
        'searchdata': '',
    }
    return render(request, 'products/index.html',context)

def search(request):
    query = request.GET.get('base-query','')
    category = request.GET.get('base-category')

    if category != '전체':
        products = Product.objects.filter(category=category)
    else:
        products = Product.objects.all()

    if query:
        products = products.filter(
            Q(title__icontains=query)|
            Q(content__icontains=query)|
            Q(category__icontains=query)|
            Q(delivery__icontains=query)
        )

    product_images = []
    for product in products:
        images = ProductImage.objects.filter(product=product)
        if images:
            product_images.append((product, images[0]))
        else:
            product_images.append((product, ''))
    
    context = {
        'product_images': product_images,
        'cate': category,
        'sor' : None,
        'sta' : None,
        'pri' : None,
        'query1' : '',
        'query2' : '',
        'searchdata': query,
    }
    return render(request, 'products/index.html',context)

def filtering(request, category=None, sort=None, star=None, price=None):
    products = Product.objects.all()
    q1 = request.GET.get('q1')
    q2 = request.GET.get('q2')

    if category != 'None':
        products = func_category(category)
  
    if sort != 'None':
        products = func_sort(sort, products)
    
    if star != 'None':
        products = func_star(star, products)

    if q1 and q2:
        products = func_price_search(q1, q2, products)
        price = 'None'
    else:
        q1 = ''
        q2 = ''
    
    if price != 'None':
        products = func_price(price, products)
        
    
   
    product_images = []
    for product in products:
        images = ProductImage.objects.filter(product=product)
        if images:
            product_images.append((product, images[0]))
        else:
            product_images.append((product, ''))

    context = {
        'product_images': product_images,
        'cate': category,
        'sor' : sort,
        'sta' : star,
        'pri' : price,
        'query1' : q1,
        'query2' : q2,
        'searchdata' : '',
    }
    return render(request, 'products/index.html',context)

def func_category(c):
    if c == 'c_avenue':
        return Product.objects.filter(c_avenue = True)
    elif c == '무료배송':
        return Product.objects.filter(free_shipping = True)
    else:
        return Product.objects.filter(
            Q(category = c)|
            Q(delivery = c)
        )

def func_sort(s, queryset):
    if s == '최신순':
        return queryset.order_by('-pk')
    elif s == '별점순':
        return queryset.order_by('-star')
    elif s == '할인순':
        return queryset.order_by('-discount_rate')
    elif s == '낮은가격순':
        return queryset.order_by('discounted_price')
    elif s == '높은가격순':
        return queryset.order_by('-discounted_price')

def func_star(st, queryset):
    if st == '4':
        return queryset.filter(star__gte=4)
    elif st == '3':
        return queryset.filter(star__gte=3)
    elif st == '2':
        return queryset.filter(star__gte=2)
    elif st == '1':
        return queryset.filter(star__gte=1)
    else:
        return queryset
        
def func_price(p, queryset):
    if p == '1만원 미만':
        return queryset.filter(discounted_price__lt=10000)
    if p == '1만원~2만원':
        return queryset.filter(discounted_price__lt=20000, discounted_price__gte=10000)
    if p == '2만원~3만원':
        return queryset.filter(discounted_price__lt=30000, discounted_price__gte=20000)
    if p == '3만원~4만원':
        return queryset.filter(discounted_price__lt=40000, discounted_price__gte=30000)
    if p == '4만원 이상':
        return queryset.filter(discounted_price__gte=40000)
    else:
        return queryset
    
def func_price_search(q1, q2, queryset):
    return queryset.filter(discounted_price__lte=q2, discounted_price__gte=q1)

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
            return redirect('products:detail', f.pk)
        else:
            print(form.errors)
    else:
        product_form = ProductForm()
        image_form = ProductImageForm()
    context = {'product_form': product_form, 'image_form':image_form,}
    return render(request, 'products/create.html', context)

def update_product_star(sender, instance, **kwargs):
    product = instance.product
    comments = Comment.objects.filter(product=product)
    star_sum = sum([comment.star for comment in comments])
    star_avg = star_sum / comments.count()
    product.star = star_avg
    product.save()

def detail(request, product_pk):
    product = Product.objects.get(pk=product_pk)
    comments = product.comment_set.all()

    if comments:
        star_sum = sum([comment.star for comment in comments])
        star_avg = star_sum / comments.count()
        product.star = round(star_avg,1)
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


