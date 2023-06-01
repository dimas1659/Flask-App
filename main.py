from flask import Flask
import random
from datetime import datetime
import pytz
from flask import Flask, render_template

### Make the flask app
app = Flask(__name__)


### Routes
@app.route("/")
def hello_world():
  return "Hello, world!"  # Whatever is returned from the function is sent to the browser and displayed.


@app.route("/time")
def get_time():
  now = datetime.now().astimezone(pytz.timezone("US/Central"))
  timestring = now.strftime(
    "%Y-%m-%d %H:%M:%S")  # format the time as a easy-to-read string
  return render_template("time.html", timestring=timestring)


@app.route("/info")
def info_sabout_student():
  return "Dmytro Blahovisnyy KID-22"  # Whatever is returned from the function is sent to the browser and displayed.


@app.route("/randvalue")
def get_random():
  random_value = random.randint(1, 10)
  return render_template("random.html", number=random_value)

@app.route("/dump")
def dump_entries():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('select id, date, title, content from entries order by date')
    rows = cursor.fetchall()
    output = ""
    for r in rows:
        debug(str(dict(r)))
        output += str(dict(r))
        output += "\n"
    return "<pre>" + output + "</pre>"

@app.route("/browse")
def browse():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('select id, date, title, content from entries order by date')
    rowlist = cursor.fetchall()
    return render_template('browse.html', entries=rowlist)

@app.cli.command("initdb")
def init_db():
    """Clear existing data and create new tables."""
    conn = get_db()
    cur = conn.cursor()
    with current_app.open_resource("schema.sql") as file: # open the file
        alltext = file.read() # read all the text
        cur.execute(alltext) # execute all the SQL in the file
    conn.commit()
    print("Initialized the database.")

@app.cli.command('populate')
def populate_db():
    conn = get_db()
    cur = conn.cursor()
    with current_app.open_resource("populate.sql") as file: # open the file
        alltext = file.read() # read all the text
        cur.execute(alltext) # execute all the SQL in the file
    conn.commit()
    print("Populated DB with sample data.")


### Start flask
if __name__ == "__main__":
  app.run(host='0.0.0.0', port=8080, debug=True)
