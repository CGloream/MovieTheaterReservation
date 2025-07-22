# MovieTheaterReservation
Author: Cheng Xu
a project for course "Basics of Programming - Exercise"

## 1. Topic Description
An application for maintaining a movie theater reservation system. The system has the following minimum requirements: 
- The theater has several (differently sized) halls 
- The theater shows several movies at the same time 
- Each hall has several screenings a day 
- A customer can reserve a seat for any show (provided there is room in the hall) 
- The administrator can add movies and screenings as well as browse reservations 

## 2. Solution Principle
Users interact with the system via graphical interface.
The system uses an object-oriented design, abstracting entities into classes.
Data persistence is achieved through file storage system.

## 3. Project Structure

### Data Model Module: core system entities
|Entities|Comment|
|:---|:---|
|Cinema|model of cinemas|
|ScreeningRoom|model of screening rooms|
|Movie|model of movies|
|Screening|model of screenings|
|Reservation|model of reservation orders|

### Business Logic Module: implement core functions
|Entities|Comment|
|:---|:---|
|ReservationManager|Handle reservation-related operations|
|AdminManager|Handles administrator operations|

### Data Storage Module:
|Entities|Comment|
|:---|:---|
|DataStorage|Responsible for loading and saving data|

### User Interface Module:
|Entities|Comment|
|:---|:---|
|CinemaApp|App with UI|

## 4. External Libraries Used
|Usage|Library|
|:---|:---|
|Data Storage|json|
|Graphical User Interface|tkinter|
|DataTime Handling|datetime|
|Data Validating|re|


## 5. User Process

User Reservation Process
User → Select Movie → Select Screening → Choose Seats → Confirm Reservation → System Validation → Generate Reservation Code → Save Data

Administrator Add Screening Process
Administrator → Login → Select "Add Screening" → Input Movie, Time, Screening Room → System Validation → Save Data

**Admin Account: admin**
**Admin password: admin123**

## 6. Something to be improved

It could be better to add a scroll bar in the app UI;
Due to the data connection, the app do not have the delete funtion (e.g. User cannot delete Movie or Rooms). If the app use Database Systems, the problem could be solved easily.
