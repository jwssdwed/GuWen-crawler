# Description:
This is a python crawler built with `requests + parsel + sqlalchemy + re`. The purpose of this crawler is gathering Chinese ancient poetries from some public website in legal way. 

Folks who is new to python also welcomes to take a look at this project because the code is easy to understand and you could get experience on python with database and RESTful requests.
# Prerequest:
You need to have python3 and pip installed in your machine.
* Check the python version
    ```shell
    python -V
    ```
* Install pip:
    * Windows
        ```shell
        py -m pip install --upgrade pip
        ```
    * Mac and Unix
        ```shell
        python3 -m pip install --user --upgrade pip
        ```
# Preparation:
I recommend you to use Virtual Environment for this project. This is not necessary, but I don't want this project's dependencies to mess up your native environment.

1. Upgrade your pip
* Windows
    ```shell
    py -m pip --version
    py -m pip install --upgrade pip
    ```
* Mac or Unix
    ```shell
    python3 -m pip install --user --upgrade pip
    ```

2. Install virtual environment
* Windows
    ```shell
    py -m pip install --user virtualenv
    ```
* Mac or Unix
    ```shell
    python3 -m pip install --user virtualenv
    ```

3. Creating a virtual environment¶
* Windows
    ```shell
    py -m venv env
    ```
* Mac or Unix
    ```shell
    python3 -m venv env
    ```

4. Activating a virtual environment¶
* Windows
    ```shell
    .\env\Scripts\activate
    ```
* Mac or Unix
    ```shell
    source env/bin/activate
    ```

5. Validate/Confirm you have the virtual environment for this project
* Windows
    ```shell
    which python
    /Users/cheshen/personal/GuWen-crawler/env/bin/python.exe
    ```
* Mac or Unix
    ```shell
    which python
    /Users/cheshen/personal/GuWen-crawler/env/bin/python
    ```

6. Leaving the virtual environment
    ```shell
    deactivate
    ```
