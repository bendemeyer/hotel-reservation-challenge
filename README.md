# Hotel Reservation Challenge

A small Django app to simulate a configurable hotel reservations system

Uses SQLite as its data store. The data is non-relational, so depending on expected usage a NoSQL store might be a valid choice. But for the purposes of this project I choose to keep it as portable as possible, which SQLite acheives very well.

## Setup

### Requirements

The setup guide assumes installation on a *nix system. The application should work on Windows systems as well, but you're on your own figuring that out. Required packages are:

- `python3`
- `python3-venv` or `virtualenv`

### Steps

Once you have cloned the repository, perform the following steps to run the application locally.

1. Create a virtual environment for the project by running either of the following commands from the project root
    - `python3 -m venv ./python_env`
    - `virtualenv ./python_env -p python3`
1. Activate the virtual environment
    - `source python_env/bin/activate`
1. Install project dependencies
    - `pip install -r requirements.txt`
1. Swich to the directory containing the Django project
    - `cd keypr`
1. Prepare Django database setup
    - `python manage.py makemigrations`
1. Run Django database setup
    - `python manage.py migrate`

With those steps complete, you should now be able to start up a local instance of the application with the following:

- `python manage.py runserver`

This will start the server running on port 8000, and accepting only requests originating from your local machine.

You can also run the unit tests with:

- `python manage.py test hotel_reservations.tests`

### Optional Setup

You may want to create a Django superuser which will allow you to manage reservations and hotel configuration from the Django admin area. To create this user, run:

- `python manage.py createsuperuser`

and follow the interactive instructions. Once complete, you can use the username and password you entered to access the admin site at `/admin/`

## Usage

The application can be used either as a standard Web UI application, or via REST API endpoints. (The instructions were a little ambiguous, they called for a REST API specifically, but also made some references to funcitonality that seemed closer to a web UI. So I decided to just build both since the additional effort was pretty minimal)

### The Data

#### Reservations

A reservation entry is made up of four fields:

- `name`

    A string. The name of the person making the reservation
    
    Validations:

    - None

- `email`

    A string. The email address of the person making the reservation

    Validations:

    - A non-strict check to ensure that the string is formatted somewhat like an email address

- `check_in`

    A date. If submitted as a string, the format YYYY-MM-DD should be used. The date that marks the beginning of the reservation.

    Validations:

    - The date provided must be on-or-after the current date.

- `check_out`

    A date. If submitted as a string, the format YYYY-MM-DD should be used. The date that marks the end of the reservation.

    Validations:

    - The date provided must be after the check-in date.

One additional non-field-level validation takes place before a reservation can be created. The system will check that there is at least one room available each night of the requested reservation.

#### Hotel Configuration

The hotel configuration data is made up of two fields:

- `room_count`

    An integer. The total number of rooms in the hotel available to reserve.

    Validations:

    - Must be greater than zero

- `overbooking_level`

    A float. Determines the level to which the system will overbook. To determine the total number of bookable rooms, the system will add `1` to this value and multiply the result by the `room_count`. So in effect, a value of `0.1` in this field represents an overbooking level of 10%. A value of `1` represents an overbooking level of 100%.

    Validations:

    - Must be greater than or equal to zero

### Web UI

The web UI can be used to submit new reservations using the landing page at `/`. This form includes all fields required for creating a reservation and will prevent submission and show appropriate error messaging in cases where the submission was invalid.

Additionally, functionality for creating, updating and deleting reservations can be found in the Django admin site at `/admin/`. Also in the admin section is a method for editing the "Hotel Configuration", which allows setting the total room count and the acceptable level of overbooking.

### API

Two REST API endpoints are exposed, one for creating new reservations and one for editing the hotel configuration.

Both API endpoints are write-only, so only accept POST requests. Both expect the request body to be formatted in JSON, and the request header should specify `Content-Type: application/json`.

If the request is handled successfully, the server will respond with a 201 status code and return the contents of the request body back in the response as confirmation. If an error is encountered trying to process the request, the server will respond with a status code 400 and the response body will be a dictionary of errors, where the key is the field that caused the error and the value is the error message.

#### Reservations

The reservations API endpoint exists at `/reservations/`. An example request body should look like this:

```json
{
    "name": "Guest Name",
    "email": "guest@example.com",
    "check_in": "2018-05-01",
    "check_out": "2018-05-02"
}
```

#### Hotel Configuration

The hotel configuration API endpoint exists at `/config/`. An example request body should look like this:

```json
{
    "room_count": 100,
    "overbooking_level": 0.1
}
```