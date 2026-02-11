FROM nginx:stable-alpine

RUN rm /etc/nginx/conf.d/default.conf
COPY nginx.conf /etc/nginx/conf.d/

WORKDIR /usr/share/nginx/html
COPY . .

EXPOSE 3000
CMD ["nginx", "-g", "daemon off;"]
