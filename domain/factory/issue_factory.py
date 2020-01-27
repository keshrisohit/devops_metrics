from domain.entities import Issue


class IssueRequestFactory(object):

    def create_issue(self, payload):
        start_time = payload.get("start_time", "")
        end_time = payload.get("end_time", "")
        title = payload.get("title", "")
        description = payload.get("description", "")
        sev = payload.get("sev", "")
        reported_by = payload.get("reported_by", "")
        issue_id = payload.get("issue_id", "")

        issue = Issue(issue_id,start_time, end_time, title, description, sev, reported_by)

        return issue

