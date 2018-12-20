from flask import Flask
from flask import request
import requests
from tracer import init_tracer
from opentracing.ext import tags
from opentracing.propagation import Format
# from flask_opentracing import FlaskTracer
import opentracing
import redis
import time




app = Flask(__name__)
tracer = init_tracer('main-tracer')
init_redis = redis.StrictRedis(host='localhost', port=6379, db=0)


@app.route("/home")
def home():

	with tracer.start_active_span('home-span') as scope:
		home_span='home_span'
		scope.span.set_tag('home_span', home_span)
		print("Tis home-tracer's home-span")
		item_name = input("Enter the food item: ")
		# set new redis key for this span
		init_redis.set('home', 'this is key for home_span')
		init_redis.set('item_ordered', item_name)
		time.sleep(5)
		assign_delivery(item_name)
		return "Your food is on the way...."


def assign_delivery(with_item):
	print("The delivery is being assigned....")
	with tracer.start_active_span('Assign-Delivery') as scope:
		delv_guy = 'salvador'
		scope.span.set_tag('Delivery_Guy', delv_guy)
		init_redis.set('Delivery_Guy', delv_guy)
		db_handler(8082, delivery_guy=delv_guy, order_item=with_item)
		return "everything done..."


def db_handler(port, **details):
	url = 'http://127.0.0.1:{}/db'.format(port)
	span = tracer.active_span
	span.set_tag(tags.HTTP_METHOD, 'GET')
	span.set_tag(tags.HTTP_URL, url)
	span.set_tag(tags.SPAN_KIND, tags.SPAN_KIND_RPC_CLIENT)
	headers=details
	tracer.inject(span, Format.HTTP_HEADERS, headers)
	r = requests.get(url, headers=headers)
	# list_keys = init_redis.keys()
	# print(list_keys)
	return "request completed"


if __name__ == "__main__":
	app.run(port=8081)	
	
