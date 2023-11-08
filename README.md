# M7011E


## Setup
Recommended is to use a [virtaulenv](https://virtualenv.pypa.io/en/latest/).

To install all dependencies: (in terminal)
```bash
pip install -r requirements
```

### Errors

**Exception: Can not find valid pkg-config name.  Specify MYSQLCLIENT_CFLAGS and MYSQLCLIENT_LDFLAGS env vars manually**

This can (in Ubuntu 22.04.3 LTS) be fixed by writing the following command:
```bash
sudo apt-get install libmysqlclient-dev
```

## Run the project
To run the project either write: (in terminal)
```bash
python main.py
```
Or if [code runner](https://marketplace.visualstudio.com/items?itemName=formulahendry.code-runner) is installed, just press `Ctrl + Alt + k`


## Coding best practices
This project uses flake8 (PEP8), with black formatter. Best way to integrate this is to install the extensions:
* [black](https://marketplace.visualstudio.com/items?itemName=ms-python.black-formatter)
* [flake8](https://marketplace.visualstudio.com/items?itemName=ms-python.flake8)