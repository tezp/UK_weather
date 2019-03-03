# UK_weather
This is Django REST Api to get UK_weather.
## Getting Started
These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. 
### Prerequisites
Packages/Libraries need to install to run the project.
* django
```bash
pip3 install django
```
* django rest framework
```bash
pip3 install djangorestframework
```
## Running the project: 
1.  First we need to save the data into database using [Django management command](https://docs.djangoproject.com/en/2.1/howto/custom-management-commands/).</br>

    Open the terminal in project repository and type following command with URL (-u for URL).</br>
  ```bash
    python3 manage.py fetch_json_and_save -u https://s3.eu-west-2.amazonaws.com/interview-question-data/metoffice/Tmin-Wales.json
  ```
2.  Then start django server with following command :</br>
 ```bash
 python3 manage.py runserver
 ```
3. After starting django server, we have to check the UK_Weather API.</br>
   Here, we have created two separate APIs (but output is same) which will show output as json data and serialised json data.</br>
  * Get json data API using HTTP GET method request :</br>
    ```bash
    curl -X GET -i 'http://127.0.0.1:8000/getjsondata/?start_date=2010-01&end_date=2010-12&location=Wales&metric=Tmin'
    ```
  * Get serialised json data API using HTTP GET method request :</br>
    ```bash
    curl -X GET -i 'http://127.0.0.1:8000/getserialiseddata/?start_date=2010-01&end_date=2010-12&location=Wales&metric=Tmin'
    ``` 
4. To test the model, views and management commands :</br>
 ```bash
    python3 manage.py test
 ```
   

