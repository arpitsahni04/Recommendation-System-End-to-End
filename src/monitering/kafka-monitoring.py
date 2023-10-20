from kafka import KafkaConsumer
from prometheus_client import Counter, Histogram, start_http_server, Gauge

topic = 'movielog2'

start_http_server(8765)

# Counter, Gauge, Histogram, Summaries
REQUEST_COUNT = Counter(
    'request_count', 'Recommendation Request Count',
    ['http_status']
)

REQUEST_LATENCY = Histogram('request_latency_seconds', 'Request latency')

RATING_GAUGE = Gauge('rating_average', 'Exponentially Weighted Average of Last 2000 Ratings')

STATUS_RATIO = Gauge('status_ratio', 'Ratio of non-200 status codes to 200 status codes over the past 10000 requests')

ratings = []
ewma = 0
alpha = 0.01
count = 0

statuses = {'200': 0}
other_statuses = 0
request_count = 0

def update_ewma(rating):
    global ewma, count
    if count < 2000:
        ratings.append(rating)
        ewma = sum(ratings) / len(ratings)
        count += 1
    else:
        ewma = alpha * rating + (1 - alpha) * ewma
        removed = ratings.pop(0)
        ewma = ewma - alpha * removed + alpha * ewma
        ratings.append(rating)

def main():
    global other_statuses, request_count
    consumer = KafkaConsumer(
        topic,
        bootstrap_servers='localhost:9092',
        auto_offset_reset='earliest',
        group_id=topic,
        enable_auto_commit=True,
        auto_commit_interval_ms=1000
    )

    for message in consumer:
        event = message.value.decode('utf-8')
        values = event.split(',')

        if 'GET /rate/' in values[2]:
            rating_value = values[2].split('=')[1]
            if rating_value.isnumeric():
            # convert the rating value to an integer
                rating = int(rating_value)

                update_ewma(rating)
                RATING_GAUGE.set(ewma)

        elif 'recommendation request' in values[2]:
            status = values[3].strip().split(" ")[1]
            REQUEST_COUNT.labels(status).inc()

            time_taken = float(values[-1].strip().split(" ")[0])
            REQUEST_LATENCY.observe(time_taken / 1000)

            if status == '200':
                statuses['200'] += 1
            else:
                other_statuses += 1

            request_count += 1

            if request_count >= 10000:
                ratio = float(other_statuses) / statuses['200']
                STATUS_RATIO.set(ratio)

                # reset counters
                statuses['200'] = 0
                other_statuses = 0
                request_count = 0


if __name__ == "__main__":
    main()