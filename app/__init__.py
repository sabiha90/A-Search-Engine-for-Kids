from flask import Flask, render_template, send_from_directory, request
import os
from jinja2 import Environment, PackageLoader, select_autoescape
env = Environment(
    loader=PackageLoader('app', 'templates'),
    autoescape=select_autoescape(['html', 'xml'])
)


from app.index.elastic_search_helper import init_index, load_documents, query_index, load_blacklist

app = Flask(__name__)


@app.route('/')
@app.route('/index')
@app.route('/index/')
def render_static():
    return render_template('index.html', index=True)


@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, '../static'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')


@app.route('/search', methods=['GET'])
def perform_search():
    load_blacklist()
    query = request.args.get('query')
    results = query_index(query)
    print(str(len(results)) + " results found.")
    print(str(results))
    return render_template('index.html', result_data=results)


@app.route('/create_document', methods=['GET'])
def create_documents():
    init_index()
    load_documents()
    return render_template('index.html')


if __name__ == '__main__':
    app.run()