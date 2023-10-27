from django.urls import path
from .views import ChatView, IndexView


urlpatterns = [
    path('', IndexView.as_view(), name='home'),
    path('<str:username>/', ChatView.as_view(), name='chat')
]
