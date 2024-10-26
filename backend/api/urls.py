from django.urls import path
from . import views
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView


urlpatterns = [
    path('', views.get_routes),
    path('clients/', views.get_clients),
    path('intents/', views.get_intents),
    path('clients/create/', views.create_client, name='create_client'),
    path('intents/create/', views.create_intent, name='create_intent'),
    path('intents/delete/<int:id>/', views.delete_intent, name='delete_intent'),
    path('clients/delete/<int:id>/', views.delete_client, name='delete_client'),
    
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]