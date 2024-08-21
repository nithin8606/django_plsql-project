from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from.import views

urlpatterns = [
    path('',views.view_users,name='view_users'),
    path('add_users',views.add_users,name='add_users'),
    path('update_users/<int:id>',views.update_users,name='update_users'),
    path('delete_users/<int:id>',views.delete_users,name='delete_users'),

]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)