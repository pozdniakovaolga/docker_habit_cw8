from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, generics
from rest_framework.generics import CreateAPIView, DestroyAPIView
from rest_framework.permissions import IsAuthenticated

from main.models import Place, Reward, Habit
from main.paginators import PagePagination
from main.permissions import IsOwner, IsPublic
from main.serializers import PlaceSerializer, RewardSerializer, HabitSerializer, HabitCreateUpdateSerializer


class PlaceViewSet(viewsets.ModelViewSet):
    """ViewSet для модели Место"""
    serializer_class = PlaceSerializer
    queryset = Place.objects.all()
    permission_classes = [IsAuthenticated, IsOwner]

    def perform_create(self, serializer):  # автоматическое сохранение автора места
        new_place = serializer.save()
        new_place.created_by = self.request.user
        new_place.save()

    def get_queryset(self):
        queryset = Place.objects.filter(created_by=self.request.user)
        return queryset


class RewardViewSet(viewsets.ModelViewSet):
    """ViewSet для модели Вознаграждение"""
    serializer_class = RewardSerializer
    queryset = Reward.objects.all()
    permission_classes = [IsAuthenticated, IsOwner]

    def perform_create(self, serializer):  # автоматическое сохранение автора вознаграждения
        new_reward = serializer.save()
        new_reward.created_by = self.request.user
        new_reward.save()

    def get_queryset(self):
        queryset = Reward.objects.filter(created_by=self.request.user)
        return queryset


class HabitCreateAPIView(CreateAPIView):
    """Контроллер создания привычки"""
    serializer_class = HabitCreateUpdateSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):

        new_habit = serializer.save()  # автоматическое сохранение автора привычки
        new_habit.created_by = self.request.user
        new_habit.save()


class HabitListAPIView(generics.ListAPIView):
    """Контроллер просмотра списка привычек пользователя"""
    serializer_class = HabitSerializer
    queryset = Habit.objects.all()
    pagination_class = PagePagination
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['place', 'is_pleasing_habit', 'is_public']
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = Habit.objects.filter(created_by=self.request.user)
        return queryset


class PublicHabitListAPIView(generics.ListAPIView):
    """Контроллер просмотра списка публичных привычек"""
    serializer_class = HabitSerializer
    queryset = Habit.objects.all()
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = Habit.objects.filter(is_public=True)
        return queryset


class HabitRetrieveAPIView(generics.RetrieveAPIView):
    """Контроллер просмотра конкретной привычки"""
    serializer_class = HabitSerializer
    queryset = Habit.objects.all()
    permission_classes = [IsAuthenticated, IsOwner | IsPublic]


class HabitUpdateAPIView(generics.UpdateAPIView):
    """Контроллер редактирования привычки"""
    serializer_class = HabitCreateUpdateSerializer
    queryset = Habit.objects.all()
    permission_classes = [IsAuthenticated, IsOwner]


class HabitDestroyAPIView(DestroyAPIView):
    """Контроллер удаления привычки"""
    serializer_class = HabitSerializer
    queryset = Habit.objects.all()
    permission_classes = [IsAuthenticated, IsOwner]
