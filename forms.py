from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired, FileAllowed, FileSize

from wtforms.fields import StringField, IntegerField, SubmitField, PasswordField, SelectField
from wtforms.validators import DataRequired, Length, equal_to

class AddTourForm (FlaskForm):
    city = StringField("ქალაქის სახელი", validators=[DataRequired(message="ქალაქის ველი სავალდებულოა")])
    country = StringField ("ქვეყნის სახელი", validators=[DataRequired(message="ქვეყნის ველი სავალდებულოა")])
    price = IntegerField ("ტურის ფასი", validators=[DataRequired(message="ფასის ველი სავალდებულოა")])
    img = FileField ("სურათი", validators=[FileRequired(message="სურათის ველი სავალდებულოა"),
                                            FileSize(max_size=1024*1024*25),
                                            FileAllowed(["jpg", "png", "jpeg"], message="დაშვებულია: jpg, png და jpeg ტიპის ფაილები")])
    

    submit = SubmitField ("დამატება")


class EditTourForm (FlaskForm):
    city = StringField("ქალაქის სახელი", validators=[DataRequired(message="ქალაქის ველი სავალდებულოა")])
    country = StringField ("ქვეყნის სახელი", validators=[DataRequired(message="ქვეყნის ველი სავალდებულოა")])
    price = IntegerField ("ტურის ფასი", validators=[DataRequired(message="ფასის ველი სავალდებულოა")])
    img = FileField ("სურათი", validators=[FileSize(max_size=1024*1024*25),
                                            FileAllowed(["jpg", "png", "jpeg"], message="დაშვებულია: jpg, png და jpeg ტიპის ფაილები")])
                                            
    submit = SubmitField ("დამატება")
    



class RegForm(FlaskForm):
    username = StringField("მომხმარებლის სახელი", validators=[DataRequired(message="მომხმარებლის სახელი სავალდებულოა")]) 
    password = PasswordField("პაროლი", validators=[Length(min=8, max=60),DataRequired(message="პაროლი სავალდებულოა") ])
    repeat_password = PasswordField("გაიმეორეთ პაროლი", validators=[equal_to("password", message="პაროლები არ ემთხვევა"), DataRequired(message="პაროლის გამეორება სავალდებულოა")])
    country = SelectField("მონიშნეთ ქვეყანა" ,choices=["საქართველო", "გერმანია", "საბერძნეთი", "იტალია", "ესპანეთი", "ჩეხეთი"], validators=[DataRequired(message="ქვეყნის მონიშვნა სავალდებულოა")])

    submit = SubmitField("რეგისტრაცია")
    

class LoginForm(FlaskForm):
    username = StringField("მომხმარებლის სახელი", validators=[DataRequired(message="მომხმარებლის სახელი სავალდებულოა")]) 
    password = PasswordField("პაროლი", validators=[DataRequired(message="პაროლი სავალდებულოა")])

    submit = SubmitField("შესვლა")