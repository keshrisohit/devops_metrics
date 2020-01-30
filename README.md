# devops_metrics
This repo is an attempt to capture devops metrics like lead time, deployment metric, mean time to recovery etc.



PullRequest will have source and target branch , multiple commits and multiple participants

merge_commit_sha  column from pull_request  will be commit_id in build_details table when merged branch is deployed


![Alt text](db_schema.png?raw=true "Title")


### Setup details 

##### If you want to deploy on AWS lambda and api gateway 

Setup your config in config.py or set it in envoirnment variable


```DB_URL - connection string to database(eg:sqlite:///metrics.db)```


if you are using bitbucket set  
```BITBUCKET_CLIENT_ID  and BITBUCKET_SECRET_KEY ``` i

if you are using github  set 
```GITHUB_ACCESS_TOKEN ```


Setup your database tables
Go to project root directory and run 


```PYTHONPATH=./ alembic upgrade head```



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

#### Build details data
lambda with name code_build_metrics will get deployed which can subscribe to ```aws code build``` event and persist build details if use aws code build


##### How to get access token and add webhook for github?
https://developer.github.com/webhooks/creating/#setting-up-a-webhook

https://help.github.com/en/github/authenticating-to-github/creating-a-personal-access-token-for-the-command-line


##### How to get client id and secrete key   and add webhook for bitbucket?
https://confluence.atlassian.com/bitbucket/manage-webhooks-735643732.html

https://vssue.js.org/guide/bitbucket.html




Coming soon queries to measure and compare all the metrics


All the queries will pull data for last 30 days

Get Lead Time

Get all commits for merged pull_request, where target branch is master.
Build details deployment commit id should be same as merge_commit_sha in pull_request
average of difference between commit time and build_details end_time is you lead time as commit is deployed in production
````
select pr.repository_url as repository ,week(pr.merged_at) as week ,avg(timestampdiff(minute,c.time,bd.end_time)) as lead_time
from pull_request pr , 
build_details bd ,
commit c , 
branch b,
pull_request_commit_association prc,
pull_request_branch_association prb
where pr.action ='MERGED'
and prb.branch_id=b.id
and prb.branch_type='TARGET'
and b.name='master'
and bd.commit_id = pr.merge_commit_sha
and c.id =prc.commit_id
and pr.id=prc.pull_request_id

group by pr.merged_at,pr.repository_url
````



Lets say you dont have build details and if you depploy your code after merge to master, we can get approx lead time assuming PR merged_at as deployemnt time 

```
 select pr.repository_url,week(pr.merged_at),avg(timestampdiff(minute,c.time,pr.merged_at))as lead_time 
 from pull_request_commit_association prc, 
`commit` c,
 branch b,
 pull_request pr,
 pull_request_branch_association prb 
 where prc.commit_id=c.id
 and pr.id=prc.pull_request_id 
 and prb.pull_request_id=pr.id  
 and prb.branch_id=b.id  
 and action ='MERGED' 
 and prb.branch_type='TARGET' 
 and b.name='master' group by week(pr.merged_at),pr.repository_url
 and pr.merged_at > NOW() - INTERVAL 30 DAY
```

Deployment frequency if you have build_deatils
```
select bd.project_name as service ,count(*) as deployment_frequency ,week(bd.start_time)  
from build_details  bd
where bd.end_time > NOW() - INTERVAL 30 DAY
group by week(bd.start_time),bd.project_name;
```

Deployemnt frequency if you consider merege to master as deployemnt

```
select count(*) deployment_frequency,week(pr.merged_at), pr.repository_url as repository_url from 
pull_request pr, 
pull_request_branch_association prb  ,
branch b
where
prb.branch_id=b.id
and  pr.action='MERGED'
and prb.branch_type='TARGET'
and b.name='master'
and pr.merged_at > NOW() - INTERVAL 30 DAY
group by week(pr.merged_at),pr.repository_url
```

Mean Time to Recover
Select sev types which means service unavailable /un usable
```

select avg(timestampdiff(minute,start_time,end_time)) mttr from issues 
where sev=''

```
No of review comments.
```
select  pr.repository_url,week(pr.merged_at) ,coalesce(sum(pr.no_of_review_comments),0)+coalesce(sum(pr.no_of_comments),0) as comments  
from pull_request pr 
where action='MERGED' 
and pr.merged_at > NOW() - INTERVAL 30 DAY
group by week(pr.merged_at) ,pr.repository_url
```

No of lines changed per repository 
```
select  pr.repository_url,week(pr.merged_at) ,COALESCE(SUM(pr.lines_added),0)+COALESCE(SUM(pr.lines_removed),0)
from pull_request pr 
where action ='MERGED'
and pr.merged_at > NOW() - INTERVAL 30 DAY
group by week(pr.merged_at) ,pr.repository_url

```

NO fo commits per repositroy

```
select count(*), week(c.time),repository_url 
from commit c 
where c.time > NOW() - INTERVAL 30 DAY
group by repository_url ,week(c.time);

```

Deployment Time per repository

```
select project_name,avg(TIMESTAMPDIFF(second,start_time,end_time)) as deployment_time ,week(start_time)   
from build_details 
where start_time > NOW() - INTERVAL 30 DAY
group by week(start_time),project_name;

```
Sample dashboard



#### Work in progress.....

![Alt text](sample_dashboard.png?raw=true "Title")