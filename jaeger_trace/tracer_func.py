import sys
import time
import logging
import requests
from jaeger_client import Config
from tracer import init_tracer
from opentracing.ext import tags
from opentracing.propagation import  Format


def say_hello(hello_to):
	with tracer.start_active_span('hello-again') as scope:
		scope.span.set_tag('hello-to-this-guy', hello_to)
		scope.span.log_kv({'event': 'string-format', 'value': hello_to})
		print(hello_to)

def hello_from_home(hello_obj):
	with tracer.start_active_span('hello-from-home') as scope:
		hello_str = http_get(8081, 'home', 'helloObj', hello_obj)
		scope.span.log_kv({'event': 'string-format', 'value': hello_str})
		return hello_obj
		# scope.span.set_tag('another-hello-to', hello_obj)
		# scope.span.log_kv({'event': 'string-format', 'value': hello_obj})
		# print(hello_obj)


def http_get(port, path, param, value):
	url = "http://localhost:{}/{}".format(port, path)

	span = tracer.active_span
	span.set_tag(tags.HTTP_METHOD, 'GET')
	print("1 tag ",tags.HTTP_METHOD)
	span.set_tag(tags.HTTP_URL, url)
	print("2 tag ", tags.HTTP_URL)
	span.set_tag(tags.SPAN_KIND, tags.SPAN_KIND_RPC_CLIENT)
	print("3 tag ", type(tags.SPAN_KIND))
	print("tags:", tags)
	headers = {}
	print(headers)
	tracer.inject(span, Format.HTTP_HEADERS, headers)
	print("tracer injected")

	r = requests.get(url, params={param: value}, headers=headers)
	assert r.status_code == 200
	return r.text


tracer = init_tracer('hello-world-again')

hello_to='Bryan'
say_hello(hello_to)

hello_from_home('John')


time.sleep(2)
tracer.close()