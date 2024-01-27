http://testphp.vulnweb.com/artists.php?artist=1"
This URL has a SQL injection vulnerability. The payload "'" was added to the URL, resulting in an SQL injection error.
The vulnerable link detected is http://testphp.vulnweb.com/artists.php?artist=1".
http://testphp.vulnweb.com/search.php?test=query'
This URL has a SQL injection vulnerability. The payload "'" was added to the URL, resulting in an SQL injection error.
The vulnerable link detected is http://testphp.vulnweb.com/search.php?test=query'.
http://testphp.vulnweb.com/search.php?test=query
This URL has a SQL injection vulnerability. The payload " OR 1=1 --" was added to the form input field named searchFor, resulting in an SQL injection error.
The vulnerable link detected is http://testphp.vulnweb.com/search.php?test=query.
The form details for this vulnerable link:
Action: search.php?test=query
Method: post
Inputs:
Name: searchFor, Type: text, Value: ``
Name: goButton, Type: submit, Value: go

The Sql scanner/crawler was used to search for sql injection vulnerabilities
