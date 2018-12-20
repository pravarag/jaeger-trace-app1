from flask import Flask
from flask import request
import redis
from tracer import init_tracer
from opentracing.ext import tags
from opentracing.propagation import Format
import json

app = Flask(__name__)
tracer = init_tracer('redis-display')
conn_redis = redis.Redis(host='localhost', port=6379, db=0)


@app.route('/display')
def display_values():
	span_ctx = tracer.extract(Format.HTTP_HEADERS, request.headers)
	span_tags = {tags.SPAN_KIND: tags.SPAN_KIND_RPC_SERVER}

	with tracer.start_active_span('redis-display-span', child_of=span_ctx, tags=span_tags):
		# details = {'Delivery-Guy':conn_redis.get('Delivery-Guy'),
		# 			'Food-Ordered':conn_redis.get('item_ordered')}
		print(type(conn_redis.get('Delivery-Guy')))
		print(type(conn_redis.get('item_ordered'))) 

		return "hello world"


if __name__ == '__main__':

	app.run(port=8083)
