from flask import Flask, render_template, request, flash, redirect, url_for, session
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Regexp
from flask_bootstrap import Bootstrap

app = Flask(__name__)
app.config['SECRET_KEY'] = 'mysecretkey'
Bootstrap(app)

# Форма для введення номеру квитка
class TicketForm(FlaskForm):
    ticket_number = StringField('Введіть номер квитка (6 цифр):',
                                validators=[DataRequired(), Regexp(r'^[0-9]{6}$', message='Повинно бути 6 цифр')])
    submit = SubmitField('Перевірити')

# Головна сторінка з формою
@app.route('/', methods=['GET', 'POST'])
def index():
    form = TicketForm()
    if form.validate_on_submit():
        ticket_number = form.ticket_number.data
        # Збереження даних для передачі на сторінку результату
        session['ticket_number'] = ticket_number
        return redirect(url_for('result'))
    elif request.method == 'POST' and not form.validate():
        flash('Помилка: введіть коректний номер квитка (6 цифр).', 'danger')
    return render_template('index.html', form=form)

# Сторінка результату
@app.route('/result')
def result():
    ticket_number = session.get('ticket_number', None)
    if ticket_number:
        # Перевірка на щасливий квиток
        first_half = sum(int(digit) for digit in ticket_number[:3])
        second_half = sum(int(digit) for digit in ticket_number[3:])
        if first_half == second_half:
            flash('Вітаємо! Це щасливий квиток!', 'success')
            result_image = 'yes.png'
        else:
            flash('На жаль, це не щасливий квиток.', 'danger')
            result_image = 'no.png'
        return render_template('result.html', result_image=result_image)
    else:
        return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
