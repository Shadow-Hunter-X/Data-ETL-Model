from flask import Flask, make_response, request

app = Flask(__name__)

@app.route("/set_cookies")
def set_cookie():
    resp = make_response("success")
    resp.set_cookie("test", "test",max_age=3600)
    return resp

@app.route("/get_cookies")
def get_cookie():
    cookie_1 = request.cookies.get("test")  
    return cookie_1

@app.route("/delete_cookies")
def delete_cookie():
    resp = make_response("del success")
    resp.delete_cookie("test")
    return resp

if __name__ == '__main__':
    app.run(debug=True)