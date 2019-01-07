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
import sys
import os



app = Flask(__name__)
tracer = init_tracer('main-tracer')
redis_host = os.getenv('REDIS_HOST', 'localhost')
redis_port = os.getenv('REDIS_PORT', '6379')
#init_redis = redis.StrictRedis(host=redis_host, port=6379, db=0)
init_redis = redis.StrictRedis(host=redis_host, port=int(redis_port), db=0)

app2_host = os.getenv('APP2_HOSTNAME', 'localhost')
app3_host = os.getenv('APP3_HOSTNAME', 'localhost')
# TODO: make app2_port configurable

# first call to home endpoint
@app.route("/home")
def home():
	with tracer.start_active_span('home-span') as scope:
		home_span='home_span'
		scope.span.set_tag('home_span', home_span)
		try:
			item_name = request.args.get('item')
		except requests.exceptions.RequestException as e:
			return("Couldn't connect to the mentioned service")
			#sys.exit(1)
		print('Item entered: ', item_name)
		# set the redis keys
		init_redis.set('home', 'home_span')
		init_redis.set('item_ordered', item_name)
		time.sleep(5)
		resp = assign_delivery(item_name)
		return f"Your food is on the way....\n{resp}\n"


def assign_delivery(with_item):
	print("The delivery is being assigned....")
	with tracer.start_active_span('Assign-Delivery') as scope:
		delv_guy = 'salvador'
		scope.span.set_tag('Delivery_Guy', delv_guy)
		init_redis.set('Delivery_Guy', delv_guy)
		url = 'http://' + app2_host + '/db'
		resp = db_handler(8082, url, delivery_guy=delv_guy, order_item=with_item)
		# retrv_order_id = init_redis.get('Order-Id')
		# print(retrv_order_id)
		print("delivery assigned")
		return resp.text


@app.route('/getdetails')
def call_redis_display():
	with tracer.start_active_span('display-order-details') as scope:
		order_ = 'display-order-details'
		scope.span.set_tag('display-order-details', order_)
		try:
			ord_id = request.args.get('order_id')
		except requests.exceptions.RequestException as e:
			return("Couldn't connect to the mentioned service")

		print("Order id for details display: ", ord_id)
		url = 'http://'+app3_host+'/display'
		resp = db_handler(8083, url, order_id=ord_id)
	# import pdb; pdb.set_trace()
	return resp.text


def db_handler(port, url, **details):
	# ip = str(os.getenv('IP'))
	# url = 'http://'+ip+':{}/db'.format(port)
	# TODO: DEPRECATE port argument
	span = tracer.active_span
	span.set_tag(tags.HTTP_METHOD, 'GET')
	span.set_tag(tags.HTTP_URL, url)
	span.set_tag(tags.SPAN_KIND, tags.SPAN_KIND_RPC_CLIENT)
	headers=details
	tracer.inject(span, Format.HTTP_HEADERS, headers)
	r = requests.get(url, headers=headers)
	return r


if __name__ == "__main__":
    #app.debug = True
    app.run(port=8081)
