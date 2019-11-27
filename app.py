from flask import Flask, request, render_template
import json
import math
app = Flask(__name__)
import psycopg2

@app.route('/')
def index():
  return 'Index Page'

@app.route('/hello')
def hello():
  return 'Hello, greetings from different endpoint'

#adding variables
@app.route('/user/<username>',methods=['GET','POST'])
def show_user(username):
    answer = "start"
    try:
        connection = psycopg2.connect(user="postgres",
                                      password="p@ssw0rd",
                                      host="127.0.0.1",
                                      port="5432",
                                      database="beeline")

        cursor = connection.cursor()
        answer = "pg connected"
        select_Query = \
            "SELECT   player.id,player.name,player.age,player.nationality FROM   public.player  Limit 10"
        cursor.execute(select_Query)
        columns = ('id', 'name', 'age', 'nationality')
        results = []
        for row in cursor.fetchall():
            results.append(dict(zip(columns, row)))
        answer = json.dumps(results, indent=2)

    except (Exception, psycopg2.Error) as error:
        print("Error while connecting to PostgreSQL", error)
        answer = "error"
    finally:
        # closing database connection.
        if (connection):
            cursor.close()
            connection.close()
    return answer

@app.route('/post/<post_id>',methods=['GET','POST'])
def show_post(post_id):
  if request.method == 'POST':
      data = request.get_json(force=True)
      return str(data['selling']['number'])
      #returns the post, the post_id should be an int
      #   #y = json.loads(post_id)
  #return str(post_id)
     #return str(math.factorial((int(post_id))))
  elif request.method == 'GET':
      data = request.get_json(force=True)
      return str(data['selling']['date'])
 