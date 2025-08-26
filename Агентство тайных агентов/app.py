from flask import Flask, render_template, redirect, url_for, request
from flask_sqlalchemy import SQLAlchemy
from random import choice

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'

db = SQLAlchemy(app)


class Agent(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    code_name = db.Column(db.String(50), nullable=False)
    contact_phone = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(50), nullable=False)
    access_level = db.Column(db.String(20), nullable=False)

    def __repr__(self):
        return f"<Agent {self.code_name}>"


with app.app_context():
    db.create_all()


@app.route('/')
def get_agent_list():
    agent_list = Agent.query.all()
    return render_template('agent_list.html', agent_list=agent_list)


@app.route('/add', methods=['GET', 'POST'])
def add_agent():
    if request.method == 'POST':
        new_agent_data = form_data = request.form.to_dict()
        new_agent = Agent(**form_data)
        db.session.add(new_agent)
        db.session.commit()
        return redirect(url_for('get_agent_list'))
    return render_template('add_agent.html')

@app.route('/random_name')
def random_name():
    agent_names = [
        "Phantom Wolf",
        "Silent Hawk",
        "Midnight Lynx",
        "Ghost Panther",
        "Midnight Raven"
    ]
    random_name = choice(agent_names)
    return render_template('add_agent.html', random_name=random_name)


@app.route('/agent/<int:id>')
def get_agent_data(id):
    agent_data = Agent.query.get(id)
    if agent_data is None:
        return redirect(url_for('get_agent_list'))
    agent_dict = {
        'Кодовое имя': agent_data.code_name,
        'Телефон для связи': agent_data.contact_phone,
        'Почта': agent_data.email,
        'Уровень доступа': agent_data.access_level
    }
    return render_template('agent_data.html', agent_data=agent_dict, agent_id=id)


@app.route('/agent_redirect')
def agent_redirect():
    agent_name = request.args.get('code_name')
    agent_data = Agent.query.filter_by(code_name=agent_name).first()
    if agent_data:
        return redirect(url_for('get_agent_data', id=agent_data.id))
    return redirect(url_for('get_agent_list'))


@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_agent_data(id):
    agent_data = Agent.query.get(id)
    if agent_data is None:
        return redirect(url_for('get_agent_list'))
    if request.method == 'POST':
        agent_data.code_name = request.form["code_name"]
        agent_data.contact_phone = request.form["contact_phone"]
        agent_data.email = request.form["email"]
        agent_data.access_level = request.form["access_level"]
        db.session.commit()
        return redirect(url_for('get_agent_list'))
    return render_template('edit_agent.html',
                           agent_id=id,
                           code_name=agent_data.code_name,
                           contact_phone=agent_data.contact_phone,
                           email=agent_data.email,
                           access_level=agent_data.access_level)


@app.route('/edit_redirect')
def edit_agent_redirect():
    agent_id = request.args.get('id')
    if Agent.query.get(agent_id):
        return redirect(url_for('edit_agent_data', id=agent_id))
    return redirect(url_for('get_agent_list'))


@app.route('/delete/<id>', methods=['GET', 'POST'])
def delete_agent(id):
    agent_data = Agent.query.get(id)
    if agent_data is None:
        return redirect(url_for('get_agent_list'))
    if request.method == 'POST':
        db.session.delete(agent_data)
        db.session.commit()
        return redirect(url_for('get_agent_list'))
    agent_dict = {
        'Кодовое имя': agent_data.code_name,
        'Телефон для связи': agent_data.contact_phone,
        'Почта': agent_data.email,
        'Уровень доступа': agent_data.access_level
    }
    return render_template('delete_agent.html',agent_data=agent_dict, agent_id=id)


@app.route('/delete_redirect')
def delete_agent_redirect():
    agent_id = request.args.get('id')
    if Agent.query.get(agent_id):
        return redirect(url_for('delete_agent', id=agent_id))
    return redirect(url_for('get_agent_list'))

@app.route('/delete', methods=['GET', 'POST'])
def delete_all():
    if request.method == 'POST':
        Agent.query.delete()
        db.session.commit()
        return redirect(url_for('get_agent_list'))
    return render_template('delete_all.html')


if __name__ == '__main__':
    app.run(debug=True)
