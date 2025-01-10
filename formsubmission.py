#https://www.youtube.com/watch?v=fPAUGZYU4MA&list=PLf9umJdQ546h26s7VKQVUir5GoOZ-1JTP&index=10

from flask_wtf import form

from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import ValidationError, DataRequired

class BrawlStarsMapTrackerRegistrationForm(form.Form):
    name=StringField(label="Username:",validators=[DataRequired()])
    passWord=PasswordField(label="Password:",validators=[DataRequired()])
    submit=SubmitField("Confirm")