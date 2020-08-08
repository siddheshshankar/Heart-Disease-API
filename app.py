import os
from flask import Flask, render_template
import pickle
from flask_wtf import FlaskForm
from wtforms import IntegerField, BooleanField, FloatField, SubmitField, RadioField
from wtforms.validators import DataRequired


class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    APP_PATH = os.path.dirname(__file__)


app = Flask(__name__)
app.config.from_object(Config)


class DataForm(FlaskForm):
    gender = RadioField('Gender', validators=[DataRequired()], choices=['Male', 'Female'])
    age = IntegerField('Age', validators=[DataRequired()])
    diabetic = BooleanField('Are you Diabetic?')
    smoker = BooleanField('Do you smoke? ')
    cig_count = FloatField('How many cigarettes do you smoke per day ?', default=0)
    weight = FloatField('Weight (Kg)', validators=[DataRequired()])
    height = FloatField('Height (cm)', validators=[DataRequired()])
    bp = IntegerField('Blood Pressure (mmHg)  Normal range : (90-120)/(60-80)', validators=[DataRequired()])
    submit = SubmitField('Submit')


@app.route('/')
@app.route('/index', methods=['GET', 'POST'])
def index():
    form = DataForm()
    if form.validate_on_submit():
        li = ['age', 'gender', 'cig_count', 'diabetic', 'height', 'weight', 'smoker', 'bp']
        data = {}
        for ele in li:
            data[ele] = eval('form.' + ele + '.data')

        gender = 1 if data['gender'] == 'Male' else 0
        smoker = 1 if data['smoker'] else 0
        diabetic = 1 if data['diabetic'] else 0
        filename = os.path.join(app.config['APP_PATH'], 'model.pkl')
        with open(filename, 'rb') as f:
            model = pickle.load(f)
            value = model.predict([[gender, data['age'], smoker, data['cig_count'],
                                    diabetic, data['bp'], bmi(data['weight'], data['height'])]])
            data = ['done', value[0]]
        return render_template('index.html', value=data, form=form, data=data)
    return render_template('/index.html', form=form)


def bmi(weight, height):
    return round(float(weight) / (float(height / 100) * float(height / 100)), 2)


if __name__ == '__main__':
    app.run(debug=True)
