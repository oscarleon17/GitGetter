from operator import itemgetter
import requests
import re
import json
# The function below will ask the user for a github username and print the json from the github API.
def getjson():

    # Asking the suer for the username and removing all left and right spaces
    username = input("Enter a username from github: ")
    username = username.strip()

    # If username contains ONLY alphanumeric characters and hyphens, continue, otherwise return message
    if re.match('^[\w-]+$', username):

        # Setting root and path for our endpoint.
        root = f"https://api.github.com"
        path = f"/users/{username}"
        repos = f"/repos"
        endpoint = f"{root}{path}"
        reposendpoint = f"{root}{path}{repos}"

        # Using the requests package, use a GET call to get raw data from the github API
        # Format the raw data to json and filter for specific fields
        r = requests.get(endpoint)
        data = r.json()
        data_filtered = {key: data[key] for key in
                         data.keys() & {'login', 'name', 'avatar_url', 'location', 'email', 'html_url', 'created_at',
                                        'repos'}}

        # Perform a second GET call to get raw data from the github API and get name and urls for
        # specified username repos
        r2 = requests.get(reposendpoint)
        reposdata = r2.json()
        # Mapping repo names to a list
        repo_name = list(map(itemgetter('name'), reposdata))
        # Mapping repo urls to a list
        repo_url = list(map(itemgetter('html_url'), reposdata))
        repos_filtered = []

        # Zipping Repo names and urls into a list of dictionaries (key/value pairs)
        for i, j in zip(repo_name, repo_url):
            repos_filtered.append({"name": i, "url": j})

        # Replacing the original 'repos' value from the first json, with the values obtained from the second json
        data_filtered['repos'] = repos_filtered

        # Getting and formatting date
        date_formatted = data_filtered['created_at']
        date_formatted = re.sub('[A-Z]', ' ', date_formatted)
        data_filtered['created_at'] = date_formatted.strip()

        # Printing JSON for user to read
        print(json.dumps(data_filtered, indent=2))

    else:
        print('Please try again and enter a valid username. Only alphanumeric characters or hyphens are allowed')
    pass

# Fuction that prints menu to console for user interaction
def menu():
    print('Type and enter the following to perform an action.')
    print('     1: Get user data from github api')
    print('     quit: Exit program.')
    pass

# Main function, asks for user input and performs what user selects from menu.
def main():
    while True:
        menu()
        selection = input("Please type your selection: ")
        if selection == 'quit':
            return
        elif selection == '1':
            getjson()
        else:
            print('No such selection exists, try again')


if __name__ == '__main__':

    # Call main function
    main()
