from django.urls import path
# from rest_framework.urlpatterns import format_suffix_patterns
from . import views #manage_items, manage_item

app_name = 'api'
urlpatterns = [
    path('', views.get_all, name="get_all"),
    path('<slug:key>', views.item, name="item")
]
# urlpatterns = format_suffix_patterns(urlpatterns)
# </slug:key>