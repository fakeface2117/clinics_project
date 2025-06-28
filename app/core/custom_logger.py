import logging.config

STDOUT_FORMAT = '%(log_color)s[%(asctime)s] - [%(levelname)s] - %(filename)s:%(lineno)d - %(message)s'

LOGGING_CONFIG = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            '()': 'colorlog.ColoredFormatter',
            'log_colors': {
                'DEBUG': 'cyan',
                'INFO': 'blue',
                'WARNING': 'yellow',
                'ERROR': 'red',
                'CRITICAL': 'bold_red',
            },
            'format': '%(log_color)s[%(asctime)s] - [%(levelname)s] - %(filename)s:%(lineno)d - %(message)s',
            'datefmt': '%Y-%m-%d %H:%M:%S'
        }
    },
    'handlers': {
        'console': {
            'formatter': 'verbose',
            'class': 'logging.StreamHandler',
            'stream': 'ext://sys.stdout',
        }
    },
    'loggers': {
        'root': {
            'handlers': ['console'],
            'level': 'INFO',
        },
        'uvicorn.access': {
            'handlers': ['console'],
            'level': 'INFO'
        },
    }
}

logging.config.dictConfig(LOGGING_CONFIG)
logger = logging.getLogger(__name__)
