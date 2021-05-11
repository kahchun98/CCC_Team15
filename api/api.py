import flask
from flask import request, jsonify
import couchdb



app = flask.Flask(__name__)
app.config["DEBUG"] = True


def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d

#needs refinement, working on it
@app.route('/', methods=['GET'])
def home():
    return "<h1>Prototype API</h1><p>This site is a prototype API for assignment2.</p>"

#needs refinement, working on it
@app.route('/api/v1/resources/suburbs/all', methods=['GET'])
def api_all():

    db = g.couch['suburbs']
    conn.row_factory = dict_factory
    cur = db.cursor()
    #couchdb query issue, working on it
    all_suburbs = cur.execute('SELECT * FROM suburbs;').fetchall()

    return jsonify(all_suburbs)


@app.errorhandler(404)
def page_not_found(e):
    return "<h1>404</h1><p>The resource could not be found.</p>", 404


#needs refinement, working on it
@app.route('/statistics', methods=['GET'])
def api_filter():

    #localhost:5984
    couch = couchdb.Server()
    manager = CouchDBManager()
    manager.setup(app)

    db = g.couch['suburbs']
    db['rows'] = dict()

    #couchdb query issue, working on it
    query_parameters = request.args
    id = query_parameters.get('id')
    name = query_parameters.get('suburbname')

    query = "SELECT * FROM suburbs WHERE"
    to_filter = []

    if id:
        query += ' id=? AND'
        to_filter.append(id)

    if name:
        query += ' suburbname=? AND'
        to_filter.append(name)

    if not (id or name):
        return page_not_found(404)

    query = query[:-4] + ';'

    results = cur.execute(query, to_filter).fetchall()

    return jsonify(results)



app.run()
