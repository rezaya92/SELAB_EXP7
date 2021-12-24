from flask import Flask, request, Response, jsonify
import requests
import jwt
import base64
import json

app = Flask("SELAB")


def byte2json(byte_array):
    res = byte_array.decode('utf8').replace("'", '"')
    return json.loads(res)


@app.route('/', defaults={'path': ''})
@app.route('/<path:path>', methods=['GET', 'POST'])
def _proxy(path):
    if 'Authorization' in request.headers:
        try:
            jwt.decode(request.headers['Authorization'], 'SELAB', algorithms=["HS256"])
        except:
            return Response("{'error':'authentication failed'}", status=401, mimetype='application/json')
        jwt_payload = base64.b64decode(request.headers['Authorization'].split('.')[1])
        jwt_payload = byte2json(jwt_payload)
    
    
    if "login" in path or "signup" in path:
        service_port = "8000"
    else:
        service_port = "9000"


    data = request.get_data()
    req_json = request.get_json()

    if path == "prescriptions/view":
        data = None
        req_json = {
            "is_doctor": jwt_payload["is_doctor"],
            "is_patient": jwt_payload["is_patient"],
            "is_admin": jwt_payload["is_admin"],
            "national_id": jwt_payload["national_id"]
        }
    elif path == "prescriptions/add":
        if not jwt_payload["is_doctor"]:
            return "Access denied.", 403
        data = None
        req_json = {
            "doctor_national_id": jwt_payload["national_id"],
            "patient_national_id": byte2json(request.get_data())["patient_national_id"],
            "description": byte2json(request.get_data())["description"]
        }
    elif path == "statistics":
        if not jwt_payload["is_admin"]:
            return "Access denied.", 403
        service_port = "8000"
        resp = requests.request(
          method=request.method,
          url=request.url.replace(request.host_url, f'http://127.0.0.1:{service_port}/'),
          headers={key: value for (key, value) in request.headers if key != 'Host'},
          data=data,
          json=req_json,
          cookies=request.cookies)
        
        user_stats = byte2json(resp.content)
        #TODO
        # print(user_stats)
        # print(resp.text)
        # print(resp.json())
        # print(resp.raw)
        service_port = "9000"
        resp = requests.request(
          method=request.method,
          url=request.url.replace(request.host_url, f'http://127.0.0.1:{service_port}/'),
          headers={key: value for (key, value) in request.headers if key != 'Host'},
          data=data,
          json=req_json,
          cookies=request.cookies,
          allow_redirects=False)
        prescription_stats = byte2json(resp.content)
        user_stats.update(prescription_stats)
        return user_stats
    
    
    resp = requests.request(
      method=request.method,
      url=request.url.replace(request.host_url, f'http://127.0.0.1:{service_port}/'),
      headers={key: value for (key, value) in request.headers if key != 'Host'},
      data=data,
      json=req_json,
      cookies=request.cookies,
      allow_redirects=False)

    # print(resp.content)
    
    excluded_headers = ['content-encoding', 'content-length', 'transfer-encoding', 'connection']
    headers = [(name, value) for (name, value) in resp.raw.headers.items()
               if name.lower() not in excluded_headers]

    # print(data)
    response = Response(resp.content, resp.status_code, headers)
    return response


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
