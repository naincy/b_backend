# Benchmark Backend

Python - Django Project 

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites

```
Python should be installed. Link for downloading python: [Python Download](https://www.python.org/downloads/)
```

The Python installers for Windows include pip. You should be able to access pip using:
```
py -m pip --version
>>> pip 9.0.1 from c:\python36\lib\site-packages (Python 3.6.1)
```

You can make sure that pip is up-to-date by running:
```
py -m pip install --upgrade pip
```

### Installing

A step by step series of examples that tell you how to get a development env running

### 1) Installing and Creating Virtual Environment for Project Dependencies:

On macOS and Linux:

```
python3 -m pip install --user virtualenv
```

On Windows:
```
py -m pip install --user virtualenv
```

To create a virtual environment, go to your project’s directory and run virtualenv.

On macOS and Linux:
```
python3 -m virtualenv env
```

On Windows:
```
py -m virtualenv env
```

The second argument is the location to create the virtualenv. Generally, you can just create this in your project and call it env.

virtualenv will create a virtual Python installation in the env folder.


### 2) Activating a virtualenv

Before you can start installing or using packages in your virtualenv you’ll need to activate it. Activating a virtualenv will put the virtualenv-specific python and pip executables into your shell’s PATH.

On macOS and Linux:
```
source env/bin/activate
```

On Windows:
```
.\env\Scripts\activate
```

### 3) Installing packages

Go the project root folder where requirements.txt is present and run:
```
pip install -r requirements.txt
```
Above command should install all the required dependencies into the virtual environment.

### 4) Configuring AWS keys

To configure AWS Keys run the command:
```
aws configure
```
Above command will ask for inputs for access key and secret key. Get the key details from the Team lead.

### 5) Starting the Django App

Go the project root folder and run:
```
python manage.py runserver
```

### Leaving the virtualenv

If you want to switch projects or otherwise leave your virtualenv, simply run:
```
deactivate
```
If you want to re-enter the virtualenv just follow the same instructions above about activating a virtualenv. There’s no need to re-create the virtualenv.

### API Gateway
API Gateway configuration
![AWS API Gateway](https://s3.ap-south-1.amazonaws.com/benchmark-dam/screenshots/api-gateway.JPG  "AWS API Gateway")

### API Specifications

API Docs: 
```
http://api-docs-benchmark.s3-website.ap-south-1.amazonaws.com/ 
```

![API's](https://s3.ap-south-1.amazonaws.com/benchmark-dam/screenshots/swagger.JPG "API's")


