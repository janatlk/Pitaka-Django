from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    """Профиль пользователя"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name='Пользователь')
    phone = models.CharField('Телефон', max_length=20, blank=True)
    avatar = models.ImageField('Аватар', upload_to='avatars/', blank=True, null=True)
    created_at = models.DateTimeField('Дата регистрации', auto_now_add=True)
    
    class Meta:
        verbose_name = 'Профиль'
        verbose_name_plural = 'Профили'
    
    def __str__(self):
        return f"Профиль: {self.user.username}"


def create_user_profile(sender, instance, created, **kwargs):
    """Создание профиля при регистрации пользователя"""
    if created:
        Profile.objects.create(user=instance)


def save_user_profile(sender, instance, **kwargs):
    """Сохранение профиля при сохранении пользователя"""
    instance.profile.save()


from django.db.models.signals import post_save
post_save.connect(create_user_profile, sender=User)
post_save.connect(save_user_profile, sender=User)
