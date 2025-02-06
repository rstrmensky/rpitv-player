import logging
from configparser import ConfigParser

# Load settings.ini configuration
settings_conf = ConfigParser()
settings_conf.read('conf/settings.ini')

# Create loger
log = logging.getLogger('RPiTV')
log.setLevel(logging.DEBUG)

# Create handlers
app_handler = logging.FileHandler(settings_conf['SETTINGS']['log_app'])
app_handler.setLevel(logging.DEBUG)

error_handler = logging.FileHandler(settings_conf['SETTINGS']['log_error'])
error_handler.setLevel(logging.ERROR)

# Create formaters
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
app_handler.setFormatter(formatter)
error_handler.setFormatter(formatter)

# Add handlers
log.addHandler(app_handler)
log.addHandler(error_handler)

# Add filters to exclude ERROR and higher levels
app_handler.addFilter(lambda record: record.levelno < logging.ERROR)
