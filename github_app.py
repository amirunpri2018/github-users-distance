from flask import Flask, render_template, request, Response
from db_cyphers import GitHubNeo4jFunctions
import os
from json import dumps

app = Flask(__name__)
uri = os.environ['URI']
user = os.environ['USER']
password = os.environ['PASSWORD']
github_neo4j_functions = GitHubNeo4jFunctions(uri, user, password)


@app.route('/')
def get_index():
    return render_template("index.html.j2")


@app.route('/graph')
def graph():
    first_user = request.args.get('first')
    second_user = request.args.get('second')
    users_distance = github_neo4j_functions.users_distance(first_user, second_user)
    result = Response(dumps(users_distance), mimetype="application/json")
    return result


@app.route('/following')
def following():
    result = github_neo4j_functions.users_with_numerous_following()
    return render_template("index.html.j2", result=result)


@app.route('/followers')
def followers():
    result = github_neo4j_functions.users_with_numerous_followers()
    return render_template("index.html.j2", result=result)


@app.route('/members')
def members():
    result = github_neo4j_functions.projects_with_numerous_members()
    return render_template("index.html.j2", result=result)


if __name__ == '__main__':
    app.run(debug=True)
