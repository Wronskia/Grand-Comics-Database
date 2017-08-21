# ComicsDB
Steps to execute:

1 - navigate to the root folder of the project

2 - create a virtual environment and install requirements (virtualenv is required)
```
virtualenv -p python3 env
source env/bin/activate
pip install -r requirements.txt
```

3 - download and run elasticsearch 2.2.x, it can be found [here](https://www.elastic.co/downloads/past-releases)
```
cd elasticsearch/elasticsearch-2.2.x/bin/elasticsearch
```

4 - populate elasticsearch with the tuples of the database (this can take 30 minutes to an hour)
```
itbscomics/manage.py search_index --rebuild
```

5 - run the server
```
itbscomics/manage.py runserver 0.0.0.0:8000
```

6 - open in browser the link [http://127.0.0.1:8000](http://127.0.0.1:8000)


