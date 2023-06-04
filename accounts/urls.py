from rest_framework.routers import SimpleRouter

from accounts.api.views import UserViewSet

router = SimpleRouter()

router.register("", UserViewSet, basename="user")

urlpatterns = router.urls
