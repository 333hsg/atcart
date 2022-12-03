from django.shortcuts import render
from django.http import HttpResponse
from .models import Product, Orders
from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import get_template
from xhtml2pdf import pisa
import json
import math
# templateshub.net
# Create your views here.


def index(request):
    products = Product.objects.all()
    for j in products:
        if j.desc1 == "0":
            j.desc1 = ""
        if j.desc2 == "0":
            j.desc2 = ""
        if j.desc3 == "0":
            j.desc3 = ""
        if j.save_rs == "n":
            j.save_rs = j.actual_price - j.discount_price
        j.save()
    products = Product.objects.exclude(subcategories="0")
    p = products.filter(categories="Dry Fruits")
    a = getcategories(products)
    l = []
    for i in a:
        if i == "Dry Fruits":
            continue
        l.append(products.filter(categories=i))
    n = len(products)
    print(l)
    k = []
    for sss in a:
        if sss == "Dry Fruits":
            continue
        k.append(sss)
        p = p.order_by('product_name')
    params = {'range': range(n), 'product': p,
              'categories': k, 'other': l, 'selected': "Dry Fruits"}
    if request.method == "POST":
        k.append("Dry Fruits")
        cate = request.POST.get('cate', '')
        if cate != "Dry Fruits":
            s = products.filter(categories=cate)
        else:
            s = products.filter(categories="Dry Fruits")
        k.remove(cate)
        s = s.order_by('product_name')
        params = {'range': range(n), 'product': s,
                  'categories': k, 'other': l, 'selected': cate}
    return render(request, 'shop/nhome.html', params)


def searchmatch(query, item):
    query = query.lower()
    if query in (item.desc1).lower() or query in (item.desc2).lower() or query in (item.desc3).lower() or query in (item.product_name).lower() or query in (item.categories).lower() or query in (item.hidden).lower():
        return True
    return False


def search(request):
    query = request.GET.get('search')
    # allProds = []
    # catprods = Product.objects.values('category', 'id')
    # cats = {item['category']} for item in catprods}
    # for cat in cats:
    #    prodtemp = Product.objects.filter(category=cat)
    #    n = len(prod)
    #    allProds.append(prod)
    # params = {'range': range(n), 'product': allprods}
    products = Product.objects.exclude(subcategories="0")
    results = [item for item in products if searchmatch(query, item)]
    n = len(products)
    print(len(results))
    isempty = False
    if len(results) == 0:
        isempty = True
    print(isempty)
    a = getcategories(products)
    l = []
    for i in a:
        l.append(products.filter(categories=i))
    n = len(products)
    print(l)
    k = []
    for sss in a:
        k.append(sss)
    kl = []
    nn = 0
    for i in products:
        if i in results:
            continue
        kl.append(i)
        if nn >= 9:
            break
        nn += 1

    productsss = Product.objects.exclude(subcategories="0")
    cat_l = []
    cat_l.append("All Products")
    cat_l += getcategories(productsss)
    params = {'range': range(n), 'product': results, 'isempty': isempty,
              'categories': k, 'other': kl, 'selected': "All", 'c': cat_l}
    if request.method == "POST":
        k.append("All")
        cate = request.POST.get('cate', '')
        if cate != "All":
            s = products.filter(categories=cate)
        else:
            s = Product.objects.exclude(subcategories="0")
        k.remove(cate)
        params = {'range': range(n), 'product': s,
                  'categories': k, 'other': kl, 'selected': cate, 'c': cat_l}
    print(cat_l)
    return render(request, 'shop/nsearch.html', params)


def cart(request):
    productsss = Product.objects.exclude(subcategories="0")
    cat_l = []
    cat_l.append("All Products")
    cat_l += getcategories(productsss)
    params = {'categories': cat_l}
    return render(request, 'shop/ncart.html', params)


def orderplaced(request):
    productsss = Product.objects.exclude(subcategories="0")
    cat_l = []
    cat_l.append("All Products")
    cat_l += getcategories(productsss)
    params = {'categories': cat_l}
    return render(request, 'shop/order-placed.html', params)


def getcategories(products):
    categories = set()
    for i in products:
        categories.add(i.categories)
    return list(categories)


