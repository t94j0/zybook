import argparse
import parse
from zybook import login, get_activities

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
