from wtforms import *
from flask_wtf import *
from wtforms.validators import *
from our_requests import *


class AutorisationForm(FlaskForm):
    email = EmailField("Введите Вашу почту", validators=[DataRequired()])
    password = PasswordField("Введите Ваш пароль", validators=[DataRequired()])
    submit = SubmitField("Войти")


class RegistrationForm(FlaskForm):
    conn = get_db_connection()
    cur = conn.cursor()
    email = EmailField("Почта", validators=[DataRequired()])
    password = PasswordField("Пароль", validators=[DataRequired()])
    password_again = PasswordField(
        "Повторите пароль",
        validators=[
            DataRequired(),
            EqualTo("password", message="Пароли должны совпадать."),
        ],
    )
    name = StringField("Имя пользователя", validators=[DataRequired()])
    surname = StringField("Фамилия пользователя", validators=[DataRequired()])
    role = SelectField("Введите Вашу роль", choices=get_roles(cur))
    submit = SubmitField("Зарегистрироваться")


class InventoryaddForm(FlaskForm):
    name = StringField("Название", validators=[DataRequired()])
    quantity = IntegerField(
        "Количество",
        validators=[
            DataRequired(),
            NumberRange(min=1, message="Количество должно быть неотрицательным"),
        ],
    )
    submit = SubmitField("Добавить")


class EditInventoryForm(FlaskForm):
    conn = get_db_connection()
    cur = conn.cursor()
    data = get_conditions(cur)
    name = StringField("Название", validators=[DataRequired()])
    quantity = IntegerField("Количество", validators=[DataRequired()])
    status = SelectField(
        "Состояние", choices=data, coerce=int, default=data[0]
    )
    save = SubmitField("Сохранить", render_kw={"class": "btn btn-warning"})
    delete = SubmitField("Удалить", render_kw={"class": "btn btn-danger"})
    back = SubmitField("Назад", render_kw={"class": "btn btn-secondary"})


class ReportForm(FlaskForm):
    sender_name = StringField('Имя отправляющего', validators=[
        DataRequired(message="Поле обязательно для заполнения."),
        Length(max=100, message="Имя должно быть не длиннее 100 символов.")
    ])
    report_date = DateField('Дата отчета', validators=[
        DataRequired(message="Укажите дату.")
    ])
    report_content = TextAreaField('Содержание отчета', validators=[
        DataRequired(message="Введите текст отчета."),
        Length(max=1000, message="Отчет не должен превышать 1000 символов.")
    ])
    submit = SubmitField('Создать отчет')


class PurchasePlanForm(FlaskForm):
    item_name = StringField('Название инвентаря', validators=[
        DataRequired(message="Поле обязательно для заполнения."),
        Length(max=200, message="Название не должно превышать 200 символов.")
    ])
    supplier = StringField('Название поставщика', validators=[
        DataRequired(message="Укажите поставщика."),
        Length(max=150, message="Название поставщика не должно превышать 150 символов.")
    ])
    price = DecimalField('Планируемая цена за всю закупку', places=2, validators=[
        DataRequired(message="Введите цену."),
        NumberRange(min=1, message="Цена не может быть меньше 1.")
    ])
    quantity = IntegerField('Количество предметов', validators=[
        DataRequired(message="Введите количество."),
        NumberRange(min=1, message="Количество должно быть не меньше 1.")
    ])
    submit = SubmitField('Добавить в план закупок')