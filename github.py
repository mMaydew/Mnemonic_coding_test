#!/usr/bin/env python3

import argparse
from requests import get
from tabulate import tabulate
from typing import Optional
from typing import Sequence
# Import json for reading the token file
from json import load


def get_profile_data(profile_url: str, token: str = ""):
    """
        A function to get user data\n
        args:\n
            \tprofile_url - URL for the users repo list\n
            \ttoken - personal access token
    """

    get_user_info = get(
        profile_url,
        headers={
            "Accept": "application/vnd.github.v3+json"
        },
        auth=(token, "x-oauth-basic")
    ).json()

    try:
        # Put the user information in a dict
        parsed_user_info = {
            "username": get_user_info["login"],
            "name": get_user_info["name"],
            "location": get_user_info["location"],
            "repos_url": get_user_info["repos_url"]
        }
    # if there is no data, there is either no user with that username
    # or the token is wrong/invalid - Then we exit with a message
    except KeyError:
        exit("Invalid username or token\n")

    return parsed_user_info


def get_repos_data(repo_url: str, token: str = "", no_forks: bool = False,
                   repo_url_query: str = ""):
    """
        A function to get the repo data\n
        args:\n
            \trepo_url - URL for the users repo list\n
            \ttoken - personal access token\n
            \tno_forks - boolean that determines whether or not we keep forks\n
            \trepo_url_query - URL query string that determines if we get pub/priv/both repos
    """

    get_repos_info = get(
        repo_url + "?{parameters}".format(parameters=repo_url_query),
        headers={
            "Accept": "application/vnd.github.v3+json"
        },
        auth=(token, "x-oauth-basic")
    ).json()

    parsed_repos = list()

    # loop through the repos
    for repo in get_repos_info:
        # check if the no-forks option is passed and if the repo is a fork
        if no_forks is True and repo["fork"] is True:
            continue
        else:
            # add the repo data we need to a list (for outputting as a table)
            parsed_repos.append({
                "name": repo["name"],
                "url": repo["html_url"],
                "stars": repo["stargazers_count"]
            })

    return parsed_repos


def my_profile_function(args: dict):
    """
        A function that handles the my-profile command\n
        args:\n
            \targs - the commandline arguments
    """

    token = args["token"]
    private = args["private"]
    public = args["public"]

    # Check if the private or public option is passed
    # and then set up the visibility query accordingly
    if private is True:
        visibility_param = "visibility=private"
    elif public is True:
        visibility_param = "visibility=public"
    else:
        visibility_param = "visibility=all"

    my_profile_data = get_profile_data(
        profile_url="https://api.github.com/user",
        token=token
    )
    my_profile_repo_data = get_repos_data(
        repo_url="https://api.github.com/user/repos",
        repo_url_query=visibility_param,
        no_forks=args["no_forks"],
        token=token
    )

    format_output(my_profile_data, my_profile_repo_data)


def profile_function(args: dict):
    """
        A function that handles the profile command\n
        args:\n
            \targs - the commandline arguments
    """

    username = args["username"]

    profile_data = get_profile_data(
        profile_url="https://api.github.com/users/{username}".format(
            username=username)
    )
    profile_repo_data = get_repos_data(
        repo_url=profile_data["repos_url"],
        no_forks=args["no_forks"]
    )

    format_output(profile_data, profile_repo_data)


def format_output(user_data: dict, repo_data: list):
    """
        A function that formats the data for the the output:\n
            \tusername: full name - location\n
            \t{table of repos}\n
        \n
        args:\n
            \tuser_data - parsed user information\n
            \trepo_data - parsed repo information\n
    """

    print(
        user_data["username"] + ":",
        user_data["name"], "-", user_data["location"]
    )

    # Check if there is any repo data
    try:
        table_header = repo_data[0].keys()
        table_rows = [row.values() for row in repo_data]
        print(tabulate(table_rows, table_header), "\n")
    # If there is no data exit with a message
    except IndexError:
        exit("No repo data found!\n")


def main(argv: Optional[Sequence[str]] = None) -> int:
    # Initiate the cl arguments parser and subparsers
    arg_parser = argparse.ArgumentParser(
        description="A CLI to get GitHub user & repo information.")
    subparsers = arg_parser.add_subparsers(
        dest="command", title="Commands", required=True)

    # Arguments for the my-profile command
    my_profile_parser = subparsers.add_parser(
        "my-profile", help="display information about the current user's profile")
    my_profile_parser.add_argument(
        "--token", help="GitHub personal access token", action="store")
    my_profile_parser.add_argument(
        "--no-forks", help="do not show forks", action="store_true")
    my_profile_parser.add_argument(
        "--private", help="show private repositories only", action="store_true")
    my_profile_parser.add_argument(
        "--public", help="show public repositories only", action="store_true")

    # Arguments for the profile command
    profile_parser = subparsers.add_parser(
        "profile", help="display information about a github user's profile")
    profile_parser.add_argument(
        "username", help="the username of the profile", action="store")
    profile_parser.add_argument(
        "--no-forks", help="do not show forks", action="store_true")

    args = arg_parser.parse_args(argv)

    # Check which command was passed
    if vars(args)["command"] == "my-profile":
        # If no token was passed check the config file
        if vars(args)["token"] is None:
            with open("github_config.json") as config_file:
                token = load(config_file)["public_access_token"]
                if len(token) <= 0:
                    # If no token is given in the config file raise an error
                    raise argparse.ArgumentTypeError(
                        "No token given, use --token or add a token to the config file.")
                else:
                    vars(args)["token"] = token

        my_profile_function(vars(args))
    else:
        profile_function(vars(args))

    return 0


if __name__ == "__main__":
    exit(main())