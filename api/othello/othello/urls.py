from django.contrib import admin
from django.contrib.admin.views.decorators import staff_member_required
from django.urls import path, re_path, include
from django.conf.urls.static import static
from django.conf import settings
from rest_framework import routers, permissions
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from othello_users.views import OthelloUserViewSets
from matchings.views import MatchingViewSets
from games.views import GameViewSets
import debug_toolbar


# DRF router settings

router = routers.DefaultRouter(trailing_slash=False)
router.register('othello_users', OthelloUserViewSets)
router.register('matchings', MatchingViewSets)
router.register('games', GameViewSets)

# DRF documents

schema_view = get_schema_view(
   openapi.Info(
      title='Othello API',
      default_version='v1',
   ),
   permission_classes=(permissions.AllowAny,),
   public=True
)


urlpatterns = [
    path('api/', include(router.urls)),
    re_path(
        'admin/swagger(?P<format>.json|.yaml)',
        staff_member_required(schema_view.without_ui(cache_timeout=None))
    ),
    path(
        'admin/swagger/',
        staff_member_required(schema_view.with_ui(
            'swagger', cache_timeout=None
        ))
    ),
    path(
        'admin/redoc/',
        staff_member_required(schema_view.with_ui('redoc', cache_timeout=None))
    ),
    path('admin/doc/', include('django.contrib.admindocs.urls')),
    path('admin/', admin.site.urls),
]


if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT
    )
    urlpatterns = [
        path('__debug__/', include(debug_toolbar.urls))
    ] + urlpatterns
