import requests
import pandas as pd

# Fetch details of a repository
def get_repository(owner, repo,key):
    headers = {'Authorization': f'token {key}'}

    url = f'https://api.github.com/repos/{owner}/{repo}'
    response = requests.get(url,headers=headers)
    print(response.json())
    print("Fetched repository details....")
    return response.json()

# Fetch total repositories of an organization
def get_organization(organization,key,per_page=100):
    repos = []
    page = 1
    headers = {'Authorization': f'token {key}'}
    
    while True:
        url = f'https://api.github.com/users/{organization}/repos'
        params = {'page': page, 'per_page': per_page}
        response = requests.get(url, headers=headers, params=params)
        data = response.json()
        if not data:
            break
        repos.extend(data)
        page += 1
        print(response.json())
    print("Fetched all repositories details of an organization....")
    return repos

# Fetch total no of contributors
def get_contributors(owner, repo,key,per_page=100):
    contributors = []
    page = 1
    headers = {'Authorization': f'token {key}'}
    
    while True:
        url = f'https://api.github.com/repos/{owner}/{repo}/contributors'
        params = {'page': page, 'per_page': per_page}
        response = requests.get(url, headers=headers, params=params)
        data = response.json()
        if not data:
            break
        contributors.extend(data)
        page += 1
        print(response.json())
    print("Fetched total no of contributers....")
    return contributors

# Fetch created issues by a contributor
def get_created_issues_for_each(owner, repo,contributor,key,per_page=100):
    issues = []
    page = 1
    headers = {'Authorization': f'token {key}'}

    while True:
        url = f'https://api.github.com/repos/{owner}/{repo}/issues'
        params = {'page': page, 'per_page': per_page,'creator': contributor,'state': 'open'}
        response = requests.get(url, headers=headers, params=params)
        data = response.json()
        if not data:
            break
        issues.extend(data)
        page += 1
        print(response.json())
    print("Fetched repository details....")
    return issues

# Fetch closed issues by a contributor
def get_closed_issues_for_each(owner, repo,contributor,key,per_page=100):
    issues = []
    page = 1
    headers = {'Authorization': f'token {key}'}
    
    while True:
        url = f'https://api.github.com/repos/{owner}/{repo}/issues'
        params = {'page': page, 'per_page': per_page,'creator': contributor,'state': 'closed'}
        response = requests.get(url, headers=headers, params=params)
        data = response.json()
        if not data:
            break
        issues.extend(data)
        page += 1
        print(response.json())
    print("Fetched closed issues....")
    return issues

def get_commits(owner, repo,key,per_page=100):
    commits = []
    page = 1
    headers = {'Authorization': f'token {key}'}
    
    while True:
        url = f'https://api.github.com/repos/{owner}/{repo}/commits'
        params = {'page': page, 'per_page': per_page}
        response = requests.get(url, headers=headers, params=params)
        data = response.json()
        if not data:
            break
        commits.extend(data)
        page += 1
        print(response.json())
    print("Fetched total commits....")
    return commits

from collections import defaultdict
def count_commits_by_user(commits):
    commit_counts = defaultdict(int)
    
    for commit in commits:
        author = commit['commit']['author']['name']
        commit_counts[author] += 1
    
    return dict(commit_counts)

def create_commits_dataframe(commit_counts):
    df_commits = pd.DataFrame(list(commit_counts.items()), columns=['Contributor Name', 'Total Commits'])
    return df_commits


# Comments made by a contributor under an issue
def get_issue_comments_for_each(owner,repo,contributor,key):
    headers = {'Authorization': f'token {key}'}
    url = f'https://api.github.com/repos/{owner}/{repo}/issues/comments'
    data = requests.get(url, headers=headers)
    comments=data.json()
    total_comments=0
    
    for each in comments:
        if each['user']['login']==contributor:
            total_comments+=1
    print(total_comments)
    print("Fetched issue comments for each user....")
    return total_comments

# Comments made by a contributor under a PR
def get_pull_request_comments_for_each(owner,repo,contributor,key):
    headers = {'Authorization': f'token {key}'}
    url = f'https://api.github.com/repos/{owner}/{repo}/pulls/comments'
    data = requests.get(url, headers=headers)
    comments=data.json()
    total_comments=0
    
    for each in comments:
        if each['user']['login']==contributor:
            total_comments+=1
    print(total_comments)
    print("Fetched pull requests for each user....")
    return total_comments

# Reviews made by each contributor
def get_reviews_for_each(owner, repo, contributor,key):
    url = f'https://api.github.com/repos/{owner}/{repo}/pulls'
    headers = {'Authorization': f'token {key}'}
    response = requests.get(url, headers=headers)
    pulls = response.json()

    review_count = 0
    for pull in pulls:
        pull_number = pull['number']
        reviews_url = f'https://api.github.com/repos/{owner}/{repo}/pulls/{pull_number}/reviews'
        reviews_response = requests.get(reviews_url, headers=headers)
        reviews = reviews_response.json()

        for review in reviews:
            if review['user']['login'] == contributor:
                review_count += 1
    print(review_count)
    print("Fetched reviews for each user....")
    return review_count

