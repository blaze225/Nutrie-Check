from app import app
from flask import render_template, request, jsonify
from PIL import Image
import os
import requests
from ocr import *
from models import *

UPLOAD_FOLDER = '/Users/saad/Desktop/Sem4/code.fun.do/uploads/'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/')
def index():
	user = {'username': 'Saad'}
	return render_template('index.html', title='Home', user=user)

@app.route('/scan_barcode', methods=['GET','POST'])
def scan_barcode():
	""" USECASE1: BAR CODE SCAN """
	if request.method == 'POST':
		bcode = request.form['bcode']
		print("GOT BARCODE!!", bcode)
		# check if product is in db
		result = select_ingredients(bcode)
		print(result)
		return jsonify(result)
		# return render_template('ingredients.html',words=words)
	else:
		return "Y U NO USE POST?"

@app.route('/get_ingredients', methods=['GET','POST'])
def get_ingredients():
	"""USECASE2: GET INGREDIENTS FROM PRODUCTS"""
	if request.method == 'POST':
		# Save file
		bcode = request.form['bcode']
		file = request.files['file']
		ptype = request.form['type']
		filename = file.filename
		file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
		print("FILE SAVED!",filename)
		# Get ocr result
		words, bounding_boxes = ocr('uploads/'+filename)
		print("OCR DONE!")
		result=[]
		for w in words:
			w=w.replace('\'',' ')
			print(w)
			if w:
				temp='_'.join(w.strip().split())
				print(temp)
				if temp:
					rs = select_safety_rating(ptype,temp)
					#print(rs)
					if rs:
						result.append(rs)
		print(result)
		return jsonify(result)
		# return jsonify(bounding_boxes)
		# return render_template('ingredients.html',words=words)
	else:
		return "Y U NO USE POST?"

