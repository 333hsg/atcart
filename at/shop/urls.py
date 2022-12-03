from . import views
from django.urls import path

urlpatterns = [
    path("", views.categories, name="shopHome"),
    path("update", views.index, name="update"),
    path("cart/", views.cart, name="cart"),
    path("checkout/", views.checkout, name="checkout"),
    path("categories/", views.categories, name="categories"),
    path("categories/<str:cat>", views.scategories, name="scategories"),
    path("products/<int:mid>", views.productv, name="productv"),
    path("search/", views.search, name="search"),
    path("ordersforadmin/", views.ordersforadmin, name="ordersforadmin"),
    path("order-placed/", views.orderplaced, name="orderplaced"),
    path("order-placed/invoice/<int:oid>", views.invoice, name="invoice")
]
