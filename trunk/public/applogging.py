#!/usr/bin/env python
# coding=utf-8
import public.config as config

if config.DEPLOY_ENV == 'bae':
    from bae.api import logging
else:
    import logging

logger = logging.getLogger('soulife')


def critical(msg):
    logger.critical(msg)

def error(msg):
    logger.error(msg)

def warning(msg):
    logger.warning(msg)

def info(msg):
    logger.info(msg)
    
def debug(msg):
    logger.debug(msg)

def exception(msg):
    logger.exception(msg)

