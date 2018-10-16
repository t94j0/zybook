#!/usr/bin/env python3
import argparse
import requests
import datetime
import parse

def login(username, password):
    SIGNIN_URL = 'https://zyserver.zybooks.com/v1/signin'
    headers = {
	    'Accept': 'application/json, text/javascript, */*; q=0.01',
	    'Accept-Encoding': 'gzip, deflate, br',
	    'Accept-Language': 'en-US,en;q=0.9',
	    'Origin': 'https://learn.zybooks.com',
	    'Referer': 'https://learn.zybooks.com/signin',
	    'Content-Type': 'application/json',
	    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36',
	    }

    payload = '{"email": "%s", "password": "%s"}' % (username, password)
    ret = requests.post(SIGNIN_URL, data=payload, headers=headers)
    return ret.json()["session"]["auth_token"]

def get_activities(URL, access_code):
    URL_GET = '%s?auth_token=%s' % (URL, access_code)
    headers = {
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'en-US,en;q=0.9',
        'Referer': URL,
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36',
    }
    ret = requests.get(URL_GET, headers=headers)
    resources = ret.json()["section"]["content_resources"]
    for resource in resources:
        if "options" in resource["payload"]:
            options = resource["payload"]["options"]
            if "terms" in options:
                row = [term["term"] for term in options["terms"]]
                print(row)
        if "questions" in resource["payload"]:
            questions = resource["payload"]["questions"]
            for question in questions:
                if "answers" in question:
                    print(question["answers"])
                if "choices" in question:
                    correct = [ choice["label"] for choice in question["choices"] if choice["correct"] ]
                    value = correct[0]
                    if isinstance(value, (list,)):
                        print(value[0]["text"])
                    else:
                        print(value)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Solve ZyBooks Section')
    parser.add_argument('url', metavar='URL', type=str, help='Problem to solve')
    parser.add_argument('-u', '--username', type=str, help='username to log in to')
    parser.add_argument('-p', '--password', type=str, help='password to log in with')
    args = parser.parse_args()

    results = parse.parse("https://learn.zybooks.com/zybook/{}/chapter/{}/section/{}", args.url)
    URL = "https://zyserver.zybooks.com/v1/zybook/{}/chapter/{}/section/{}".format(results[0], results[1], results[2])
    access_code = login(args.username, args.password)
    get_activities(URL, access_code)
