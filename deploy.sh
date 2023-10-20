docker build -t movie_recommender:$1 --build-arg timestamp=$1 -f /home/cdgamaro/group-project-s23-the-incredi-codes/Dockerfile /home/cdgamaro/group-project-s23-the-incredi-codes >> /home/cdgamaro/docker_build_output
export IMAGE=movie_recommender:$1
docker stack deploy -c /home/cdgamaro/group-project-s23-the-incredi-codes/docker-compose.yml movie_recommender