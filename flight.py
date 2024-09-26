from flask import Flask,render_template, request, redirect, url_for

app=Flask(__name__)

@app.route("/")
def welcome():
    return "Hello World"
@app.route('/main',methods=['POST','GET'])
def homepage():
    if(request.method=="GET"):
        return render_template("main.html")
    else:
        dest=request.form.get("dest")
        msg="Submitted!"
        return render_template('main.html', message=msg)
if __name__=="__main__":
    app.run(debug=True)
