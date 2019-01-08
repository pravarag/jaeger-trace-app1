import os
import sys
import time
import logging
from jaeger_client import Config


def init_tracer(service):
	jaeger_host = os.getenv('JAEGER_AGENT_HOST', 'localhost')
	logging.getLogger('').handlers = []
	logging.basicConfig(format='%(message)s', level=logging.DEBUG)

	config = Config(
		config = {
				'sampler': {
				'type': 'const',
				'param': 1,
				
			},
			'local_agent':{'reporting_host': jaeger_host},
			'logging': True,
			'reporter_batch_size': 1,
			},
			service_name=service,

		)	

	return config.initialize_tracer()