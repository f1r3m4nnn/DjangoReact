from django.urls import path, include, re_path
from django.contrib import admin
from rest_framework import routers
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework.authtoken.views import obtain_auth_token
from core.views import ContactAPIView
from lojinha.views import ( 
                            OrderList,
                            OrderDetailList,
                            OrderDetailSingle,
                            OrderSingle,
                            Itemlist,
                            ItemSingle
)
from django.conf import settings
from django.conf.urls.static import static


schema_view = get_schema_view(
    openapi.Info(
        title="Vendinha® - API",
        default_version='v1',
        description="API de Aplicação - Tales S.",
        terms_of_service="https://routerlabs.io",
        contact=openapi.Contact(email="tales@routerlabs.io"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)


router = routers.DefaultRouter()


urlpatterns = [
    path('contact/', ContactAPIView.as_view(), name='contact'),
    path('items/', Itemlist.as_view(), name='items'),
    path('items/<uuid:id>/', ItemSingle.as_view(), name='item-single'),
    path('orders/', OrderList.as_view(), name='orders'),
    path('orders/<uuid:id>/', OrderSingle.as_view(), name='order-single'),
    path('orderdetails/', OrderDetailList.as_view(), name='order-details'),
    path('orderdetails/<uuid:id>/', OrderDetailSingle.as_view(), name='order-detail-single'),
    path('admin/', admin.site.urls),
    # path('', include('core.urls')),
    path('api-token-auth/', obtain_auth_token),
    re_path(r'^swagger(?P<format>\.json|\.yaml)$',
            schema_view.without_ui(cache_timeout=0), name='schema-json'),
    re_path(r'^swagger/$', schema_view.with_ui('swagger',
            cache_timeout=0), name='schema-swagger-ui'),
    re_path(r'^redoc/$', schema_view.with_ui('redoc',
            cache_timeout=0), name='schema-redoc'),
] + router.urls + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)