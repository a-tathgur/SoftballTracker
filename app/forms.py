from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SelectField, SubmitField
from wtforms.fields.datetime import DateField
from wtforms.validators import DataRequired, NumberRange

class PlayerForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    submit = SubmitField('Add Player')

class GameForm(FlaskForm):
    date = DateField('Date', format='%Y-%m-%d', validators=[DataRequired()])
    opponent = StringField('Opponent', validators=[DataRequired()])
    score_own = IntegerField('Score (Own)', validators=[NumberRange(min=0)], default=0)
    score_opponent = IntegerField('Score (Opponent)', validators=[NumberRange(min=0)], default=0)
    submit = SubmitField('Add Game')

class PlayerStatsForm(FlaskForm):
    player = SelectField('Player', choices=[], coerce=int)
    singles = IntegerField('Singles', default=0)
    doubles = IntegerField('Doubles', default=0)
    triples = IntegerField('Triples', default=0)
    home_runs = IntegerField('Home Runs', default=0)
    walks = IntegerField('Walks', default=0)
    outs = IntegerField('Outs', default=0)
    position = SelectField('Position', choices=[
        ('P', 'Pitcher'),
        ('C', 'Catcher'),
        ('1B', 'First Base'),
        ('2B', 'Second Base'),
        ('3B', 'Third Base'),
        ('SS', 'Shortstop'),
        ('LF', 'Left Field'),
        ('LCF', 'Left Center Field'),
        ('RCF', 'Right Center Field'),
        ('RF', 'Right Field')
    ], validators=[DataRequired()])
    submit = SubmitField('Add Stats')