from datetime import datetime

def get_response_times_for_contributor(owner, repo,contributor,key):
    url = f'https://api.github.com/repos/{owner}/{repo}/pulls'
    headers = {'Authorization': f'token {key}'}
    response = requests.get(url, headers=headers)
    pulls = response.json()

    response_times = []
    for pull in pulls:
        pull_number = pull['number']
        reviews_url = f'https://api.github.com/repos/{owner}/{repo}/pulls/{pull_number}/reviews'
        reviews_response = requests.get(reviews_url, headers=headers)
        reviews = reviews_response.json()

        for review in reviews:
            if review['user']['login'] == contributor:
                review_created_at = datetime.strptime(review['created_at'], '%Y-%m-%dT%H:%M:%SZ')
                pull_created_at = datetime.strptime(pull['created_at'], '%Y-%m-%dT%H:%M:%SZ')
                response_time = (review_created_at - pull_created_at).total_seconds()
                response_times.append(response_time)

    return response_times

# PRS created by a contributor
def get_created_prs_for_each(org, repo,contributor, key):
    total_prs_created = 0
    
    url = f'https://api.github.com/repos/{org}/{repo}/pulls?state=open'
    headers = {'Authorization': f'token {key}'}
    response = requests.get(url, headers=headers)
    prs = response.json()
    
    for pr in prs:
        if pr['user']['login'] == contributor:
            total_prs_created+=1
    
    return total_prs_created

# PRs merged by a contributor
def get_merged_prs_for_each(org, repo,contributor, key):
    total_prs_merged = 0
    
    url = f'https://api.github.com/repos/{org}/{repo}/pulls?state=closed'
    headers = {'Authorization': f'token {key}'}
    response = requests.get(url, headers=headers)
    prs = response.json()
    
    for pr in prs:
        if pr['merged_at'] is not None:
            reviews_url = f'https://api.github.com/repos/{org}/{repo}/pulls/{pr["number"]}/reviews'
            reviews_response = requests.get(reviews_url, headers=headers)
            reviews = reviews_response.json()
            
            for review in reviews:
                if review['user']['login'] == contributor:
                    total_prs_merged += 1
                    break
    
    return total_prs_merged

def get_dataframe_from_organization(organization,key):
    columns = ['Contributor Name','Contributions','Total PRs Created','Total PRs Merged','Total Issues Created','Total Issues Closed','Total PR Comments','Total Issues Comments']
    df = pd.DataFrame(columns=columns)
    contributors_set = set()
    repos=get_organization(organization,key)
    merged_df=pd.DataFrame()
    
    for each_repo in repos:
        name=each_repo['name']
        contributors=get_contributors(organization,name,key)
        for each_contributor in contributors:
            contributor_name=each_contributor['login']
            if contributor_name in contributors_set:
                contributions=each_contributor['contributions']
                closed_issues=get_closed_issues_for_each(organization,name,contributor_name,key)
                created_issues=get_created_issues_for_each(organization,name,contributor_name,key)
                created_prs=get_created_prs_for_each(organization,name,contributor_name,key)
                merged_prs=get_merged_prs_for_each(organization,name,contributor_name,key)
                issue_comments=get_issue_comments_for_each(organization,name,contributor_name,key)
                pulls_comments=get_pull_request_comments_for_each(organization,name,contributor_name,key)
                commits=get_commits(organization,name,key)
                commit_counts = count_commits_by_user(commits)
                df_commits = create_commits_dataframe(commit_counts)
                
                df.loc[df['Contributor Name'] == contributor_name, 'Contributions'] += int(contributions)
                df.loc[df['Contributor Name'] == contributor_name, 'Total PR Commits'] += len(closed_issues)
                df.loc[df['Contributor Name'] == contributor_name, 'Total Issue Commits'] += len(created_issues)
                df.loc[df['Contributor Name'] == contributor_name, 'Total Issues Closed'] += len(closed_issues)
                df.loc[df['Contributor Name'] == contributor_name, 'Total Issues Created'] += len(created_issues)
                df.loc[df['Contributor Name'] == contributor_name, 'Total PRs Created'] += created_prs
                df.loc[df['Contributor Name'] == contributor_name, 'Total PRs Merged'] += merged_prs
                df.loc[df['Contributor Name'] == contributor_name, 'Total PR Comments'] += pulls_comments
                df.loc[df['Contributor Name'] == contributor_name, 'Total Issues Comments'] += issue_comments


                merged_df = pd.merge(df, df_commits, on='Contributor Name', how='left')
                continue

            contributions=each_contributor['contributions']
            closed_issues=get_closed_issues_for_each(organization,name,contributor_name,key)
            created_issues=get_created_issues_for_each(organization,name,contributor_name,key)
            created_prs=get_created_prs_for_each(organization,name,contributor_name,key)
            merged_prs=get_merged_prs_for_each(organization,name,contributor_name,key)
            issue_comments=get_issue_comments_for_each(organization,name,contributor_name,key)
            pulls_comments=get_pull_request_comments_for_each(organization,name,contributor_name,key)
            commits=get_commits(organization,name,key)
            commit_counts = count_commits_by_user(commits)
            df_commits = create_commits_dataframe(commit_counts)
            
            new_row={
                    'Contributor Name': contributor_name,
                    'Contributions': int(contributions),
                    'Total Issues Closed' : len(closed_issues),
                    'Total Issues Created' : len(created_issues),
                    'Total PRs Created': created_prs,
                    'Total PRs Merged': merged_prs,
                    'Total PR Comments': pulls_comments,
                    'Total Issues Comments': issue_comments
            }
            
            new_row_df = pd.DataFrame([new_row], columns=df.columns)
            df = pd.concat([df, new_row_df], ignore_index=True)
            
            merged_df = pd.merge(df, df_commits, on='Contributor Name', how='left')

    
    return merged_df

