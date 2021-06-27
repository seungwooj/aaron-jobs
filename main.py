from flask import Flask, render_template, request, redirect, send_file
from scrapper import return_jobs
from exporter import save_to_file

app = Flask("Scrapper")

fake_db = {}


@app.route("/")
def home():
    # create search form
    return render_template("home.html")


@app.route("/report")
def report():
    # Rendering
    word = request.args.get('word') #/reports?args1=a&args2=b&args3=...
    if word:
        word = word.lower()
        existing_jobs = fake_db.get(word)
        # if db already has the result : return the result on db
        # if db has no result : run scrapper
        if existing_jobs:
            jobs = existing_jobs
        else:
            jobs = return_jobs(word)
            fake_db[word] = jobs
    else:
        return redirect("/")
    return render_template(
        "report.html", 
        searchingBy=word, 
        resultsNumber=len(jobs),
        jobs=jobs
        )

@app.route("/export")
def export():
  try:
    word = request.args.get('word')
    # requires keyword to search
    if not word:
      raise Exception()
    word = word.lower()
    jobs= fake_db.get(word)
    # when no data on db : redirect
    if not jobs:
      raise Exception
    save_to_file(jobs)
    return send_file("jobs.csv")
     
  except:
    return redirect("/")

    
app.run(host="127.0.0.1", port=8080)
