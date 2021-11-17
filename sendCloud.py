import http.client
import json
import requests
from boto3 import Session as AWSSession
from requests_aws4auth import AWS4Auth
from datetime import datetime
from datetime import timedelta
from logger import *

# Constants Copied from AppSync API 'Settings'
API_URL = 'https://w3lhm34x5jgxlbpr7zzxx7ckqq.appsync-api.ap-southeast-2.amazonaws.com/graphql'
API_KEY = 'da2-hgqwkvc7ezeqlp2nc5uih2zjca'

def send_gql_cloud(recs):
    status = 'FAILED'
    HOST = API_URL.replace('https://', '').replace('/graphql', '')

    #
    conn = http.client.HTTPSConnection(HOST, 443)
    headers = {
        'Content-type': 'application/graphql',
        'x-api-key': API_KEY,
        'host': HOST
    }

    # Perform a query to get a Todo ID
    graphql_query = {
        'query': 'query{ listTodos { items {id title} } }'
    }
    query_data = json.dumps(graphql_query)
    conn.request('POST', '/graphql', query_data, headers)
    response = conn.getresponse()

    response_string = response.read().decode('utf-8')
    print(response_string)

    # Substitue the ID in the GraphQL Mutation Variables
    response_json = json.loads(response_string)
    id = response_json['data']['listTodos']['items'][0]['id']
    new_title = "Get Lunch"

    graphql_mutation = {
        'query': 'mutation($in:UpdateTodoInput!){updateTodo(input:$in){id title}}',
        'variables': '{ "in": {"id":"' + id + '", "title":"' + new_title + '"} }'
    }
    mutation_data = json.dumps(graphql_mutation)

    # Now Perform the Mutation
    conn.request('POST', '/graphql', mutation_data, headers)
    response = conn.getresponse()

    response_string = response.read().decode('utf-8')
    print(response_string)
    return status


# convert record object to GQL mutation query string
# an example is as the following:
  # mutation = """
    #     mutation MyMute {
    #   createPeople(input:[{
    #     phones : ["510-760-3989", "925-623-2794"],
    #     lastName : "SC",
    #     firstName : "CS",
    #     emails : ["111@222.com", "222@333.com"],
    #     birthday : "1970-01-01",
    #     addrs : [
    #         {	street1: "200 ABC St. Apt B1",
    #             street2: "None",
    #             city: "Austin",
    #             state: "TX",
    #             zip: "78753",
    #             startDate: "1970-01-01",
    #             endDate: "1980-01-01"
    #         },
    #         {	street1: "300 ABC St. Apt 121",
    #             street2: "None",
    #             city: "Tucson",
    #             state: "AZ",
    #             zip: "78753",
    #             startDate: "1981-01-01",
    #             endDate: "1991-01-01"
    #         }
    #     ]
    #   }]) [{
    #     id
    #     phones
    #     lastName
    #     firstName
    #     emails
    #     birthday
    #     addrs {
    #       city
    #       endDate
    #       startDate
    #       state
    #       street1
    #       street2
    #       zip
    #     }
    #   }]
    # }"""
def convert_ppl_rec_to_query_string(recs):
    query_string = """
        mutation MyMute {
      createPeople(input:[
    """
    rec_string = ""
    for i in range(len(recs)):
        rec_string = rec_string + recs[i].genPrintable()
        if i != len(recs) - 1:
            rec_string = rec_string + ', '
    print('rec_string====>')
    print(rec_string)

    tail_string = """
    ]) 
    } """
    query_string = query_string + rec_string + tail_string
    print(query_string)
    return query_string


def convert_mffn_rec_to_query_string(recs, mf, cult):
    query_string = """
        mutation MyMute {
      createMFGivenNames(input:[
    """
    rec_string = ""
    for i in range(len(recs)):
        rec_string = rec_string + "{ firstName: \"" + recs[i].firstName() + "\", "
        rec_string = rec_string + "sex: \"" + mf + "\", "
        rec_string = rec_string + "cult: " + cult + " }"
        if i != len(recs) - 1:
            rec_string = rec_string + ', '

    tail_string = """
    ]) 
    } """
    query_string = query_string + rec_string + tail_string
    print(query_string)
    return query_string


