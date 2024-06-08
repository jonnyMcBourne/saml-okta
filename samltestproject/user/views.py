from django.shortcuts import render

# Create your views here.
#  nueva vista para acs
from djangosaml2.views import AssertionConsumerServiceView
import logging

logger = logging.getLogger(__name__)

class CustomAssertionConsumerServiceView(AssertionConsumerServiceView):
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        if hasattr(self, 'context'):
            session_info = self.context.session_info()
            logger.debug(f'Session info: {session_info}')
            print("SESSION INFO",session_info)
            if 'ava' in session_info:
                attributes = session_info['ava']
                logger.debug(f'Received attributes: {attributes}')
                for attr, values in attributes.items():
                    logger.debug(f'Attribute {attr}: {values}')
            else:
                logger.debug('No attributes found in session info')
        return response