# Using Repository
def get_dataframe_from_repository(organization,repo,key):
    columns = ['Contributor Name','Contributions','Total PRs Created','Total PRs Merged','Total Issues Created','Total Issues Closed','Total PR Comments','Total Issues Comments']
    df = pd.DataFrame(columns=columns)
    contributors_set = set()
    details=get_repository(organization,repo,key)
    name=details['name']
    merged_df=pd.DataFrame()
    
    contributors=get_contributors(organization,name,key)
    for each_contributor in contributors:
        contributor_name=each_contributor['login']
        if contributor_name in contributors_set:
            contributions=each_contributor['contributions']
            closed_issues=get_closed_issues_for_each(organization,name,contributor_name,key)
            created_issues=get_created_issues_for_each(organization,name,contributor_name,key)
            created_prs=get_created_prs_for_each(organization,name,contributor_name,key)
            merged_prs=get_merged_prs_for_each(organization,name,contributor_name,key)
            issue_comments=get_issue_comments_for_each(organization,name,contributor_name,key)
            pulls_comments=get_pull_request_comments_for_each(organization,name,contributor_name,key)
            commits=get_commits(organization,name,key)
            commit_counts = count_commits_by_user(commits)
            df_commits = create_commits_dataframe(commit_counts)
            
            df.loc[df['Contributor Name'] == contributor_name, 'Contributions'] += int(contributions)
            df.loc[df['Contributor Name'] == contributor_name, 'Total PR Commits'] += len(closed_issues)
            df.loc[df['Contributor Name'] == contributor_name, 'Total Issue Commits'] += len(created_issues)
            df.loc[df['Contributor Name'] == contributor_name, 'Total Issues Closed'] += len(closed_issues)
            df.loc[df['Contributor Name'] == contributor_name, 'Total Issues Created'] += len(created_issues)
            df.loc[df['Contributor Name'] == contributor_name, 'Total PRs Created'] += created_prs
            df.loc[df['Contributor Name'] == contributor_name, 'Total PRs Merged'] += merged_prs
            df.loc[df['Contributor Name'] == contributor_name, 'Total PR Comments'] += pulls_comments
            df.loc[df['Contributor Name'] == contributor_name, 'Total Issues Comments'] += issue_comments
            
            merged_df = pd.merge(df, df_commits, on='Contributor Name', how='left')

            continue

        contributions=each_contributor['contributions']
        closed_issues=get_closed_issues_for_each(organization,name,contributor_name,key)
        created_issues=get_created_issues_for_each(organization,name,contributor_name,key)
        created_prs=get_created_prs_for_each(organization,name,contributor_name,key)
        merged_prs=get_merged_prs_for_each(organization,name,contributor_name,key)
        issue_comments=get_issue_comments_for_each(organization,name,contributor_name,key)
        pulls_comments=get_pull_request_comments_for_each(organization,name,contributor_name,key)
        commits=get_commits(organization,name,key)
        commit_counts = count_commits_by_user(commits)
        df_commits = create_commits_dataframe(commit_counts)
                
        new_row={
                'Contributor Name': contributor_name,
                'Contributions': int(contributions),
                'Total Issues Closed' : len(closed_issues),
                'Total Issues Created' : len(created_issues),
                'Total PRs Created': created_prs,
                'Total PRs Merged': merged_prs,
                'Total PR Comments': pulls_comments,
                'Total Issues Comments': issue_comments
        }
        
        new_row_df = pd.DataFrame([new_row], columns=df.columns)
        df = pd.concat([df, new_row_df], ignore_index=True)
        
        merged_df = pd.merge(df, df_commits, on='Contributor Name', how='left')

    
    return merged_df