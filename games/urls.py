from rest_framework.routers import SimpleRouter

from games.api.views import GameViewSet

router = SimpleRouter()
router.register("", GameViewSet, basename="game")

urlpatterns = router.urls
