# uses debian stertch-slim
# https://github.com/nginxinc/docker-nginx/blob/master/stable/stretch/Dockerfile
FROM nginx:stable

# Remove default configuration from Nginx
RUN rm /etc/nginx/conf.d/default.conf

ARG config=nginx.conf

# Overwrite the NGINX conf
COPY $config /etc/nginx/conf.d/