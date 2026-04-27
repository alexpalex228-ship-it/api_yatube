from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import gettext_lazy as _

User = get_user_model()


class Group(models.Model):
    """Модель группы для объединения постов."""

    title = models.CharField(
        _('название'),
        max_length=200,
        help_text=_('Название группы (максимум 200 символов)')
    )
    slug = models.SlugField(
        _('уникальный идентификатор'),
        unique=True,
        help_text=_('Уникальный идентификатор группы в URL')
    )
    description = models.TextField(
        _('описание'),
        help_text=_('Подробное описание группы')
    )

    class Meta:
        verbose_name = _('группа')
        verbose_name_plural = _('группы')
        ordering = ('title',)

    def __str__(self):
        return self.title


class Post(models.Model):
    """Модель поста пользователя."""

    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name=_('автор'),
        related_name='posts',
        help_text=_('Автор поста')
    )
    group = models.ForeignKey(
        Group,
        on_delete=models.SET_NULL,
        verbose_name=_('группа'),
        blank=True,
        null=True,
        related_name='posts',
        help_text=_('Группа, к которой относится пост')
    )

    text = models.TextField(
        _('текст'),
        help_text=_('Текст поста')
    )
    pub_date = models.DateTimeField(
        _('дата публикации'),
        auto_now_add=True,
        db_index=True,
        help_text=_('Дата и время публикации поста')
    )
    image = models.ImageField(
        _('изображение'),
        upload_to='posts/',
        blank=True,
        null=True,
        help_text=_('Изображение для поста')
    )

    class Meta:
        verbose_name = _('пост')
        verbose_name_plural = _('посты')
        ordering = ('-pub_date',)

    def __str__(self):
        return _('Пост от {author}, {date}').format(
            author=self.author.username,
            date=self.pub_date.strftime('%Y-%m-%d')
        )


class Comment(models.Model):
    """Модель комментария к посту."""

    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name=_('автор'),
        related_name='comments',
        help_text=_('Автор комментария')
    )
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        verbose_name=_('пост'),
        related_name='comments',
        help_text=_('Пост, к которому относится комментарий')
    )

    text = models.TextField(
        _('текст'),
        help_text=_('Текст комментария')
    )
    created = models.DateTimeField(
        _('дата создания'),
        auto_now_add=True,
        db_index=True,
        help_text=_('Дата и время создания комментария')
    )

    class Meta:
        verbose_name = _('комментарий')
        verbose_name_plural = _('комментарии')
        ordering = ('created',)

    def __str__(self):
        return _('Комментарий от {author} к посту {post_id}').format(
            author=self.author.username,
            post_id=self.post.id
        )
