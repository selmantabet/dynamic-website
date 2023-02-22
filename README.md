# CMT120 Coursework 2 - Dynamic Website

Username: c22076452

Link to website: http://c22076452-cmt120-cw2-prod-c22076452-cmt120-cw2.apps.openshift.cs.cf.ac.uk/

#### [Website Quality Report](c22076452_report.pdf)

---

## Demo Video

## [![Website Video Demo](https://i.ytimg.com/vi/Q3_VkIxhObg/maxresdefault.jpg)](https://youtu.be/Q3_VkIxhObg "Website Video Demo")

---

### References - Source Code:

- Navbar Implementation based on Bootstrap 5.3 Docs (https://getbootstrap.com/docs/5.3/components/navbar/)
- File upload mechanism based on Flask-Uploads Docs (https://flask-uploads.readthedocs.io/en/latest/)
- File size validation based on a Stack Overflow answer by Gokul NC (https://stackoverflow.com/a/67172432/11690953)
- Login and Registration mechanisms based an implementation by Dr. Natasha Edwards at Cardiff University for the CMT120 lab material.

Images used throughout the site are appropriately referenced in the form of in-line comments.

---

## Instructions (Local Deployment - Empty Site)

You may opt to use a virtual environment as follows:

On Windows (NT)

```bash
python3 -m venv venv
.\venv\Scripts\activate
```

On UNIX-based systems (POSIX)

```bash
python -m venv venv
source venv/bin/activate
```

Install the required packages using pip.

```bash
pip install -r requirements.txt
```

Run the following command to create the database:

```
python db_creation.py
```

Then press Enter to confirm creation.
You will be prompted to enter an Admin password. This password will be used to set up the Admin account.

Then, run the Flask application:

```
flask run
```

Alternatively, you can run the application using the following command:

```
python wsgi.py
```

---

## Instructions (Remote Deployment)

### Prerequisites

Inject the following environment variables into the deployment:

- `ENV_TYPE` - should either be `PROD` or `STAGING`
- `MYSQL_ADDRESS` - MySQL Database Address
- `MYSQL_DB_NAME` - MySQL Database Name
- `MYSQL_USER` - MySQL Database Address
- `MYSQL_PASSWORD` - MySQL Database Password

The database must be in MySQL, other databases can work by modifying the dialect and driver parts of the URI in `cfg.py`. Just ensure that the environment variables are set up properly and that the database URI is correctly formatted using the logs.

### Initial Setup

On the shell of the deployment container, run the following commands:

```
python db_creation.py
```

You should see the address and name of the target database, ensure that they are the correct parameters.
Then press Enter to confirm creation.
You will be prompted to enter an Admin password. This password will be used to set up the Admin account.

You may now serve the application through a pod restart.
