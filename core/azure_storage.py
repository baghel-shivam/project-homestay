from storages.backends.azure_storage import AzureStorage
from . import settings

class AzureMediaStorage(AzureStorage):
    account_name = settings.AZURE_ACCOUNT_NAME
    account_key = settings.AZURE_ACCOUNT_KEY
    azure_container = settings.AZURE_CONTAINER
    expiration_secs = None