from datetime import datetime
from flask import Flask, Response,render_template, request, redirect,url_for
import pandas as pd
from logging import DEBUG
import matplotlib
matplotlib.use('agg')
import matplotlib.pyplot as plt
import io
import base64
import seaborn as sns
import json
from wtforms import TextField, Form
from flask import jsonify

app = Flask(__name__)

result_pca = pd.read_csv('result_pca.csv')
movie_names=result_pca['title'].unique().tolist()

class SearchForm(Form):
    autocomp = TextField('Insert City', id='city_autocomplete')

@app.route('/')
@app.route('/index')
def index():
	return render_template('index.html')

@app.route('/rating',methods=['GET','POST'])
def rating():
	form = SearchForm(request.form)
	m=[0,0,0,0,0,0]
	num=[0,0,0,0,0,0]
	total_m=-1
	total_n=-1
	img = io.BytesIO()
	plt.savefig(img,format='png')
	img.seek(0)
	plot_url = base64.b64encode(img.getvalue()).decode()
	if request.method == "POST":
		name = request.form['text']
		print(name)
		sub=result_pca[result_pca['title']==name]
		num=sub['Number'].values
		m=[round(i,2) for i in sub['mean'].values]
		total_m=round(sum(num*m)/sum(num),2)
		total_n=sum(num)

		img = io.BytesIO()
		result_pca_plot(result_pca,name)
		plt.savefig(img,format='png')
		img.seek(0)

		plot_url = base64.b64encode(img.getvalue()).decode()
		
		return render_template('rating.html',form=form,title=name,plot_url=plot_url,num=num,m=m,total_m=total_m,total_n=total_n)
	return render_template('rating.html',form=form,plot_url=plot_url,num=num,m=m,total_m=total_m,total_n=total_n)
#	return render_template('rating.html',form = form)

@app.route('/_autocomplete', methods=['GET'])
def autocomplete():
	return Response(json.dumps(movie_names), mimetype='application/json')

def result_pca_plot(result_pca,name):
	plt.figure(figsize=(8,4))
	a = result_pca[result_pca.title==name]
	ax =sns.barplot(x="group",y="mean",data=a)
	ax.set_xticklabels(['G1','G2','G3','G4','G5','G6'],rotation=0,fontsize=10)
	plt.ylim(2.5,4.8)
	plt.title(name,fontsize=10)
	plt.xlabel("",fontsize=20)
	plt.ylabel("Rating(mean)",fontsize=10)

if __name__ == '__main__':
	app.run(debug=True)
