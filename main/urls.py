from django.urls import path

from main.apps import MainConfig
from main.views import PlaceViewSet, RewardViewSet, HabitListAPIView, HabitCreateAPIView, HabitRetrieveAPIView, \
    HabitUpdateAPIView, HabitDestroyAPIView, PublicHabitListAPIView
from rest_framework.routers import DefaultRouter

app_name = MainConfig.name

router = DefaultRouter()
router.register(r'place', PlaceViewSet, basename='place')
router.register(r'reward', RewardViewSet, basename='reward')


urlpatterns = [
    path('habit/', HabitListAPIView.as_view(), name='habit_list'),
    path('public_habit/', PublicHabitListAPIView.as_view(), name='public_habit_list'),
    path('habit/create/', HabitCreateAPIView.as_view(), name='habit_create'),
    path('habit/<int:pk>/', HabitRetrieveAPIView.as_view(), name='habit_get'),
    path('habit/update/<int:pk>/', HabitUpdateAPIView.as_view(), name='habit_update'),
    path('habit/delete/<int:pk>/', HabitDestroyAPIView.as_view(), name='habit_delete'),
] + router.urls
