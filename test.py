f2f_l = []
if len(f2f_l) is None:
    pass
else:
    print(f2f_l)


# from datetime import datetime
#
# # Your list of post_date_time strings
# post_date_times = [
#     'Thu Feb 05 06:00:21 +0000 2015',
#     'Sat Mar 21 03:06:06 +0000 2015',
#     'Thu Feb 26 08:18:44 +0000 2015',
#     'Thu Feb 26 08:16:04 +0000 2015',
#     'Thu Feb 26 08:28:11 +0000 2015'
# ]
#
# # Convert strings to datetime objects
# date_time_objects = [datetime.strptime(dt, '%a %b %d %H:%M:%S %z %Y') for dt in post_date_times]
# print(date_time_objects)
# # Sort datetime objects
# sorted_date_time_objects = sorted(date_time_objects)
# print(sorted_date_time_objects)
# # Calculate time differences
# time_diffs = [sorted_date_time_objects[i+1] - sorted_date_time_objects[i] for i in range(len(sorted_date_time_objects)-1)]
# print(time_diffs)
#
# # Calculate posting frequency in seconds
# posting_frequency_seconds = sum(diff.total_seconds() for diff in time_diffs) / len(time_diffs)
# print(posting_frequency_seconds)
# print(posting_frequency_seconds/60)
# # Convert posting frequency to a more human-readable format
# posting_frequency_hours = posting_frequency_seconds / 3600
# print(posting_frequency_hours/24)
#
# print(f"Average posting frequency: {posting_frequency_hours:.2f} hours")


# import csv
# import random
#
# # Generate random numbers
# random_numbers = [random.randint(1, 10000) for _ in range(10000)]
#
# # Shuffle the list to randomize the order
# random.shuffle(random_numbers)
#
# # Split the list into two columns
# column1 = random_numbers[:5000]
# column2 = random_numbers[5000:]
#
# # Combine the two columns into rows
# rows = list(zip(column1, column2))
#
# # Write to CSV file
# with open('random_numbers.csv', 'w', newline='') as csvfile:
#     csvwriter = csv.writer(csvfile)
#     csvwriter.writerow(['Column1', 'Column2'])  # Header row
#     csvwriter.writerows(rows)

# from pywebio import start_server, pin
# from pywebio.output import put_markdown, put_text, put_buttons, clear, toast, put_table, put_row, put_column, put_code
# from pywebio.pin import put_input, pin, put_textarea


# def application():
#     put_markdown('Twitter (X) Bot Account Detection').style('text-align:center;'
#                                                             'color:darkgrey;'
#                                                             'font-size:50px;'
#                                                             'font-weight: bold;'
#                                                             'text-decoration:underline')
#     put_input('pin_name', placeholder='inter x account id with @')
#
#     put_buttons(['Submit'], [lambda: submit_handler()])
#     put_text('Results').style('text-align:center;'
#                               'margin-top:50px;'
#                               'color:white;'
#                               'font-weight: bold;'
#                               'font-size:40px;'
#                               'background-color:#008CBA')
#
#     put_textarea(name='Bot', label=' Module Predict', placeholder='Waiting Prediction ...',
#                  readonly=True).style('width:350px;'
#                                       'display:inline-block;'
#                                       'margin-top:30px')
#     put_column([
#         put_markdown('Stats'),
#         put_row([
#             put_code('xcatter2'), None,
#             put_code('xcatter2'), None,
#         ]),
#         put_row([
#             put_code('xcatter1'), None,
#             put_code('xcatter1'), None,
#         ]),
#         put_row([
#             put_code('xcatter'), None,
#             put_code('xcatter'), None,
#         ])
#     ]).style('float:right;'
#              'display:inline-block;'
#              'margin-top:30px;'
#              'width:400px')
#
#     def submit_handler():
#         entered_pin = pin.pin_name
#         if pin.pin_name:
#             put_text(f'You entered: {entered_pin}')
#             pin.pin_name = ''  # Clear the input field
#         else:
#             toast('Enter ID for Query and Analysis 🔔')

#
# if __name__ == '__main__':
#     start_server(application, port=8088)
# import requests
#
# key = '94113a6fb2fb039cfa75ad704c0db9b41e9b7ddb12f7ee680f7d6c706e1def0b'
# url = 'https://www.virustotal.com/api/v3/urls'
# domain = 'https://youtu.be'
# form_url = {'url': domain}
# headers = {'x-apikey': key}
# response = requests.post(url, headers=headers, data=form_url)
# analysis_id_value = (response.json()['data']['id'])
# get_real_id = analysis_id_value.split('-')
# real_id = get_real_id[1].strip()
# result = requests.get(f'{url}/{real_id}', headers=headers)
# print(result.text)

# import dns.resolver
# domain = 'br-icloud.com.br'
# key = "uoiu26lyudmx4yrr73hnalpc34"
##
# # Construct the DBL query domain
# dbl_domain = f'{domain}.{key}.dbl.dq.spamhaus.net'
#
# # Perform the DNS query
# response = dns.resolver.Resolver().resolve(dbl_domain)
# if response:
#     print(f'The domain {domain} is listed in Spamhaus DBL.')
#     print(response)
# else:
#     print(f'The domain {domain} is not listed in Spamhaus DBL.')
# url = "https://api.spamhaus.org/api/v1/login"
# pass = "pkJichwKQtL3"
# responses = requests.post(url, '{"username":"kismetkoranteng@yahoo.com", "password":"pass", "realm":"intel"}')
# token = responses.json()['token']
#
#
# headers = {"Authorization": f"Bearer {token}",
#            "Accept": "application/json"}
# result = requests.get('https://api.spamhaus.org/api/intel/v1/byobject/domain/paypa1.com', headers=headers)
# print(result.status_code)
# print(result.json)

# from pywebio.input import input, FLOAT
# from pywebio.output import put_text, put_html
# from pywebio import start_server
#
#
# def calculate_square_root():
#     put_text("Welcome to the Square Root Calculator!")
#
#     # Get user input
#     number = input("Enter a number to calculate its square root:", type=FLOAT)
#
#     # Calculate square root
#     result = number ** 0.5
#
#     # Display the result
#     put_html(f"The square root of {number} is: <strong>{result}</strong>")
#
#
# if __name__ == "__main__":
#     # Start PyWebIO server
#     start_server(calculate_square_root, port=8080)
#
# # import tldextract
#
# url = "https://example.com/path/page"
# extracted_info = tldextract.extract(url)
# print(extracted_info.domain)
