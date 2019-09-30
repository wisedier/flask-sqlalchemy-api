import os

from config import settings

__all__ = (
    'config',
)

env = os.environ.get('ENV', 'DEVELOPMENT')
config = None
if env == 'TEST':
    config = settings.TestConfig()
elif env == 'DEVELOPMENT':
    config = settings.DevelopmentConfig()
elif env == 'STAGING':
    config = settings.StagingConfig()
elif env == 'PRODUCTION':
    config = settings.ProductionConfig()
else:
    raise EnvironmentError(f'ENV={env} is invalid environment setting.')
