# devops_metrics
This repo is an attempt to capture devops metrics like lead time, deployment metric, mean time to recovery etc.



PullRequest will have source and target branch , multiple commits and multiple participants

merge_commit_sha  column from pull_request  will be commit_id in build_details table when merged branch is deployed



![Alt text](db_schema.png?raw=true "Title")


### Setup details 

##### If you want to deploy on AWS lambda and api gateway 

Setup your config in config.py or set it in envoirnment variable

```DB_URL - connection string to database(eg:sqlite:///metrics.db)```

if you are using bitbucket set  ```BITBUCKET_CLIENT_ID  and BITBUCKET_SECRET_KEY ``` in config

if you are using github  set ```GITHUB_ACCESS_TOKEN ```


Setup your database tables

```alembic upgrade head ```

Setup your access key and secret key using ```aws configure```

Install severless  https://serverless.com/framework/docs/providers/aws/guide/installation/


Run ```serverless deploy``` to deploy 



##### If you want torun it as docker container 

```docker build . -t devops_metrics:latest```

Run in docker container 

```
docker run -d  -p 5000:5000 \
-e DB_URL='' \
-e BITBUCKET_CLIENT_ID='' \
-e BITBUCKET_SECRET_KEY='' \
-e GITHUB_ACCESS_TOKEN='' \
devops_metrics:latest
```

After deployment add the below  urls as a webhook for all the pull_request_event
```
host:port/pull_request/bitbucket for bitbucket
host:port/pull_request/github for github
```

##### Details of APIs to push data


```
<host>:port/issue  to post issue data
{ 
   'issue_id':'abc',
   'start_time':'2019-05-15T15:20:30Z',
   'end_time':'2019-05-15T15:20:30Z',
   'title':'title',
   'description':'desc',
   'sev':'high',
   'reported_by':'xyz'
}
```
```
host:port/build_detail  to post deployment build detail data
{ 
   'build_id':'123',
   'project_name':'xyz_service',
   'source_type':'github',
   'source_location':'github.com/url',
   'branch_name':'master',
   'commit_id':'ahskjdhsdadfasd',
   'start_time':'2019-05-15T15:20:30Z',
   'end_time':'2019-05-15T15:20:30Z',
   'status':'SUCCESS'
}
```



##### How to get access token and add webhook for github?
https://developer.github.com/webhooks/creating/#setting-up-a-webhook

https://help.github.com/en/github/authenticating-to-github/creating-a-personal-access-token-for-the-command-line


##### How to get client id and secrete key   and add webhook for bitbucket?
https://confluence.atlassian.com/bitbucket/manage-webhooks-735643732.html

https://vssue.js.org/guide/bitbucket.html



Coming soon queries to measure and compare all the metrics

#### Work in progress.....