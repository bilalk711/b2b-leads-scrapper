## B2B Leads Web Scrapper for European Companies

### Overview
Python script to scrap email and names of European B2B Companies.

### Configuration
Python package manager (PIP)[https://pypi.org/project/pip/] is required for this project.
After installing PIP, you will have to create a virtual environment for this project.
Install the virtual environment package by running the following command:
`pip install virtualenv`
Create the virtual environment:
`virtualenv env`
and then activate the environment:
On Windows: `.\env\Scripts\activate`
On Mac: `source env/bin/activate`

and then run the following command to install the required packages in the virtual environment:
`pip install -r requirements.txt`
This will install all the required packages.
Now you can execute the script.

### How To Use
Run the following command:
`python main.py AT software` 
This will fetch records of Austrian B2B Company emails and names and save it inside the `data` directory.
