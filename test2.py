# # Twitter version 2 API to get account info endpoints
# import csv
# import json
#
# import requests
#
# url = "https://twitter-v24.p.rapidapi.com/search/"
# querystring = {"query": "@KismetKismet", "limit": "1"}
# twitter_headers = {
#     "X-RapidAPI-Key": "cc05abe945msh7cc26d5561cbae6p115cd3jsn85c96893f8fd",
#     "X-RapidAPI-Host": "twitter-v24.p.rapidapi.com"}
# response = requests.get(url, headers=twitter_headers, params=querystring)
#
#
# # Reformat the json response from Twitter to #csv------------------------------------------------------------------
# # flat_data = {}
# def flatten(json_data, parent_key="", sep="."):
#     flat_data = {}
#     if isinstance(json_data, dict):
#         for key, value in json_data.items():
#             new_key = f"{parent_key}{sep}{key}" if parent_key else key
#             if new_key:  # Skip empty keys
#                 if isinstance(value, (dict, list)):
#                     flat_data.update(flatten(value, new_key, sep=sep))
#                 else:
#                     flat_data[new_key] = value
#     elif isinstance(json_data, list):
#         for index, value in enumerate(json_data):
#             new_key = f"{parent_key}{sep}{index}"
#             if new_key:  # Skip empty keys
#                 if isinstance(value, (dict, list)):
#                     flat_data.update(flatten(value, new_key, sep=sep))
#                 else:
#                     flat_data[new_key] = value
#     return flat_data
#
#
# def write_data_file(data):
#     formatted_json_response_txt = json.dumps(response.json(), indent=4)
#     flattened_csv = "flattened_csv.csv"
#     text_file = "text_file.txt"
#     header_columns = list(data.keys())
#     row_values = list(data.values())
#     #
#     # Write the formatted data to CSV file-----------------------------------------------------------------------
#     with open(flattened_csv, "w", encoding="utf-8") as file:
#         writer = csv.writer(file)
#         writer.writerow(header_columns)
#         writer.writerow(row_values)
#
#     # Write the formatted data to text file-----------------------------------------------------------------------
#     with open(text_file, "w") as f:
#         f.write(formatted_json_response_txt)
#
#
# def data_points(met):
#     url_data, follower, following, username, account_create_date = [], [], [], [], []
#     post_date_time, verified, geolocation, retweets = [], [], [], []
#     for i in range(11):
#         media_url_entry = met.get(
#             f"data.search_by_raw_query.search_timeline.timeline.instructions.0.entries.{i}.content.itemContent."
#             f"tweet_results.result.legacy.entities.media.0.expanded_url")
#         if media_url_entry is None:
#             pass
#         else:
#             url_data.append(media_url_entry)
#
#         url_entry = met.get(
#             f"data.search_by_raw_query.search_timeline.timeline.instructions.0.entries.{i}.content.itemContent."
#             f"tweet_results.result.legacy.entities.urls.0.expanded_url")
#         if url_entry is None:
#             pass
#         else:
#             url_data.append(url_entry)
#
#         follower_entry = met.get(
#             f"data.search_by_raw_query.search_timeline.timeline.instructions.0.entries.{i}.content.itemContent."
#             f"tweet_results.result.core.user_results.result.legacy.followers_count")
#         if follower_entry is None:
#             pass
#         else:
#             follower.append(follower_entry)
#
#         following_entry = met.get(
#             f"data.search_by_raw_query.search_timeline.timeline.instructions.0.entries.{i}.content.itemContent."
#             f"tweet_results.result.core.user_results.result.legacy.friends_count")
#         if following_entry is None:
#             pass
#         else:
#             following.append(following_entry)
#
#         username_entry = met.get(
#             f"data.search_by_raw_query.search_timeline.timeline.instructions.0.entries.{i}.content.itemContent."
#             f"tweet_results.result.core.user_results.result.legacy.name")
#         if username_entry is None:
#             pass
#         else:
#             username.append(username_entry)
#
#         account_create_date_entry = met.get(
#             f"data.search_by_raw_query.search_timeline.timeline.instructions.0.entries.{i}.content.itemContent."
#             f"tweet_results.result.core.user_results.result.legacy.created_at")
#         if account_create_date_entry is None:
#             pass
#         else:
#             account_create_date.append(account_create_date_entry)
#
#         post_date_time_entry = met.get(
#             f"data.search_by_raw_query.search_timeline.timeline.instructions.0.entries.{i}.content.itemContent."
#             f"tweet_results.result.legacy.created_at")
#         if post_date_time_entry is None:
#             pass
#         else:
#             post_date_time.append(post_date_time_entry)
#
#         verified_entry = met.get(
#             f"data.search_by_raw_query.search_timeline.timeline.instructions.0.entries.{i}.content.itemContent."
#             f"tweet_results.result.core.user_results.result.legacy.verified")
#         if verified_entry is None:
#             pass
#         else:
#             verified.append(verified_entry)
#
#         geolocation_entry = met.get(
#             f"data.search_by_raw_query.search_timeline.timeline.instructions.0.entries.{i}.content.itemContent."
#             f"tweet_results.result.core.user_results.result.legacy.location")
#         if geolocation_entry is None:
#             pass
#         else:
#             geolocation.append(geolocation_entry)
#
#         retweets_entry = met.get(
#             f"data.search_by_raw_query.search_timeline.timeline.instructions.0.entries.{i}.content.itemContent."
#             f"tweet_results.result.legacy.retweet_count")
#         if retweets_entry is None:
#             pass
#         else:
#             retweets.append(retweets_entry)
#     print([url_data, follower, following, username, account_create_date, post_date_time, verified, geolocation,
#            retweets])
#     return [url_data, follower, following, username, account_create_date, post_date_time, verified, geolocation,
#             retweets]
#
#
# if __name__ == '__main__':
#     data_points(flatten(response.json()))
#     write_data_file(flatten(response.json()))
