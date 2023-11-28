from django.conf import settings
from django.conf.urls import static
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from django.contrib.auth.views import LoginView
from django.urls import include, path
from rest_framework.authtoken.views import obtain_auth_token

from .views import *
from .views import register, user_login, user_logout

urlpatterns = [
    path('products/', product_list, name='product_list'),
    path('register/', register, name='register'),
    path('api-token-auth/', obtain_auth_token, name='api_token_auth'),
    path('api/products/', ProductList.as_view(), name='product_list'),
    # path('api/products/category/<int:category_id>/', ProductListByCategory.as_view(), name='product_list_by_category'),
    path('products/<int:product_id>/submit_review/', submit_review, name='submit_review'),
    path('update_profile/', update_profile, name='update_profile'),
    path('login/', user_login, name='user_login'),
    path('logout/', user_logout, name='user_logout'),
    path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    path('home/', home, name='home'),
    path('', LoginView.as_view(), name='login'),
    path('products_by_category/<int:category_id>/', render_category_products, name='render_category_products'),
    path("update_password/", update_password, name='update_password'),

]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

