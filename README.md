# M7011E


## Setup
Pull the repository to your machine. 

Make sure that you have docker installed. 

## Run the project

Open up total of three terminals. Locate to one of  the shared_interface, item_worker and user_worker folder in each of the terminals. 

Run the following command inside of each map. Start with the shared_interface. 
```
docker compose up -d --build 
```

Wait untill the workers are connected. 

Congratulations! <br>

Now you can use Postman to send requests to access all of the functionality.

## Coding best practices
This project uses flake8 (PEP8), with black formatter. Best way to integrate this is to install the extensions:
* [black](https://marketplace.visualstudio.com/items?itemName=ms-python.black-formatter)
* [flake8](https://marketplace.visualstudio.com/items?itemName=ms-python.flake8)
