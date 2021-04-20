from flask import Flask, render_template, request
import joblib
import numpy as np


# Load from file
# Load the Random Forest CLassifier model
filename = '.sav'
model = joblib.load(filename)

app = Flask(__name__)


def home():
	return render_template('index.html')



	