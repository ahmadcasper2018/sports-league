from decouple import config
import os

env = config(
    "ENVIRONMENT", default="dev"
)  # Get current environment, defaulting to 'dev'

if env == "dev":
    print("Using dev environment...")
    from .dev import *
elif env == "production":
    print("Using production environment...")
    from .production import *
else:
    raise ValueError("Invalid environment specified.")

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "myproject.settings")
