def feature_engineering(df):
    df.fillna(0, inplace=True)
    
    high_threshold = df['Contributions'].quantile(0.8)
    low_threshold = df['Contributions'].quantile(0.2)

    def categorize_contribution(contribution):
        if contribution >= high_threshold:
            return '2'
        elif contribution >= low_threshold:
            return '1'
        else:
            return '0'

    df['Contribution Type'] = df['Contributions'].apply(categorize_contribution)
    
    # New Features Construction
    df['Contribution Rate'] = df['Contributions'] / (df['Total PRs Created'] + 1)
    df['Issue Handling Efficiency'] = df['Total Issues Closed'] / (df['Total Issues Created'] + 1)
    df['PR Comments to Created Ratio'] = df['Total PR Comments'] / (df['Total PRs Created'] + 1)
    df['Issue Comments to Created Ratio'] = df['Total Issues Comments'] / (df['Total Issues Created'] + 1)
    df['Total Activity Score'] = df['Contributions'] + df['Total PRs Created'] + df['Total PRs Merged'] + df['Total Issues Created'] + df['Total Issues Closed'] + df['Total PR Comments'] + df['Total Issues Comments']
    df['PRs Impact Score'] = (df['Total PRs Created'] + df['Total PRs Merged']) * (df['Total PR Comments'] + 1)
    df['PRs Merged to Created Ratio'] = df['Total PRs Merged'] / (df['Total PRs Created'] + 1)
    df['Issues Closed to Created Ratio'] = df['Total Issues Closed'] / (df['Total Issues Created'] + 1)
    df['High Contributor'] = (df['Contributions'] > df['Contributions'].median()).astype(int)
    df['High PRs Created'] = (df['Total PRs Created'] > df['Total PRs Created'].median()).astype(int)
    df['Total Activity per Repository'] = df['Total PRs Created'] + df['Total Issues Created']
    
    df['Average Comments per PR'] = df['Total PR Comments'] / (df['Total PRs Created'] + 1)
    df['Contribution Impact Score'] = (df['Total PRs Merged'] * 0.5 + df['Total Issues Closed'] * 0.5) / (df['Contributions'] + 1)
    df['Collaboration Score'] = (df['Total PR Comments'] + df['Total Issues Comments']) / (df['Contributions'] + 1)
    df['Total Activity per Repository'] = df['Total Activity Score'] / (df['Contributions'] + 1)

    acceptance_threshold = 0.1
    df['PR_Acceptance'] = (df['Total PRs Merged'] / (df['Total PRs Created']+1) > acceptance_threshold).astype(int)
    df['PR_Acceptance'] = df.apply(lambda row: 0 if row['Total PRs Created'] == 0 else row['PR_Acceptance'], axis=1)
    
    return df
