import csv
import json
from time import sleep
from urllib.parse import urlsplit
import requests
from pywebio import start_server, pin
from pywebio.output import put_markdown, put_text, put_buttons, clear, toast, put_table, put_row, put_column, put_code
from pywebio.pin import put_input, pin, put_textarea


# Twitter version 2 API to get account info endpoints
def api(account_id):
    url = "https://twitter-v24.p.rapidapi.com/search/"
    querystring = {"query": account_id, "limit": "5"}
    twitter_headers = {
        "X-RapidAPI-Key": "cc05abe945msh7cc26d5561cbae6p115cd3jsn85c96893f8fd",
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
    for i in range(11):
        media_url_entry = met.get(
            f"data.search_by_raw_query.search_timeline.timeline.instructions.0.entries.{i}.content.itemContent."
            f"tweet_results.result.legacy.entities.media.0.expanded_url")
        if media_url_entry is None:
            pass
        else:
            url_data.append(media_url_entry)

        url_entry = met.get(
            f"data.search_by_raw_query.search_timeline.timeline.instructions.0.entries.{i}.content.itemContent."
            f"tweet_results.result.legacy.entities.urls.0.expanded_url")
        if url_entry is None:
            pass
        else:
            url_data.append(url_entry)

        follower_entry = met.get(
            f"data.search_by_raw_query.search_timeline.timeline.instructions.0.entries.{i}.content.itemContent."
            f"tweet_results.result.core.user_results.result.legacy.followers_count")
        if follower_entry is None:
            pass
        else:
            follower.append(follower_entry)

        following_entry = met.get(
            f"data.search_by_raw_query.search_timeline.timeline.instructions.0.entries.{i}.content.itemContent."
            f"tweet_results.result.core.user_results.result.legacy.friends_count")
        if following_entry is None:
            pass
        else:
            following.append(following_entry)

        username_entry = met.get(
            f"data.search_by_raw_query.search_timeline.timeline.instructions.0.entries.{i}.content.itemContent."
            f"tweet_results.result.core.user_results.result.legacy.name")
        if username_entry is None:
            pass
        else:
            username.append(username_entry)

        account_create_date_entry = met.get(
            f"data.search_by_raw_query.search_timeline.timeline.instructions.0.entries.{i}.content.itemContent."
            f"tweet_results.result.core.user_results.result.legacy.created_at")
        if account_create_date_entry is None:
            pass
        else:
            account_create_date.append(account_create_date_entry)

        post_date_time_entry = met.get(
            f"data.search_by_raw_query.search_timeline.timeline.instructions.0.entries.{i}.content.itemContent."
            f"tweet_results.result.legacy.created_at")
        if post_date_time_entry is None:
            pass
        else:
            post_date_time.append(post_date_time_entry)

        verified_entry = met.get(
            f"data.search_by_raw_query.search_timeline.timeline.instructions.0.entries.{i}.content.itemContent."
            f"tweet_results.result.core.user_results.result.legacy.verified")
        if verified_entry is None:
            pass
        else:
            verified.append(verified_entry)

        geolocation_entry = met.get(
            f"data.search_by_raw_query.search_timeline.timeline.instructions.0.entries.{i}.content.itemContent."
            f"tweet_results.result.core.user_results.result.legacy.location")
        if geolocation_entry is None:
            pass
        else:
            geolocation.append(geolocation_entry)

        retweets_entry = met.get(
            f"data.search_by_raw_query.search_timeline.timeline.instructions.0.entries.{i}.content.itemContent."
            f"tweet_results.result.legacy.retweet_count")
        if retweets_entry is None:
            pass
        else:
            retweets.append(retweets_entry)
    print([url_data, follower, following, username, account_create_date, post_date_time, verified, geolocation,
           retweets])
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
    print(analysed_result.text)
    return analysed_result.text


def extract_domain(full_url):
    split_url = urlsplit(full_url)
    return split_url.netloc


def get_domain():
    url_list = []
    flat_data = flatten(response.json())
    for i in range(11):
        url_data = flat_data.get(f"data.search_by_raw_query.search_timeline.timeline.instructions.0.entries.{i}.content"
                                 f".itemContent.tweet_results.result.legacy.entities.urls.0.expanded_url")
        if url_data is None:
            pass
        else:
            url_list.append(extract_domain(url_data))
    return url_list


def check_domain(domain_list):
    print(domain_list)
    for domain in domain_list:
        url_spam_analysis(domain)
        sleep(65)


def bot_detection():
    check_domain(get_domain())


def application():
    put_markdown('Twitter (X) Bot Account Detection').style('text-align:center;'
                                                            'color:darkgrey;'
                                                            'font-size:50px;'
                                                            'font-weight: bold;'
                                                            'text-decoration:underline')
    put_input('pin_name', placeholder='inter x account id with @')

    def submit_handler():
        entered_pin = pin.pin_name
        if pin.pin_name:
            put_text(f'You entered: {entered_pin}')
            pin.pin_name = ''  # Clear the input field
            json_response = api(entered_pin)
            flattened_data = flatten(json_response)
            data_points(flattened_data)
        else:
            toast('Enter ID for Query and Analysis 🔔')

    put_buttons(['Submit'], [lambda: submit_handler()])
    put_text('Results').style('text-align:center;'
                              'margin-top:50px;'
                              'color:white;'
                              'font-weight: bold;'
                              'font-size:40px;'
                              'background-color:#008CBA')

    put_textarea(name='Bot', label=' Module Predict', placeholder='Waiting Prediction ...',
                 readonly=True).style('width:350px;'
                                      'display:inline-block;'
                                      'margin-top:30px')
    put_column([
        put_markdown('Stats'),
        put_row([
            put_code('xcatter2'), None,
            put_code('xcatter2'), None,
        ]),
        put_row([
            put_code('xcatter1'), None,
            put_code('xcatter1'), None,
        ]),
        put_row([
            put_code('xcatter'), None,
            put_code('xcatter'), None,
        ])
    ]).style('float:right;'
             'display:inline-block;'
             'margin-top:30px;'
             'width:400px')


if __name__ == "__main__":
    start_server(application, port=8088)

# flattened_csv = "flattened_csv.csv"
# # text_file = "text_file.txt"
# header_columns = list(flat_data.keys())
# row_values = list(flat_data.values())
# #
# # Write the formatted data to CSV file-----------------------------------------------------------------------
# with open(flattened_csv, "w", encoding="utf-8") as file:
#     writer = csv.writer(file)
#     writer.writerow(header_columns)
#     writer.writerow(row_values)

# Write the formatted data to text file-----------------------------------------------------------------------
# with open(text_file, "w") as f:
#     f.write(formatted_json_response_txt)


# print(check_user_response.json())
# with open(text_file, "w") as f:
#     f.write(json.dumps(response.json(), indent=4))
