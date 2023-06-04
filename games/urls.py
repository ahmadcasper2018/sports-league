from game.api.views import GameViewSet
from rest_framework.routers import SimpleRouter

router = SimpleRouter()
router.register("", GameViewSet, basename="game")

urlpatterns = router.urls
