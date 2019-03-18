import pandas as pd
from pandas.io.json import json_normalize
import json


class JiraDataFrameConstructor:
    """Build JIRA issue Dataframe, piece by piece."""

    @classmethod
    def construct_dataframe_for_upload(cls, issue_list_chunk):
        """Make DataFrame out of data received from JIRA API."""
        issue_list = [cls.make_issue_body(issue) for issue in issue_list_chunk]
        issue_json_list = [cls.dict_to_json_string(issue) for issue in issue_list]
        issues_df = json_normalize(issue_json_list)
        complete_df = cls.add_epic_metadata(issues_df)
        return complete_df

    @staticmethod
    def dict_to_json_string(issue_dict):
        """Converts dict to JSON to string."""
        issue_json_string = json.dumps(issue_dict)
        issue_json = json.loads(issue_json_string)
        return issue_json

    @staticmethod
    def add_epic_metadata(issues_df):
        """Perform a merge to add additional metadata."""
        epic_df = pd.read_csv('../data/epics.csv')
        final_df = pd.merge(issues_df, epic_df, how='left', on=['epic_link'])
        return final_df

    @staticmethod
    def make_issue_body(issue):
        """Create a JSON body for each ticket."""
        body = {
            'key': issue['key'],
            'assignee': issue['fields']['assignee']['displayName'],
            'assignee_url': issue['fields']['assignee']['avatarUrls']['48x48'],
            'summary': issue['fields']['summary'],
            'status': issue['fields']['status']['name'],
            'priority': issue['fields']['priority']['name'],
            'priority_url': issue['fields']['priority']['iconUrl'],
            'priority_rank': issue['fields']['priority']['id'],
            'issuetype': issue['fields']['issuetype']['name'],
            'issuetype_icon': issue['fields']['issuetype']['iconUrl'],
            'epic_link': issue['fields']['customfield_10008'],
            'project': issue['fields']['project']['name'],
            'updated': issue['fields']['updated']
        }
        return body