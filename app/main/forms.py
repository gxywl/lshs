from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField, SelectField
from wtforms.validators import DataRequired, InputRequired
from ..models import Xiangmu

class NameForm(FlaskForm):
    #xiangmu = StringField("布放项目", validators=[DataRequired()])
    #xiangmu = SelectField('布放项目', validators=[DataRequired()] , choices=[('0', '放生'),('1', '火施'),('2', '其他')])
    xiangmu = SelectField('布施项目', validators=[DataRequired()] , coerce=int)
    jine = IntegerField("金额", validators=[DataRequired()])
    submit = SubmitField('捐出')

    #在构造化Form实例时指定selectField的choices内容,
    def __init__(self, *args, **kwargs):
        super(NameForm, self).__init__( *args,**kwargs)
        self.xiangmu.choices = [(xiangmu.id, xiangmu.xiangmu) for xiangmu in Xiangmu.query.order_by(Xiangmu.id).all()]

#class EditProfileForm(FlaskForm):

