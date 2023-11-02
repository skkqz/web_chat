from django.urls import path
from .views import ChatView, IndexView


app_name = 'chat'

urlpatterns = [
    path('', IndexView.as_view(), name='home'),
    path('<str:username>/', ChatView.as_view(), name='chat')
]
