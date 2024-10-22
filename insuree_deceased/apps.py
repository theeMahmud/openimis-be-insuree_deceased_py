from django.apps import AppConfig

DEFAULT_CONFIG = {
    "insuree_deceased_create": ["101102"],
    "insuree_deceased_update": ["101103"],
    "insuree_deceased_delete": ["101104"],
    "insuree_deceased_search": ["101101"],
}

class InsureeDeceasedConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'insuree_deceased'

    insuree_deceased_create = []
    insuree_deceased_update = []
    insuree_deceased_delete = []
    insuree_deceased_search = []

    def ready(self):
        from core.models import ModuleConfiguration
        cfg = ModuleConfiguration.get_or_default(self.name, DEFAULT_CONFIG)
        self.__load_config(cfg)

    @classmethod
    def __load_config(cls, cfg):
        """
        Load all config fields that match current AppConfig class fields, all custom fields have to be loaded separately
        """
        for field in cfg:
            if hasattr(InsureeDeceasedConfig, field):
                setattr(InsureeDeceasedConfig, field, cfg[field])
