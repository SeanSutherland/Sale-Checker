from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .views import (
    ItemListView,
    ItemDetailView,
    ItemCreateView,
    ItemUpdateView,
    ItemDeleteView,
    UserItemListView,
)
from . import views

urlpatterns = [
    path('', views.home, name='sales-home'),
    #path('user/<str:username>', UserItemListView.as_view(), name='user-items'),
    path('item/<int:pk>/', ItemDetailView.as_view(), name='item-detail'),
    path('item/new/', ItemCreateView.as_view(), name='item-create'),
    path('item/<int:pk>/update/', ItemUpdateView.as_view(), name='item-update'),
    path('item/<int:pk>/delete/', ItemDeleteView.as_view(), name='item-delete'),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
