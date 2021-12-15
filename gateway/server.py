from flask import Flask, request, Response
import requests
import jwt

app = Flask("SELAB")


@app.route('/', defaults={'path': ''})
@app.route('/<path:path>', methods=['GET', 'POST'])
def _proxy(path):
    if 'Authorization' in request.headers:
        try:
            jwt.decode(request.headers['Authorization'], 'SELAB', algorithms=["HS256"])
        except:
            return Response("{'error':'authentication failed'}", status=401, mimetype='application/json')

    if "login" in path or "signup" in path:
        service_port = "8000"
    else:
        service_port = "9000"

    resp = requests.request(
      method=request.method,
      url=request.url.replace(request.host_url, f'http://127.0.0.1:{service_port}/'),
      headers={key: value for (key, value) in request.headers if key != 'Host'},
      data=request.get_data(),
      cookies=request.cookies,
      allow_redirects=False)

    excluded_headers = ['content-encoding', 'content-length', 'transfer-encoding', 'connection']
    headers = [(name, value) for (name, value) in resp.raw.headers.items()
               if name.lower() not in excluded_headers]

    response = Response(resp.content, resp.status_code, headers)
    return response


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
