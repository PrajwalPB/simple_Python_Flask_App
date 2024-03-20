from flask import Flask,render_template
from prometheus_client import Counter, Gauge, generate_latest, REGISTRY
from prometheus_client import Histogram
from flask import Response
from prometheus_client import Info
import time

app = Flask(__name__)

# Define Prometheus metrics
request_counter = Counter('http_requests_total', 'Total number of HTTP requests')
active_users = Gauge('active_users', 'Number of active users')
request_duration = Histogram('http_request_duration_seconds', 'HTTP request duration', buckets=[0.1, 0.5, 1, 2, 5])
db_query_duration = Histogram('db_query_duration_seconds', 'Duration of database queries', buckets=[0.1, 0.5, 1, 2, 5])


def perform_database_query(user_input):
    # Simulate a database query
    time.sleep(1)  # Simulating a time-consuming database operation

@app.route('/database_query/<user_input>')
def database_query(user_input):
    with db_query_duration.time():
        perform_database_query(user_input)
    return 'Query completed'


@app.route('/')
def index():
    
    return render_template('index.html')

@app.route('/helloworld')
def hello():
    # Increment the request counter
    request_counter.inc()

    # Simulate some metric changes
    active_users.set(42)

    return 'Hello, World!'

@app.route('/metrics')
def metrics():
    # Expose Prometheus metrics on the /metrics endpoint
    return Response(generate_latest(REGISTRY), content_type='text/plain')


@app.route('/some_operation')
def some_operation():
    with request_duration.time():
        # Code for the operation
        return 'Operation completed'






if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)