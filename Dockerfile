FROM python:3.7
WORKDIR /usr/src/app
COPY . .
EXPOSE 8080
CMD ["python", "./geocoding_proxy.py"]