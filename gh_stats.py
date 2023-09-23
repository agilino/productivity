import subprocess
import json
import sys


def github_kpis():
    """
      This function will return for each developer Key Performance Indicators (KPIs),
      such as lines added, deleted, PR comment count, accepted and deleted for a given GitHub project.

      While KPIs are old school, they should be combined with Objectives and Key Results (OKRs),
      e.g., number of features deployed and number of bugs reported on production,
      to provide a more holistic view of the project.

      You need to install the GitHub CLI (gh) to run this script.
      Please refer to https://github.com/cli/cli#installation for instructions.
    """
    if len(sys.argv) < 3:
        print(
            "Usage: python get_comment_counts.py <project-name> <excluded_users> [date]")
        sys.exit(1)

    # Get project name from the command line argument
    project_name = sys.argv[1]
    excluded_users = sys.argv[2].split(",")

    # Calculate the default date from 3rd console argument (30 days ago) if not provided
    create_date_from = get_date_limit(3, 30)
    merged_date_until = get_date_limit(4, 0)

    # Fetch pull requests created after the specified date using gh cli
    gh_command = 'gh pr list -R "{project_name}" -s all -S "created:>{create_date_from} merged:<={merged_date_until}" -L 10000 --json=number,author,reviews,comments,additions,deletions,state'.format(
        project_name=project_name, create_date_from=create_date_from, merged_date_until=merged_date_until)
    pr_list_output = subprocess.check_output(gh_command, shell=True)

    # Parse the JSON output
    pr_list = json.loads(pr_list_output)

    # Initialize a dictionary to store comment counts for each user
    user_stats = {}

    for pr in pr_list:
        # only count merged PRs
        if pr["state"] != "MERGED":
            continue
        # count the number of lines added and deleted
        process_loc(excluded_users, user_stats, pr)

        reviews = pr["reviews"]
        # Iterate through comments and reviews and update user comment counts
        process_reviews(excluded_users, user_stats, reviews)

        comments = pr["comments"]
        # Iterate through comments and reviews and update user comment counts
        process_comments(excluded_users, user_stats, comments)

    # Display comment counts for each user
    formatted_output = json.dumps(user_stats, indent=4, sort_keys=True)
    print(formatted_output)


def process_loc(excluded_users, user_stats, pr):
    """Process lines of code added and deleted for the author"""
    user_login = pr["author"]["login"]
    if user_login not in excluded_users:
        if user_login not in user_stats:
            user_stats[user_login] = {}
        if "loc" not in user_stats[user_login]:
            user_stats[user_login]["loc"] = {}
        user_stats[user_login]["loc"]["added"] = user_stats[user_login]["loc"].get(
            "added", 0) + pr["additions"]
        user_stats[user_login]["loc"]["deleted"] = user_stats[user_login]["loc"].get(
            "deleted", 0) + pr["deletions"]


def get_date_limit(input_arg, default_offset):
    """ Get create date from user input or use default"""
    if len(sys.argv) <= input_arg:
        from datetime import datetime, timedelta
        default_date = datetime.now() - timedelta(days=default_offset)
        create_date = default_date.strftime("%Y-%m-%d")
    else:
        create_date = sys.argv[input_arg]
    return create_date


def process_comments(excluded_users, user_stats, comments):
    """Iterate through comments and update user comment counts"""
    for item in comments:
        user_login = item["author"]["login"]
        if user_login in excluded_users:
            continue  # Skip excluded users
        if user_login not in user_stats:
            user_stats[user_login] = {}
        user_stats[user_login]["comments"] = user_stats[user_login].get(
            "comments", 0) + 1


def process_reviews(excluded_users, user_stats, reviews):
    """Iterate through reviews and update user comment counts"""
    for item in reviews:
        user_login = item["author"]["login"]
        state = item["state"]
        if user_login in excluded_users:
            continue  # Skip excluded users
        if user_login not in user_stats:
            user_stats[user_login] = {}
        if state == "COMMENTED":
            user_stats[user_login]["comments"] = user_stats[user_login].get(
                "comments", 0) + 1
        if state == "CHANGES_REQUESTED":
            user_stats[user_login]["changes_requested"] = user_stats[user_login].get(
                "changes_requested", 0) + 1
        if state == "APPROVED":
            user_stats[user_login]["approved"] = user_stats[user_login].get(
                "approved", 0) + 1
        if state == "DISMISSED":
            user_stats[user_login]["dismissed"] = user_stats[user_login].get(
                "dismissed", 0) + 1


if __name__ == "__main__":
    github_kpis()
