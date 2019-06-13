from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.contrib.auth.models import UserManager
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from caching.base import CachingMixin, CachingManager
from othello_utils.models import generate_uniq_slug


class OthelloUserManager(UserManager, CachingManager):
    """オセロユーザーマネージャー

    """


class OthelloUser(AbstractBaseUser, PermissionsMixin, CachingMixin):
    """オセロユーザー

    """

    SLUG_LENGTH = 20
    objects = OthelloUserManager()

    username = models.CharField(
        verbose_name=_('username'), max_length=150, blank=True
    )
    email = models.EmailField(_('email address'), unique=True)
    slug = models.CharField(
        verbose_name=_('slug'),
        unique=True,
        max_length=SLUG_LENGTH,
        blank=False,
        null=False,
    )

    is_staff = models.BooleanField(
        _('staff status'),
        default=False,
        help_text=_(
            'Designates whether the user can log into this admin site.'),
    )
    is_active = models.BooleanField(
        _('active'),
        default=True,
        help_text=_(
            'Designates whether this user should be treated as active. '
            'Unselect this instead of deleting accounts.'
        ),
    )
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        base_manager_name = 'objects'

    def __str__(self) -> str:
        return self.username

    @classmethod
    def _pre_save_handler(cls, sender, instance, raw, **kwargs):
        """
        保存直前処理
        """
        if instance.slug == '' or instance.slug is None:
            instance.slug = generate_uniq_slug(
                cls, 'slug', length=cls.SLUG_LENGTH
            )
