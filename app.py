from ast import parse
import urllib.parse
from flask import Flask, render_template, request, url_for, flash, redirect
import requests
import json
import re 
import random
import string
from datetime import datetime as dt 
from support import to_flights, validated_flight
app = Flask(__name__)

def k(x):return requests.post("http://157.175.184.133:5001/",data=x)
def q(x):return k('"q" "{}"'.format(x))

@app.route('/' , methods=('GET', 'POST'))
def index():
    if request.method == "GET": return render_template('index.html')
    
    parameters = {
        'user_id'          : 'alogayyil_testAPI',
        'user_password'    : 'alogayyilTest@2022',
        'access'           : 'Test',
        'ip_address'       : '157.175.184.133',
        'session_id'       : q(".travel.token").json(),
        'journey_type'     : request.form["journey_type"],
        'airport_from_code': request.form["from"],
        'airport_to_code'  : request.form["to"],
        'departure_date'   : request.form["dep_date"],
        'return_date'      : request.form["ret_date"],
        'adult_flight'     : request.form["adult"],
        'child_flight'     : request.form["chaild"],
        'infant_flight'    : request.form["infants"],
        'class'            : request.form["class"],
        'target'           : 'Test'
        }
    
    r = requests.get("https://travelnext.works/api/aero-api/flight_availability_search", params=parameters)
    file_name = "".join( [random.choice(string.ascii_letters + string.digits) for i in range(22)] ) +".json"
    json.dump(r.json(), open("search_ress/"+file_name, "w"), indent = 4)

    res = {"from":request.form["from"], "to":request.form["to"], "file_name":file_name}
    return redirect(url_for(".search", res=res))

@app.route("/results", methods=('GET', 'POST'))
def search():
    if request.method == "GET":
        res = json.loads(re.sub(r"'", r'"', request.args["res"]))
        search_res = json.load(open("search_ress/" + res["file_name"]))
        return render_template('search_results.html', res=res, flights=[to_flights(f["FareItinerary"]) for f in search_res["AirSearchResponse"]["AirSearchResult"]["FareItineraries"]])

    val = k(f'revalidate["{request.form["select"]}&session_id={q(".travel.token").json()}"]').json()
    rules= k(f'farerules["{request.form["select"]}&session_id={q(".travel.token").json()}"]').json()
    
    file_name = "".join( [random.choice(string.ascii_letters + string.digits) for i in range(22)] ) +".json"
    json.dump([val, rules], open("flights_data/"+file_name, "w"), indent = 4)

    return redirect(url_for(".booking", f=file_name))

