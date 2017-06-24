from flask import Flask, render_template, request, flash
import os

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
	if request.method == 'GET':
		print "This is a Get"
		
	else: 
		print "This is a Post"
		os.system("python bots/main.py")
		print "Finished Post Message"
		
	return render_template("index.html")
		

if __name__ == "__main__":
	app.run(debug=True)
