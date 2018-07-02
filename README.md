# Wikipedia Clickstream Fun Facts

## Project Overview
Clickstream data is very common for most companies if they have their own websites. The motivation for building such a platform is to help companies become easy to query the information they want. For example, we can choose “pagerank” and give the year, month and the number of records, the platform will return the bar chart. The “traffic source” and “traffic to” means where the click comes from or where the click goes to. Finally, if we choose “the most popular path”, we could know the most popular path in the certain month.



## Data Source
I use the Wikipedia Clickstream dataset. The data can be downloaded from this [link](https://figshare.com/articles/Wikipedia_Clickstream). 

## Raw Data 
The raw data has two formats:

| prev_id    | curr_id    | n    | prev_title                | curr_title |type  |
| ----------:|-----------:|-----:|--------------------------:|-----------:|------|
| 489033     | 331586     | 59   | Academy_Awards_ceremonies |"Crocodile" |link  |

Or:

| prev          | curr          | type                |n              | 
| ------------- |--------------:| -------------------:|--------------:|
| Adema         | Edema         | link                |60             |

We will use spark calculation to make the raw data looks like this:

| prev_title    | curr_title    | n        |date       | 
| ------------- |--------------:| --------:|----------:|
| Adema         | Edema         | 60       |2016-04    |

And also map reduce results for page rank:

| curr_title    | date        |score      | 
|--------------:| -----------:|----------:|
| Peter_Morice  | 2016-03     |35         |


## Data Pipeline
The following picture shows data pipeline for the platform. Firstly, we store the clickstream data from Wikipedia clickstream dataset into S3 buckets. Then use Spark calculation to send the data to the RDS (MySQL). We use spark to do batch processing. Finally use Tornado to visualize it.

![datapipeline](/image/datapipeline.png?raw=true "datapipeline")

## Usage Instruction
This code was run on Amazon AWS servers.

### Install
This project needs Hadoop, Spark, RDS. You can install and configure them according to the official tutorials, or you can use [pegasus](https://github.com/InsightDataScience/pegasus).

### Doing Spark Calculation and putting data into RDS
Download the data to S3 buckets from Wikipedia clickstream dataset and then run:
`$ spark-submit –-master spark://XX.XXX.XX.XXX:XXXX --executor-memory 6G --executor-cores 2 --packages mysql:mysql-connector-java:5.1.38 jdbcsql.py`

### Start Website
`$ python3 wiki.py&`

## Demo
The presentation is available [here](https://drive.google.com/open?id=1PAQzwA9bfwPtiPSksmvw8YSilt3KRuQv)
<br>
The video for demo is available [here](https://youtu.be/)




