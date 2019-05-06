# Report Generator

Report Generator is a simple Python2 script to produce text reports about a
news database.

This script was created as part of the FullStack nanodegree in Udacity.

This script is an exercise to learn SQL. Please, do not try to use it in
production and be very careful if using parts of it in a production code.
Keep in mind that it was written by a student who was trying to learn this
skills.

## Installation

This script uses Python2 with psycopg2

```bash
pip install psycopg2
```

It asumes there is a local installation of PostgreSQL server with a database
named "news" with the structure and data provided in this link; 
https://d17h27t6h515a5.cloudfront.net/topher/2016/August/57b5f748_newsdata/newsdata.zip

## Usage

To execute the program, open a terminal, navigate to the directory containing
the program and run:

```bash
python main.py
```

### Storing results

To store a report, redirect it to a file.

```bash
python main.py > report.txt
```


## Example output

```
==== TOP 3 MOST READ ARTICLES ====

---------------------------------------------------------------------------------------------------------
| title                                              count                                              |
---------------------------------------------------------------------------------------------------------
| Candidate is jerk, alleges rival                   338647                                             |
| Bears love berries, alleges bear                   253801                                             |
| Bad things gone, say good people                   170098                                             |
---------------------------------------------------------------------------------------------------------



==== TOP 10 MOST READ AUTHORS ====

---------------------------------------------------------------------------------------------------------
| name                                               views                                              |
---------------------------------------------------------------------------------------------------------
| Ursula La Multa                                    507594                                             |
| Rudolf von Treppenwitz                             423457                                             |
| Anonymous Contributor                              170098                                             |
| Markoff Chaney                                     84557                                              |
---------------------------------------------------------------------------------------------------------



==== TOP ERRORS PER DAY ====

-----------------------------------------------------------------------------------------
| day                  total                errors               percent              |
-----------------------------------------------------------------------------------------
| 2016-07-17           55907                1265                 2.26                 |
-----------------------------------------------------------------------------------------
```
