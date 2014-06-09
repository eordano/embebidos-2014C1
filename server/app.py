from datetime import datetime
import json
import os
import sys

from flask import Flask, request
from flask.ext.sqlalchemy import SQLAlchemy

import config

app = Flask(__name__)
app.config.from_object('config')

db = SQLAlchemy(app)

class Module(db.Model):

    __tablename__ = 'module'
    id = db.Column(db.Integer, primary_key=True)
    i2c_id = db.Column(db.Integer, unique=True)
    type = db.Column(db.String(50), unique=True)
    name = db.Column(db.String(50), unique=True)
    value = db.Column(db.Integer)
    last_update = db.Column(db.DateTime)

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}
    def __repr__(self):
        return '<Module %r>' % (self.name)

class Rule(db.Model):

    __tablename__ = 'rule'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True)
    time_from = db.Column(db.String(10))
    time_to = db.Column(db.String(10))
    sensor_module = db.Column(db.Integer)
    output_module = db.Column(db.Integer)
    less_than = db.Column(db.Boolean)
    value_threshold = db.Column(db.Integer)
    switch_to_value = db.Column(db.Integer)
    priority = db.Column(db.Integer)

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}
    def __repr__(self):
        return '<Rule %r>' % (self.name)


@app.route('/modules', methods=['GET'])
def modules():
    return json.dumps(Module.query.all())

@app.route('/module', methods=['POST'])
def add_module():
    values = { key: request.values[key] for key in request.values}
    try:
        values['last_update'] = datetime.fromtimestamp(float(values['last_update']))
    except:
        values['last_update'] = None
    mod = Module(**values)
    db.session.add(mod)
    db.session.commit()
    return ''

@app.route('/rules', methods=['GET'])
def rules():
    return json.dumps(Rule.query.all())

@app.route('/rule', methods=['POST'])
def add_rule():
    rule = Rule(**request.values)
    db.session.add(rule)
    db.session.commit()
    return json.dumps(rule.as_dict())

@app.route('/rule/<int:rule_id>', methods=['DELETE'])
def delete_rule(rule_id):
    db.session.delete(Rule.query.filter_by(id=rule_id))
    db.session.commit()
    return ''

@app.route('/module/<int:module_id>', methods=['PUT'])
def send_data(module_id):
    os.system('python module_send %d %d'%(module_id, request.values['value']))
    return ''
