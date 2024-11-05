#https://www.youtube.com/watch?v=fPAUGZYU4MA&list=PLf9umJdQ546h26s7VKQVUir5GoOZ-1JTP&index=10

from flask_wtf import Form

from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired

class BrawlStarsMapTrackerRegistrationForm(Form):
    name=StringField(label="Username",validators=[DataRequired()])
    passWord=PasswordField(label="Password",validators=[DataRequired()])
    submit=SubmitField("Confirm")