import os
from flask import Flask, render_template, request, jsonify, flash, redirect, url_for
from main import *

app = Flask(__name__)
app.secret_key = os.urandom(24)


@app.route('/', methods=['GET'])
def index():
    return render_template("index.html")


@app.route('/submit', methods=['POST'])
def submit():
    print(request.method)
    if request.method == "POST":
        input_id = request.form['input']
        print(input_id)
        if input_id == "" or input_id[0] != "@":
            flash('Enter Valid ID 🔔', 'info')
            return redirect(url_for('index'))
        else:
            flash(f'You entered {input_id}')
            return redirect(url_for('process_data', _id=input_id))


@app.route('/process_data/<_id>')
def process_data(_id):
    print(_id)
    json_response = api(_id)
    print(json_response)
    flattened_data = flatten(json_response)
    (url_l, follower_l, following_l, username_l, account_create_date_l, post_date_time_l, verified_l,
     geolocation_l, retweet_l) = data_points(flattened_data)
    print(url_l, follower_l, following_l, username_l, account_create_date_l, post_date_time_l, verified_l,
          geolocation_l, retweet_l)
    post_freq = post_frequency(post_date_time_l)
    print(post_freq)
    domain_l = get_domain(url_l)
    print(domain_l)
    f2f_l = [a / b for a, b in zip(follower_l, following_l)]
    f2f_rat = 'Unknown'
    if len(f2f_l) != 0:
        f2f_ratio = sum(f2f_l) / len(f2f_l)
        if 0.1 <= f2f_ratio <= 1:
            f2f_rat = 'Normal'
        else:
            f2f_rat = 'Abnormal'
    print(f2f_rat)
    mal_stat = check_domain(domain_l)
    print(mal_stat)
    bot_or_not = prediction(mal_stat, f2f_rat, post_freq)
    print(bot_or_not)
    return jsonify({
        'result': bot_or_not,
        'mal_stat': mal_stat,
        'f2f_rat': f2f_rat,
        'post_freq': post_freq
    })


if __name__ == '__main__':
    app.run()
