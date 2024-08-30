import time


def get_tag_config(config, wanted_config: str, default: str):
    if config is not None and wanted_config in config:
        return str(config[wanted_config])
    else:
        return default


def get_tag_config_boolean(config, wanted_config: str, default: str):
    if config is not None and wanted_config in config:
        return str(int(config[wanted_config] is True))
    else:
        return default


def get_tag_config_date(config, wanted_config: str, default: str):
    dateFormat = '%d-%m-%Y %H:%M'
    if config is not None and wanted_config in config:
        parsed_time = time.strptime(config[wanted_config], dateFormat)
        timestamp = time.mktime(parsed_time)
        return str(timestamp)
    else:
        return default


class Config_utils:
    pass