@app.route("/book", methods=('GET', 'POST'))
def booking():
    if request.method == "GET":
        f = request.args["f"]
        val, rules = json.load(open("flights_data/" + f))
        return render_template("booking.html", res=validated_flight(val))
    d = dict(request.form)
    p = {
    'user_id'                    : 'alogayyil_testAPI',
    'user_password'              : 'alogayyilTest@2022',
    'access'                     : 'Test',
    'ip_address'                 : '157.175.184.133',
    'target'                     : 'Test',
    'session_id'                 : q(".travel.token").json(),
    'area_code'                  : d["c-areacode"],
    'country_code'               : '01',
    'first_name'                 : "%3Cbr%3E".join([d[x] for x in d.keys() if x[0] == "A" and x.split("-")[1] == "first_name"]),
    'last_name'                  : "%3Cbr%3E".join([d[x] for x in d.keys() if x[0] == "A" and x.split("-")[1] == "last_name"]),
    'title'                      : "%3Cbr%3E".join([d[x] for x in d.keys() if x[0] == "A" and x.split("-")[1] == "title"]),
    'email_id'                   : urllib.parse.quote(d["c-email"]),
    'mobile_no'                  : d["c-phone_NO"],
    'dob'                        : "%3Cbr%3E".join([d[x] for x in d.keys() if x[0] == "A" and x.split("-")[1] == "dob"]),
    'gender'                     : "%3Cbr%3E".join([d[x] for x in d.keys() if x[0] == "A" and x.split("-")[1] == "gender"]),
    
    'issue_country'              : "%3Cbr%3E".join([d[x] for x in d.keys() if x[0] == "A" and x.split("-")[1] == "issue_country"]),
    'passport_expiry'            : "%3Cbr%3E".join([d[x] for x in d.keys() if x[0] == "A" and x.split("-")[1] == "passport_expiry"]),
    'passport_no'                : "%3Cbr%3E".join([d[x] for x in d.keys() if x[0] == "A" and x.split("-")[1] == "passport_no"]),
    'type'                       : 'Public',
    'IsPassportMandatory'        : 'false',
    
    'adult_flight'               : f'{len(set([x[:2] for x in d.keys() if x[0] == "A"]))}',
    'child_flight'               : f'{len(set([x[:2] for x in d.keys() if x[0] == "C"]))}',
    'infant_flight'              : f'{len(set([x[:2] for x in d.keys() if x[0] == "I"]))}',
    'frequentFlyrNum'            : '',
    'adultmealplan'              : '',
    
    'child_dob'                  : "%3Cbr%3E".join([d[x] for x in d.keys() if x[0] == "C" and x.split("-")[1] == "dob"]),
    'child_gender'               : "%3Cbr%3E".join([d[x] for x in d.keys() if x[0] == "C" and x.split("-")[1] == "gender"]),
    'child_title'                : "%3Cbr%3E".join([d[x] for x in d.keys() if x[0] == "C" and x.split("-")[1] == "title"]),
    'child_first_name'           : "%3Cbr%3E".join([d[x] for x in d.keys() if x[0] == "C" and x.split("-")[1] == "first_name"]),
    'child_last_name'            : "%3Cbr%3E".join([d[x] for x in d.keys() if x[0] == "C" and x.split("-")[1] == "last_name"]),
    'child_passport_expiry_date' : "%3Cbr%3E".join([d[x] for x in d.keys() if x[0] == "C" and x.split("-")[1] == "passport_expiry"]),
    'child_passport_no'          : "%3Cbr%3E".join([d[x] for x in d.keys() if x[0] == "C" and x.split("-")[1] == "passport_no"]),
    'child_frequentFlyrNum'      : '',
    'childMealplan'              : '',
    
    'infant_dob'                 : "%3Cbr%3E".join([d[x] for x in d.keys() if x[0] == "I" and x.split("-")[1] == "dob"]),
    'infant_gender'              : "%3Cbr%3E".join([d[x] for x in d.keys() if x[0] == "I" and x.split("-")[1] == "gender"]),
    'infant_first_name'          : "%3Cbr%3E".join([d[x] for x in d.keys() if x[0] == "I" and x.split("-")[1] == "first_name"]),
    'infant_last_name'           : "%3Cbr%3E".join([d[x] for x in d.keys() if x[0] == "I" and x.split("-")[1] == "last_name"]),
    'infant_title'               : "%3Cbr%3E".join([d[x] for x in d.keys() if x[0] == "I" and x.split("-")[1] == "title"]),
    'infantMealplan'             : '',
    
    'FareSourceCode'             : d["F-FareSourceCode"],
    'PostCode'                   : '560061'
}
    # return f'https://travelnext.works/api/aero-api/book?{urllib.parse.quote("&".join([f"{x}={p[x]}" for x in p.keys()]))}'
    # return k(f'all[https://travelnext.works/api/aero-api/book?{"&".join([f"{x}={p[x]}" for x in p.keys()])}]').text
    r = k(f'book[("{p["first_name"]}";"{p["last_name"]}";"{p["title"]}";"{p["dob"]}";"{p["gender"]}";"{p["issue_country"]}";"{p["passport_expiry"]}";"{p["passport_no"]}";"{p["IsPassportMandatory"]}";"{p["adult_flight"]}";"{p["child_flight"]}";"{p["infant_flight"]}";"{p["child_dob"]}";"{p["child_gender"]}";"{p["child_first_name"]}";"{p["child_last_name"]}";"{p["child_passport_expiry_date"]}";"{p["child_passport_no"]}";"{p["infant_dob"]}";"{p["infant_first_name"]}";"{p["infant_last_name"]}";"{p["FareSourceCode"]}&PostCode={p["PostCode"]}")]')
    return  r.json()

@app.route("/myflight", methods=('GET', 'POST'))
def details():
    return render_template("index.html")
if __name__ == "__main__":
    app.run(debug=True, port=5001)