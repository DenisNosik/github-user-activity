import requests


def get_github_user_activity(username):
    url = f"https://api.github.com/users/{username}/events"

    push_summary = {}

    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()

        if response.status_code == 200:
            for event in data:
                match event["type"]:
                    case "CreateEvent":
                        print(f"{username} created new event: {event['repo']['name']}")
                    case "PushEvent":
                        repo_name = event['repo']['name']
                        if repo_name in push_summary:
                            push_summary[repo_name] += 1
                        else:
                            push_summary[repo_name] = 1
                    case "IssueCommentEvent":
                        print(f"{username} commented on issue: {event['payload']['issue']['number']}")
                    case "WatchEvent":
                        print(f"{username} starred: {event['repo']['name']}")

            # counts how many identical commits there were
            for repo, total in push_summary.items():
                if repo != 0:
                    print(f"{username} pushed {total} commit(s) to: {repo}")


    except requests.exceptions.HTTPError as http_error:
        match response.status_code:
            case 400:
                print("Bad request\nPlease check your input")
            case 401:
                print("Unauthorized")
            case 403:
                print("Forbidden\nAccess denied")
            case 404:
                print("Not found")
            case 500:
                print("Internal Server Error")
            case 502:
                print("Bad Gateway")
            case 503:
                print("Service Unavailable")
            case 504:
                print("Gateway Timeout\nNo response from the server")
            case _:
                print(f"HTTP Error occurred\n{http_error}")

    except requests.exceptions.ConnectionError:
        print("Connection Error\nCheck your internet connection")
    except requests.exceptions.Timeout:
        print("Timeout Error\nThe request timed out")
    except requests.exceptions.TooManyRedirects:
        print("Too many Redirects")
    except requests.exceptions.RequestException as req_error:
        print(f"Request Error\n{req_error}")

if __name__ == "__main__":
    while True:
        input_name = input("Please enter the GitHub username(x - to exit): ")
        if input_name != "x" and input_name != "":
            get_github_user_activity(input_name)
        else:
            break