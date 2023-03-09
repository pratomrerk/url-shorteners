# URL Shortener
Easy to use URL shortener

## Getting started
View docker-compose.example for an example to docker-compose.yml and edit the environment variables.

## Install
docker-compose up -d

## Usage
New URL shorteners
```bash
curl --location --request GET 'http://127.0.0.1:7788/new-url?url=https://google.com&expire=315360000'
# expire is optional
```
```
Response
```json
{
    "check": "http://127.0.0.1:7788/check?url-key=TkUXJ7IZ",
    "count": 0,
    "expire": 1677575761,
    "short_url": "http://127.0.0.1:7788/TkUXJ7IZ",
    "url": "https://google.com"
}
```

Check Information url-key
```bash
curl --location --request GET 'http://127.0.0.1:7788/check?url-key=TkUXJ7IZ'
```
Response
```json
{
    "count": 2,
    "expire": 1677575761,
    "short_url": "http://127.0.0.1:7788/TkUXJ7IZ",
    "url": "https://google.com"
}
```

Use short url
```bash
http://127.0.0.1:7788/TkUXJ7IZ
```