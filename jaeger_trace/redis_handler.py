from flask import Flask
from flask import request
import redis
from tracer import init_tracer
from tracer import init_tracer
from opentracing.ext import tags
from opentracing.propagation import Format
import requests



listen = ['default']

app=Flask(__name__)
tracer = init_tracer('redis-handler')
conn_redis = redis.Redis(host='localhost', port=6379, db=0)


@app.route('/db')
def redis_handler():
	span_ctx = tracer.extract(Format.HTTP_HEADERS, request.headers)
	span_tags = {tags.SPAN_KIND: tags.SPAN_KIND_RPC_SERVER}
	with tracer.start_active_span('redis-handler-span', child_of=span_ctx, tags=span_tags):
		print(request.headers)
		print(request.headers.get('Delivery-Guy'))
		food_item = request.headers.get('Order-Item')
		conn_redis.set('Order-Item', str(food_item))
		call_redis_display(8083)
		return "redis_handler completes....."


def call_redis_display(port):
	url = "http://127.0.0.1:{}/display".format(port)
	span = tracer.active_span
	span.set_tag(tags.HTTP_METHOD, 'GET')
	span.set_tag(tags.HTTP_URL, url)
	span.set_tag(tags.SPAN_KIND, tags.SPAN_KIND_RPC_SERVER)
	headers = {}
	tracer.inject(span, Format.HTTP_HEADERS, headers)
	r = requests.get(url, headers)


if __name__ == "__main__":
	app.run(port=8082)