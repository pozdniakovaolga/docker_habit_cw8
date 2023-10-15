from django.db import models


class Place(models.Model):
    """Место """
    title = models.CharField(max_length=20, verbose_name='название')
    created_by = models.ForeignKey('users.User', on_delete=models.CASCADE, null=True, blank=True, verbose_name='автор')

    def __str__(self):
        return f'Место: {self.title}'

    class Meta:
        verbose_name = 'место'
        verbose_name_plural = 'места'


class Reward(models.Model):
    """Вознаграждение действием"""
    title = models.CharField(max_length=100, verbose_name='название')
    created_by = models.ForeignKey('users.User', on_delete=models.CASCADE, null=True, blank=True, verbose_name='автор')

    def __str__(self):
        return f'Вознаграждение: {self.title}'

    class Meta:
        verbose_name = 'вознаграждение'
        verbose_name_plural = 'вознаграждения'


class Habit(models.Model):
    """Привычка """

    place = models.ForeignKey(Place, on_delete=models.SET_NULL, null=True, verbose_name='место выполнения')
    time = models.TimeField(verbose_name='время выполнения')
    action = models.CharField(max_length=250, verbose_name='действие')
    period = models.PositiveSmallIntegerField(default=1, verbose_name='периодичность выполнения в днях')
    duration = models.PositiveSmallIntegerField(verbose_name='продолжительность выполнения в секундах')
    is_public = models.BooleanField(default=False, verbose_name='признак публичности')
    is_pleasing_habit = models.BooleanField(default=False, verbose_name='признак приятной привычки')
    created_by = models.ForeignKey('users.User', on_delete=models.CASCADE, null=True, blank=True, verbose_name='автор')
    last_reminder = models.DateTimeField(null=True, blank=True, verbose_name='дата отправки последнего напоминания')
    #  варианты вознаграждения
    reward_with_action = models.ForeignKey(Reward, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='вознаграждение действием')
    reward_with_pleasing_habit = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, verbose_name='вознаграждение приятной привычкой')

    def __str__(self):
        return f'Привычка: {self.action} в {self.time} в {self.place}'

    class Meta:
        verbose_name = 'привычка'
        verbose_name_plural = 'привычки'
