from .views import CityViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'cities', CityViewSet, basename='city')
urlpatterns = router.urls
