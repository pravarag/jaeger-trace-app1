from flask import Flask
import redis
from tracer import init_tracer
from rq import Worker, Queue, Connection
from tracer import init_tracer
from opentracing.ext import tags
from opentracing.propagation import Format
from flask_opentracing import FlaskTracer



app=Flask(__name__)
tracer = FlaskTracer()
conn_redis = redis.Redis(host='localhost', port=6379, db=0)

@app.route('/db')
def get_db_details:




if __name__ == "__main__":
	app.run(port=8082)