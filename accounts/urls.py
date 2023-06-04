from account.api.views import UserViewSet
from rest_framework.routers import SimpleRouter

router = SimpleRouter()

router.register("", UserViewSet, basename="user")

urlpatterns = router.urls
