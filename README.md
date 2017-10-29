# Log Analysis
In this project, I use SQL database skill to query information from a live database and use python to display into a file.
I analyze the most popular authors and articles in this newspaper site. I also figure out which date has the most error rate
of requesting from the website.

## Install
1. This program is only compatiable for **python 3**
2. You can visit the website [here](https://www.python.org/downloads/release/python-352/) to download python3
3. Please make sure you have [vagrant](https://www.vagrantup.com/downloads.html) and 
[VirtualBox](https://www.virtualbox.org/wiki/Download_Old_Builds_5_1).

## Create views
In order to query data properly, you have to create several views in the database.
```
	create view all_requests as select date(time) as date, count(date(time)) as all_num from log group by date;
```
```
	create view error_requests as select status, date(time) as date, count(*)
as error_num from log where status != '200 OK' group by status, date;
```
```
	create view pct as select error_requests.date, error_requests.error_num, 
	all_requests.all_num,all_requests.date as date_all from error_requests 
	join all_requests on error_requests.date = all_requests.date;
```
```
	create view percentage as select date,  round (100.0 * error_num / all_num, 2) 
	as pct_error,date_all, error_num, all_num from pct where date = date_all;
```
```
	create view page_views as select articles.title, count(logptitle.path) as
views from articles join (select concat(replace(substring(path, 10, length(path)), '-', ' '), '%') 
as ptitle, path from log) as logptitle on replace(articles.title, '''', '') 
ilike logptitle.ptitle where length(logptitle.path) > 10 
group by articles.title order by views desc;
```
```
	create view pop as select title, views, real.author from page_views, 
	(select authors.name as author, articles.title as realtitle from articles join authors
 on articles.author = authors.id) as real where real.realtitle = page_views.title;
```

## Instruction for running the program
1. make sure news.py is at the vagrant directory.
2. in the vagrant, **cd /vagrant**
3. once you into that file, you can type **python news.py** to run the program.
4. in the vagrant directory of your destop, it will pop out a **report.txt** file.
5. use **NOTEPAD ++** to open report.txt.
6. It will show you the log analysis.

## Attribution
1. Thanks for [Udacity](https://www.udacity.com/) to provide the huge database.
