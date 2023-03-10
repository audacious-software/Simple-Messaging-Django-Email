# pylint: disable=line-too-long

from django.conf import settings
from django.core.checks import Warning, register # pylint: disable=redefined-builtin

@register()
def check_email_settings_defined(app_configs, **kwargs): # pylint: disable=unused-argument
    errors = []

    if hasattr(settings, 'SIMPLE_MESSAGING_DEFAULT_FROM_ADDRESS') is False:
        warning = Warning('SIMPLE_MESSAGING_DEFAULT_FROM_ADDRESS parameter not defined', hint='Update configuration to include SIMPLE_MESSAGING_DEFAULT_FROM_ADDRESS.', obj=None, id='simple_messaging_email.W001')
        errors.append(warning)

    if hasattr(settings, 'SIMPLE_MESSAGING_DEFAULT_SUBJECT') is False:
        warning = Warning('SIMPLE_MESSAGING_DEFAULT_SUBJECT parameter not defined', hint='Update configuration to include SIMPLE_MESSAGING_DEFAULT_SUBJECT.', obj=None, id='simple_messaging_email.W002')
        errors.append(warning)

    return errors
