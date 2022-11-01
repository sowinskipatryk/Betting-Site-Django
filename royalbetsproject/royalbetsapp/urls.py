from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings
from django.urls import include

urlpatterns = [
    path('', views.index, name='index'),
    path('odds/', views.odds, name='odds'),
    path('table/', views.table, name='table'),
    path('results/', views.results, name='results'),
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
