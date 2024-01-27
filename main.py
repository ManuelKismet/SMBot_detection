from time import sleep
from datetime import datetime
from urllib.parse import urlsplit
import requests
from pywebio import start_server, pin
from pywebio.output import put_markdown, put_text, put_buttons, toast, put_row, put_column, put_code
from pywebio.pin import put_input, pin
import os

apikey = os.environ.get("API_Key")


# Twitter version 2 API to get account info endpoints
def api(account_id):
    url = "https://twitter-v24.p.rapidapi.com/search/"
    querystring = {"query": account_id, "limit": "2"}
    twitter_headers = {
        "X-RapidAPI-Key": apikey,
        "X-RapidAPI-Host": "twitter-v24.p.rapidapi.com"}
    response = requests.get(url, headers=twitter_headers, params=querystring)
    return response.json()


# API to check account name across other SM platforms----------------------------------------------------------
# check_user_url = "https://check-username.p.rapidapi.com/check/check/KismetKismet"
# check_user_headers = {
#     "X-RapidAPI-Key": "cc05abe945msh7cc26d5561cbae6p115cd3jsn85c96893f8fd",
#     "X-RapidAPI-Host": "check-username.p.rapidapi.com"}
# check_user_response = requests.get(check_user_url, headers=check_user_headers)

# print(response.json())#
# Get response and formate it from json to text
# json_response_raw = response.json()
# formatted_json_response_txt = json.dumps(json_response_raw, indent=4)


# Reformat the json response from Twitter to csv------------------------------------------------------------------
# flat_data = {}
def flatten(json_data, parent_key="", sep="."):
    flat_data = {}
    if isinstance(json_data, dict):
        for key, value in json_data.items():
            new_key = f"{parent_key}{sep}{key}" if parent_key else key
            if isinstance(value, (dict, list)):
                flat_data.update(flatten(value, new_key, sep=sep))
            else:
                flat_data[new_key] = value
    elif isinstance(json_data, list):
        for index, value in enumerate(json_data):
            new_key = f"{parent_key}{sep}{index}"
            if isinstance(value, (dict, list)):
                flat_data.update(flatten(value, new_key, sep=sep))
            else:
                flat_data[new_key] = value
    return flat_data


# flatten(response.json())

def data_points(met):
    url_data, follower, following, username, account_create_date = [], [], [], [], []
    post_date_time, verified, geolocation, retweets = [], [], [], []
    entry_first_string = "data.search_by_raw_query.search_timeline.timeline.instructions.0.entries."
    entry_mid_string = ".content.itemContent.tweet_results.result."
    entries = [
        "legacy.entities.media.0.expanded_url",
        "legacy.entities.urls.0.expanded_url",
        "core.user_results.result.legacy.followers_count",
        "core.user_results.result.legacy.friends_count",
        "core.user_results.result.legacy.name",
        "core.user_results.result.legacy.created_at",
        "legacy.created_at",
        "core.user_results.result.legacy.verified",
        "core.user_results.result.legacy.location",
        "legacy.retweet_count"
    ]
    for i in range(11):
        for entry in entries:
            entry_data = met.get(f"{entry_first_string}{i}{entry_mid_string}{entry}")
            if entry == entries[0] or entry == entries[1]:
                if entry_data is None:
                    pass
                else:
                    url_data.append(entry_data)
            if entry == entries[2]:
                if entry_data is None:
                    pass
                else:
                    follower.append(entry_data)
            if entry == entries[3]:
                if entry_data is None:
                    pass
                else:
                    following.append(entry_data)
            if entry == entries[4]:
                if entry_data is None:
                    pass
                else:
                    username.append(entry_data)
            if entry == entries[5]:
                if entry_data is None:
                    pass
                else:
                    account_create_date.append(entry_data)
            if entry == entries[6]:
                if entry_data is None:
                    pass
                else:
                    post_date_time.append(entry_data)
            if entry == entries[7]:
                if entry_data is None:
                    pass
                else:
                    verified.append(entry_data)
            if entry == entries[8]:
                if entry_data is None:
                    pass
                else:
                    geolocation.append(entry_data)
            if entry == entries[9]:
                if entry_data is None:
                    pass
                else:
                    retweets.append(entry_data)
    return [url_data, follower, following, username, account_create_date, post_date_time, verified, geolocation,
            retweets]


# virusTotal url spam check-------------------------------------------------------------------
def url_spam_analysis(domain_to_analyse):
    api_key = '94113a6fb2fb039cfa75ad704c0db9b41e9b7ddb12f7ee680f7d6c706e1def0b'
    api_url = 'https://www.virustotal.com/api/v3/urls'
    # domain_to_analyse = 'test.com'
    form_url = {'url': domain_to_analyse}
    headers = {'x-apikey': api_key}
    analysed_id = requests.post(api_url, headers=headers, data=form_url)
    analysis_id_value = (analysed_id.json()['data']['id'])
    get_real_id = analysis_id_value.split('-')
    real_id = get_real_id[1].strip()
    analysed_result = requests.get(f'{api_url}/{real_id}', headers=headers)
    harmless = (analysed_result.json()["data"]["attributes"]["last_analysis_stats"]["harmless"])
    malicious = (analysed_result.json()["data"]["attributes"]["last_analysis_stats"]["malicious"])
    return "harmless" if harmless > malicious else "malicious"


