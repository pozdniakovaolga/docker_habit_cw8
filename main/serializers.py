from rest_framework import serializers

from main.models import Place, Reward, Habit
from rest_framework.serializers import ValidationError


class PlaceSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Место"""

    class Meta:
        model = Place
        fields = '__all__'


class RewardSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Вознаграждение"""

    class Meta:
        model = Reward
        fields = '__all__'


class HabitCreateUpdateSerializer(serializers.ModelSerializer):
    """Сериализатор для создания и редактирования модели Привычка"""
    # фильтрация списка для поля reward_with_pleasing_habit: только привычки с признаком приятной привычки
    reward_with_pleasing_habit = serializers.PrimaryKeyRelatedField(queryset=Habit.objects.filter(is_pleasing_habit=True), allow_null=True)

    class Meta:
        model = Habit
        fields = '__all__'

    def validate(self, attrs):
        is_pleasing = attrs.get('is_pleasing_habit')
        reward1 = attrs.get('reward_with_action')
        reward2 = attrs.get('reward_with_pleasing_habit')
        duration = attrs.get('duration')
        period = attrs.get('period')

        if not is_pleasing:  # если привычка полезная
            if reward1 and reward2:
                raise ValidationError('Может быть выбрано только одно вознаграждение')
            elif not reward1 and not reward2:
                raise ValidationError('Укажите вознаграждение для полезной привычки')
        elif is_pleasing:  # если привычка приятная
            if reward1 or reward2:
                raise ValidationError('У приятной привычки не может быть вознаграждения')

        if duration > 120:
            raise ValidationError('Время выполнения привычки не должно превышать 120 секунд')

        if period > 7:
            raise ValidationError('Привычку необходимо выполнять не реже, чем 1 раз в 7 дней')

        return attrs


class HabitSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Привычка"""

    class Meta:
        model = Habit
        fields = '__all__'