def checkout(request):
    if request.method == "POST":
        x = request.POST.get('items_json', '')
        y = request.POST.get('total-amt', '')
        a = list(json.loads(x).values())
        print(a)
        b = ""
        for i in a:
            b += str(i[0]) + " "
            b += str(i[1]) + " "
            b += str(i[2]) + " "
            b += "$"
        print(b)
        name = request.POST.get('name', '')
        email = request.POST.get('email', '')
        address = request.POST.get('address1', '') + \
            " " + request.POST.get('address2', '')
        city = request.POST.get('city', '')
        state = request.POST.get('state', '')
        zip_code = request.POST.get('zip_code', '')
        phone = request.POST.get('phone', '')

        subject = "Order from " + name
        rec = "at.pvt.in@gmail.com"
        content = name + '\n' + phone + '\n' + b + '\n' + address + '\n' + y

        order = Orders(items_json=b, name=name, email=email,
                       address=address, zip_code=zip_code, phone=phone, total=y)
        order.save()
        #send_mail(
        #    subject,
        #    content,
        #    settings.EMAIL_HOST_USER,
        #    [rec]
        #)
        thank = True
        id = order.order_id
        return render(request, 'shop/checkout.html', {'thank': thank, 'id': id, 'jj': b})
    return render(request, 'shop/checkout.html')


def ordersforadmin(request):
    ord = Orders.objects.order_by('order_id').all().reverse()

    l = []
    for k in ord:
        l.append("Order No: "+str(k.order_id))
        l.append("Name: "+str(k.name))
        l.append("Address: "+str(k.address))
        l.append("Total: "+str(k.total))
        a = k.items_json
        kk = []
        while(len(a) > 0):
            b = a.index("$")
            l.append(a[:b])
            a = a[b + 1:]
        l.append(" ")
    authorised = False
    if request.method == "POST":
        uname = request.POST.get('username', '')
        pword = request.POST.get('password', '')
        if uname == "at" and pword == "0802$Sss":
            authorised = True
        # o_id = request.POST.get('o_id','')
        # status = request.POST.get('status','')
        # print(o_id)
    return render(request, 'shop/ordersforadmin.html', {'authorised': authorised, 'orders': ord, 'ooo': l, 'oo': kk})


def productv(request, mid):
    prod = Product.objects.filter(id=mid)
    cate = prod[0].categories
    productss = Product.objects.filter(categories=cate)
    productss = productss.exclude(subcategories="0")
    x = productss.exclude(id=mid)
    sh = []
    nn = 1
    for i in x:
        if nn > 10:
            break
        sh.append(i)
    print(prod)
    others = Product.objects.filter(product_name=prod[0].product_name)
    others = others.exclude(id=prod[0].id)
    products = Product.objects.exclude(subcategories="0")
    a = []
    a.append("All Products")
    a += getcategories(products)
    return render(request, 'shop/nnnproduct.html', {'prod': prod[0], 'all': sh, 'others': others, 'categories': a})


def invoice(request, oid):
    class Items:

        def __init__(self, sr, pcs, prod, price, total, s1, s2, s3, s4):
            self.sr = sr
            self.pcs = pcs
            self.prod = prod
            self.price = price
            self.total = total
            self.s1 = s1
            self.s2 = s2
            self.s3 = s3
            self.s4 = s4
    items = Orders.objects.filter(order_id=oid)
    pname = items[0].name
    items = str(items[0].items_json)
    items = items.split("$")
    items.pop(-1)
    k = []
    sr = 1
    totall = 0
    for i in items:
        b = i.split()
        lenn = len(b) - 1
        pcs = b[0]
        price = b[-1]
        prod_desc = " ".join(b[1:lenn])
        print(pcs, prod_desc, price)
        total = int(b[0]) * int(b[-1])
        b.append(total)
        s1 = str(" " * (10 - len(str(sr))))
        s2 = str(" " * (124 - len(prod_desc)))
        s3 = str(" " * (13 - len(pcs)))
        s4 = str(" " * (10 - len(price)))
        k.append(Items(sr, pcs, prod_desc, price, total, s1, s2, s3, s4))
        sr += 1
        totall += total

    template_path = 'shop/invoice.html'
    context = {'arr': k, 'total': totall, 'name': pname, 'oid': oid}
    # Create a Django response object, and specify content_type as pdf
    response = HttpResponse(content_type='application/pdf')
    # attachment; filename="invoice.pdf"
    response['Content-Disposition'] = 'attachment; filename="invoice.pdf"'
    # find the template and render it.
    template = get_template(template_path)
    html = template.render(context)

    # create a pdf
    pisa_status = pisa.CreatePDF(
        html, dest=response)
    # if error then show some funy view
    if pisa_status.err:
        return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response


def categories(request):
    products = Product.objects.exclude(subcategories="0")
    a = []
    a.append("All Products")
    a += getcategories(products)

    params = {'categories': a}
    return render(request, 'shop/category_home.html', params)


def scategories(request, cat):
    products = Product.objects.exclude(subcategories="0")
    a = []
    a.append("All Products")
    a += getcategories(products)
    a.remove(cat)
    if cat != "All Products":
        products = products.filter(categories=cat)

    params = {'product': products, 'categories': a, 'selected': cat}
    return render(request, 'shop/nhome.html', params)
