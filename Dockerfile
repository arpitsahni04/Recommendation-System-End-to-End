FROM python:3.8 as release
COPY ./requirements.txt /app/requirements.txt
WORKDIR /app
RUN pip3 install -r requirements.txt
COPY src/ /app/
COPY data/movie_list.csv /app/data/
EXPOSE 8082
ENV FLASK_RUN_PORT=8082
ENV FLASK_APP=main
ARG timestamp
ENV timestamp=$timestamp
CMD ["python3", "-m", "flask", "run", "--host", "0.0.0.0"]