def get_domain(url_list):
    domain_list = []
    for i in range(len(url_list)):
        url_data = url_list[i]
        if url_data is None:
            pass
        else:
            split_url = urlsplit(url_data)
            domain_list.append(split_url.netloc)
    return domain_list


def check_domain(domain_list):
    malicious_statuses = []
    for domain in domain_list:
        if domain is None:
            pass
        else:
            malicious_statuses.append(url_spam_analysis(domain))
            sleep(62)
    return "malicious" if 'malicious' in malicious_statuses else "harmless"


def post_frequency(pdt):
    if len(pdt) < 2:
        return 'Normal'
    else:
        date_time_objects = [datetime.strptime(dt, '%a %b %d %H:%M:%S %z %Y') for dt in pdt]
        sorted_date_time_objects = sorted(date_time_objects)
        time_diffs = [sorted_date_time_objects[i + 1] - sorted_date_time_objects[i] for i in
                      range(len(sorted_date_time_objects) - 1)]
        posting_frequency_seconds = sum(diff.total_seconds() for diff in time_diffs) / len(time_diffs)

        return 'Normal' if posting_frequency_seconds > 60 else 'Abnormal'


def prediction(ms, fr, pf):
    if ms == 'malicious' and fr == 'Normal' and pf == 'Normal':
        return 'malicious Bot Account'
    elif ms == 'malicious' and fr == 'Abnormal' and pf == 'Normal':
        return 'malicious Bot Account'
    elif ms == 'malicious' and fr == 'Abnormal' and pf == 'Abnormal':
        return 'malicious Bot Account'
    elif ms == 'malicious' and fr == 'Normal' and pf == 'Abnormal':
        return 'malicious Bot Account'
    elif ms == 'harmless' and fr == 'Normal' and pf == 'Normal':
        return 'Possible Real Account'
    elif ms == 'harmless' and fr == 'Abnormal' and pf == 'Normal':
        return 'Less Likely Bot Account'
    elif ms == 'harmless' and fr == 'Abnormal' and pf == 'Abnormal':
        return 'Likely Bot Account'
    elif ms == 'harmless' and fr == 'Normal' and pf == 'Abnormal':
        return 'Possible Real Account'
    else:
        return "Can't determine account status"


def submit_handler():
    entered_pin = pin.pin_name
    if pin.pin_name:
        put_text(f'You entered: {entered_pin}')
        pin.pin_name = ''  # Clear the input field
        json_response = api(entered_pin)
        flattened_data = flatten(json_response)
        (url_l, follower_l, following_l, username_l, account_create_date_l, post_date_time_l, verified_l,
         geolocation_l, retweet_l) = data_points(flattened_data)
        post_freq = post_frequency(post_date_time_l)
        domain_l = get_domain(url_l)
        # print(follower_l, following_l, username_l, geolocation_l)
        f2f_l = [a / b for a, b in zip(follower_l, following_l)]
        f2f_rat = 'Unknown'
        # print(f2f_l)
        if len(f2f_l) == 0:
            pass
        else:
            f2f_ratio = sum(f2f_l) / len(f2f_l)
            if 0.1 <= f2f_ratio <= 1:
                f2f_rat = 'Normal'
            else:
                f2f_rat = 'Abnormal'
        mal_stat = check_domain(domain_l)
        bot_or_not = prediction(mal_stat, f2f_rat, post_freq)
        put_text(bot_or_not).style('width:280px;'
                                   'height:200px;'
                                   'display:inline-block;'
                                   'margin-top:50px;'
                                   'color:black;'
                                   'font-weight: bold;'
                                   'font-size:30px;'
                                   'background-color:darkgrey;'
                                   'border:2px solid black;'
                                   'text-align: center;')
        put_column([
            put_markdown('Stats').style('font-weight: bold;'),
            put_row([
                put_code('Malicious Link(s)'), None,
                put_code(mal_stat), None,
            ]),
            put_row([
                put_code('F2F Ratio'), None,
                put_code(f2f_rat), None,
            ]),
            put_row([
                put_code('Post Frequency'), None,
                put_code(post_freq), None,
            ])
        ]).style('float:right;'
                 'margin-top:30px;'
                 'width:350px;'
                 'display:inline-block;')
    else:
        toast('Enter ID for Query and Analysis 🔔')


def application():
    put_markdown('Twitter (X) Bot Account Detection').style('text-align:center;'
                                                            'color:darkgrey;'
                                                            'font-size:50px;'
                                                            'font-weight: bold;'
                                                            'text-decoration:underline')
    put_input('pin_name', placeholder='inter x account id with @')

    put_buttons(['Submit'], [lambda: submit_handler()])
    put_text('Results').style('text-align:center;'
                              'margin-top:50px;'
                              'color:white;'
                              'font-weight: bold;'
                              'font-size:40px;'
                              'background-color:#008CBA')

    put_text("###Prediction###...").style('width:max-content;'
                                          'display:block;'
                                          'margin-top:50px;'
                                          'color:black;'
                                          'font-weight: bold;'
                                          'font-size:30px;'
                                          'background-color:darkgrey;'
                                          )


# if __name__ == "__main__":
    # start_server(application, port=8088)
    # api('@XcatterBits')
