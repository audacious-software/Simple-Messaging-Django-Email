# pylint: disable=line-too-long, no-member

import json
import os
import re

from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template import Template, Context

EMAIL_REGEX = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'

def process_outgoing_message(outgoing_message, metadata=None): # pylint: disable=too-many-branches, too-many-locals
    if metadata is None:
        metadata = {}

    destination = outgoing_message.current_destination()

    if re.fullmatch(EMAIL_REGEX, destination):
        transmission_metadata = {}

        if outgoing_message.transmission_metadata is not None:
            try:
                transmission_metadata = json.loads(outgoing_message.transmission_metadata)
            except ValueError:
                transmission_metadata = {}

            outgoing_message_content = outgoing_message.fetch_message(transmission_metadata)

            outgoing_message_subject = transmission_metadata.get('email_subject', settings.SIMPLE_MESSAGING_DEFAULT_SUBJECT)

            from_address = transmission_metadata.get('email_from_address', settings.SIMPLE_MESSAGING_DEFAULT_FROM_ADDRESS)

            cc_addresses = transmission_metadata.get('email_cc_addresses', [])
            bcc_addresses = transmission_metadata.get('email_bcc_addresses', [])

            email = EmailMultiAlternatives(outgoing_message_subject, outgoing_message_content, from_address, [destination], cc=cc_addresses, bcc=bcc_addresses)

            html_content = transmission_metadata.get('email_html_content', None)

            if html_content is not None:
                template = Template(html_content)

                context = Context(transmission_metadata)

                html_content = template.render(context)

                email.attach_alternative(html_content, 'text/html')

            for outgoing_file in outgoing_message.media.all().order_by('index'):
                base_name = os.path.basename(outgoing_file.content_file.path)

                with outgoing_file.content_file.open('rb') as file_contents:
                    email.attach(base_name, file_contents.read(), outgoing_file.content_type)

            email.send()

            return metadata

    return None

def simple_messaging_media_enabled(outgoing_message): # pylint: disable=unused-argument
    destination = outgoing_message.current_destination()

    return re.fullmatch(EMAIL_REGEX, destination)

# def process_incoming_request(request): # pylint: disable=unused-argument
#    return HttpResponse('Not implemented', status_code=501, content_type='text/plain')
