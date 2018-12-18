from flask import Flask
from flask import request
from tracer import init_tracer
from opentracing.ext import tags
from opentracing.propagation import Format
from flask_opentracing import FlaskTracer
import opentracing
import redis
import time




app = Flask(__name__)

# tracer = init_tracer('main-tracer')

flask_tracer = FlaskTracer(init_tracer, True, app)
parent_span = flask_tracer.get_span()
init_redis = redis.StrictRedis(host='localhost', port=6379, db=0)

@app.route("/home")
def home():

	with opentracing.tracer.start_span('home-span', child_of=parent_span) as span:
		home_span='home_span'
		span.set_tag('home_span', home_span)
		print("Tis home-tracer's home-span")
		item_name = input("Enter the food item: ")
		# set new redis key for this span
		init_redis.set('home', 'this is key for home_span')
		init_redis.set('item_ordered', item_name)
		time.sleep(5)
		assign_delivery(item_name)
		return "Your food is on the way...."
	#tracer.close()


#@app.route("/salvador")
def assign_delivery(with_item):
	print("The delivery is being assigned....")
	with opentracing.tracer.start_span('Assign-Delivery', child_of=parent_span) as span:
		delv_guy = 'salvador'
		span.set_tag('Delivery_Guy', delv_guy)
		time.sleep(5)
		init_redis.set('Delivery_Guy', delv_guy)
		# get_db_values()

		# inject order and agent details here...

		with opentracing.tracer.start_span('retrieve-order-details', child_of=span) as new_span:
			new_s = 'retrieve-order-details'
			new_span.set_tag('Order_Details', new_s)
			print("order-details gathered")
		get_db_values()
		# return "Your food is assigned to "+delv_guy


# @app.route("/db")
def get_db_values():
	# this gathers redis entries so far
	# with opentracing.tracer.start_span('retrieve-order-details', child_of=parent_span) as span:
	# 	new_s = 'retrieve-order-details'
	# 	span.set_tag('Order_Details', new_s)
	list_keys = init_redis.keys()
	print(list_keys)
	return "keys returned"


if __name__ == "__main__":
	app.run(port=8081)	
	