def set_up_cloud():
    ACCESS_KEY = 'AKIAZWU23DOOXXTWC2W2'
    SECRET_KEY = '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'
    REGION = 'us-east-1'
    session = requests.Session()
    session.auth = AWS4Auth(
        # An AWS 'ACCESS KEY' associated with an IAM user.
        ACCESS_KEY,
        # The 'secret' that goes with the above access key.
        SECRET_KEY,
        # The region you want to access.
        REGION,
        # The service you want to access.
        'appsync'
    )

    return session

# interface appsync, directly use HTTP request.
# Use AWS4Auth to sign a requests session
def send_ppl_info_to_cloud(session, recs, logfile='C:/CrawlerData/scrape_log.txt', mode='Data'):

    status = 0
    dt = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    # As found in AWS Appsync under Settings for your endpoint.
    # Constants Copied from AppSync API 'Settings'

    receiverId = "***"
    APPSYNC_API_ENDPOINT_URL = 'https://w3lhm34x5jgxlbpr7zzxx7ckqq.appsync-api.us-east-1.amazonaws.com/graphql'
    APPSYNC_API_KEY = 'da2-hgqwkvc7ezeqlp2nc5uih2zjca'
    # Use JSON format string for the query. It does not need reformatting.

    headers = {
        'Content-Type': "application/graphql",
        'x-api-key': APPSYNC_API_KEY,
        'cache-control': "no-cache",
    }

    if mode == 'Data':
        mutation = convert_ppl_rec_to_query_string(recs)
    else:
        mutation = recs

    print('MUTATION-------------->')
    print(mutation)
    # Now we can simply post the request...
    response = session.request(
        url=APPSYNC_API_ENDPOINT_URL,
        method='POST',
        headers=headers,
        json={'query': mutation}
    )

    #save response to a log file. with a time stamp.
    words = 'send_mf_info_to_cloud========>\n' + str(recs[0]) + '\n' + str(recs[len(recs)-1]) + '\n' + dt + '\n'
    words = words + response.text
    log2file(words, 'None', 'None', logfile)
    return status


# interface appsync, directly use HTTP request.
# Use AWS4Auth to sign a requests session
def send_mf_info_to_cloud(session, recs, mf, cult, logfile='C:/CrawlerData/scrape_log.txt', mode='Data'):

    status = 0
    dt = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    # As found in AWS Appsync under Settings for your endpoint.
    # Constants Copied from AppSync API 'Settings'

    receiverId = "***"
    APPSYNC_API_ENDPOINT_URL = 'https://w3lhm34x5jgxlbpr7zzxx7ckqq.appsync-api.us-east-1.amazonaws.com/graphql'
    APPSYNC_API_KEY = 'da2-hgqwkvc7ezeqlp2nc5uih2zjca'
    # Use JSON format string for the query. It does not need reformatting.

    headers = {
        'Content-Type': "application/graphql",
        'x-api-key': APPSYNC_API_KEY,
        'cache-control': "no-cache",
    }


    # query = """
    #     query MyQuery {
    #   getPeople(id: "123") {
    #     id
    #     phones
    #     lastName
    #     firstName
    #     emails
    #     birthday
    #     addrs {
    #       city
    #       endDate
    #       startDate
    #       state
    #       street1
    #       street2
    #       zip
    #     }
    #   }
    # }"""

    if mode == 'Data':
        mutation = convert_mffn_rec_to_query_string(recs, mf, cult)
    else:
        mutation = recs

    print('MUTATION-------------->')
    print(mutation)
    # Now we can simply post the request...
    response = session.request(
        url=APPSYNC_API_ENDPOINT_URL,
        method='POST',
        headers=headers,
        json={'query': mutation}
    )
    #save response to a log file. with a time stamp.
    words = 'send_mf_info_to_cloud========>\n' + str(recs[0]) + '\n' + str(recs[len(recs)-1]) + '\n' + dt + '\n'
    words = words + response.text
    log2file(words, 'None', 'None', logfile)
    return status


