import sys
import time
import logging
from jaeger_client import Config


def init_tracer(service):
	logging.getLogger('').handlers = []
	logging.basicConfig(format='%(message)s', level=logging.DEBUG)

	config = Config(
		config = {
				'sampler': {
				'type': 'const',
				'param': 1,
			},
			'logging': True,
			'reporter_batch_size': 1,
			},
			service_name=service,

		)

	return config.initialize_tracer()


# def call_infinity(input_ob):
# 	with tracer.start_span('infinite-trace-span') as span:
# 		hello_str = 'Hello for infinite-trace {}!'.format(input_ob)

# 		for i in range(0, 1000):
# 			print(hello_str)

# tracer = init_tracer('infinite-trace')
# call_infinity('new_john')
# time.sleep(10)
# tracer.close()	