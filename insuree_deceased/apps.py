from django.apps import AppConfig

MODULE_NAME = 'insuree_deceased'

DEFAULT_CFG = {
    "insuree_deceased_search": ["101101"],
    "insuree_deceased_create": ["101102"],
    "insuree_deceased_update": ["101103"],
    "insuree_deceased_delete": ["101104"],
}


class InsureeDeceasedConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = MODULE_NAME

    insuree_deceased_search = None

    insuree_deceased_create = None
    insuree_deceased_update = None
    insuree_deceased_delete = None

    @classmethod
    def __load_config(self, cfg):
        for field in cfg:
            if hasattr(InsureeDeceasedConfig, field):
                setattr(InsureeDeceasedConfig, field, cfg[field])

    def ready(self):
        from core.models import ModuleConfiguration
        cfg = ModuleConfiguration.get_or_default(MODULE_NAME, DEFAULT_CFG)
        self.__load_config(cfg)
