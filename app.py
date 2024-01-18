import os
from flask import Flask, render_template, request, jsonify, flash, redirect, get_flashed_messages, url_for
from main import *

app = Flask(__name__)
app.secret_key = os.urandom(24)


@app.route('/', methods=['GET'])
def index():
    return render_template("index.html")


@app.route('/submit', methods=['POST'])
def submit():
    if request.method == "POST":
        input_id = request.form['input']
        if input_id == "" or input_id[0] != "@":
            flash('Enter Valid ID 🔔', 'info')
            return redirect(url_for('index'))
        else:
            flash(f'You entered {input_id}')
            return redirect(url_for('process_data', input_id=input_id))


@app.route('/process_data/<input_id>')
def process_data(input_id):
    json_response = api(input_id)
    flattened_data = flatten(json_response)
    (url_l, follower_l, following_l, username_l, account_create_date_l, post_date_time_l, verified_l,
     geolocation_l, retweet_l) = data_points(flattened_data)
    post_freq = post_frequency(post_date_time_l)
    domain_l = get_domain(url_l)
    f2f_l = [a / b for a, b in zip(follower_l, following_l)]
    f2f_rat = 'Unknown'
    if len(f2f_l) != 0:
        f2f_ratio = sum(f2f_l) / len(f2f_l)
        if 0.1 <= f2f_ratio <= 1:
            f2f_rat = 'Normal'
        else:
            f2f_rat = 'Abnormal'
    mal_stat = check_domain(domain_l)
    bot_or_not = prediction(mal_stat, f2f_rat, post_freq)
    return jsonify({
        'result': bot_or_not,
        'mal_stat': mal_stat,
        'f2f_rat': f2f_rat,
        'post_freq': post_freq
    })


# @app.route('/submit', methods=['POST submit():'])
# def submit():
#     entered_pin = request.form.get('input')
#     if entered_pin:
#         json_response = api(entered_pin)
#         flattened_data = flatten(json_response)
#         (url_l, follower_l, following_l, username_l, account_create_date_l, post_date_time_l, verified_l,
#          geolocation_l, retweet_l) = data_points(flattened_data)
#         post_freq = post_frequency(post_date_time_l)
#         domain_l = get_domain(url_l)
#         f2f_l = [a / b for a, b in zip(follower_l, following_l)]
#         f2f_rat = 'Unknown'
#         if len(f2f_l) != 0:
#             f2f_ratio = sum(f2f_l) / len(f2f_l)
#             if 0.1 <= f2f_ratio <= 1:
#                 f2f_rat = 'Normal'
#             else:
#                 f2f_rat = 'Abnormal'
#         mal_stat = check_domain(domain_l)
#         bot_or_not = prediction(mal_stat, f2f_rat, post_freq)
#         return jsonify({
#             'result': bot_or_not,
#             'mal_stat': mal_stat,
#             'f2f_rat': f2f_rat,
#             'post_freq': post_freq
#         })
#     else:
#         return jsonify({'error': 'Enter ID for Query and Analysis 🔔'})


if __name__ == '__main__':
    app.run(debug=True)
