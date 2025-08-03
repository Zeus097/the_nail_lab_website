# 🌐 [The Nail Lab PetqG](https://the-nail-lab.onrender.com)


## Technologies:


<p>
  <img src="https://static.djangoproject.com/img/logos/django-logo-negative.svg" alt="Django Logo" width="40"/>
  <span style="vertical-align: middle; font-weight: bold">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Framework&nbsp;&nbsp;&nbsp;</span>
</p>


<p>
  <img src="https://www.postgresql.org/media/img/about/press/elephant.png" alt="PostgreSQL" width="30"/>
  <span style="vertical-align: middle; font-weight: bold">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Hosted on <a href="https://supabase.com" target="_blank">SUPABASE</a></span>
</p>

<p>
  <img src="https://miro.medium.com/v2/resize:fit:1400/1*YWzEFaE_YKwhKYStTkMpGw.png" alt="Media" width="55" style="vertical-align:middle;"/>
  <span style="vertical-align:middle; font-weight: bold
">&nbsp;&nbsp;&nbsp;Media Service hosted on <a href="https://cloudinary.com" target="_blank">CLOUDINARY</a></span>
</p>

<br></br>

## Short description
* The Nail Lab PetqG is a Django Web Project.
        
* The website has a home page for users who do not have a user profile,</br> 
with brief information about the site.

<br></br>
        
<img width="632" height="841" alt="Screenshot 2025-07-21 at 14 36 07" src="https://github.com/user-attachments/assets/632ff90a-fcf3-47af-9d9d-4d75982a779f" />

<br></br>

* Options to log in (if they have an account, they can also log in with Google) </br> 
or register.

<br></br>

<img width="1025" height="842" alt="Screenshot 2025-07-21 at 14 37 54" src="https://github.com/user-attachments/assets/fd8577b6-4465-494f-bcd8-1caa1be6d157" />
<img width="481" height="796" alt="Screenshot 2025-07-21 at 14 38 19" src="https://github.com/user-attachments/assets/3151b42b-6c25-4181-893b-4d4072c48bdc" />      

<br></br>

* The website also has a home page for users who already have a user profile,</br> 
having permission for full CRUD operations over their profile</br>
and current appointments.

<br></br>

<img width="624" height="734" alt="Screenshot 2025-07-21 at 14 41 00" src="https://github.com/user-attachments/assets/e1d041c5-4579-4c56-b59a-ea8c63d782ef" />

<br></br>

## Purpose
Its purpose is:
* to show what services the specialist offers;
* to check if there are free hours and book if it's possible;
* to reserve manicure hours;
* to show reserved hours only to the client and the specialist for 
whom the appointment is made;
* to edit its appointment and change it if its available.        
* to show if the specialist has a day off
* to show a gallery in which only the employee can upload photos 
of their work;
* to show contacts and information about the specialist

* The user has access to their profile and can accordingly edit </br> 
and delete it if they wish;

<br></br>

## The project has 5 apps
    
* 👤 &nbsp;&nbsp;*accounts;*


* ⏳ &nbsp;&nbsp;*appointments;*


* 📷 &nbsp;&nbsp;*photos;*


* 💅 &nbsp;&nbsp;*services;*


* 🏠 &nbsp;&nbsp;*studio;*

### 👤 accounts app

<span style="font-weight: bold; color: #1b6d85">
    The <span style="color: #00dd00">employee</span> profiles are set only</br> 
    by <span style="color: #00dd00">admin user</span> through admin panel. Admin have</br> to <span style="color: #00dd00">assign
    their services</span> through EmployeeBioAdmin</br>(also through admin panel).
</span>

* This app, contains the user profile logic.
* It has One BaseUser model and two children for</br> 
different user roles(EmployeeBio and ClientProfile).


* Models have additional validators for img size and</br> 
phone number validation.


* Every new user is set as client with the help of a signal.
* Upon creation the signal checks if the new user has status and</br> 
if not employee- it is set as client.
    

* The user has option to authenticat with its email. 
* The 'ModelBackend' is rewritten.

* It has also an option to log in with Google email. 
* It uses a pipeline which checks if the user logs for first time,</br> 
redirecting it to fill a form for completing it's profile(Save in DB).
* The authentication process goes through SOCIAL_AUTH_PIPELINE steps using </br> 
social authentication, such as Google authentication via django-allauth </br> 
or social-auth-app-django.
* They are arranged in order and sepparated with comments for better readability.


* The client profile has full CRUD operations on his profil and can:
  * upload profile picture;
  * edit profil info;
  * delete profil.
  

* In addition, the employee profil has a biography section and has the </br> 
permission to add certificates, which appear in the Contacts page as</br> 
part of personal business card.

<br></br>

### Client Profil example
<img width="609" height="683" alt="Screenshot 2025-07-21 at 14 52 17" src="https://github.com/user-attachments/assets/b447d643-be4c-42f8-bd85-23e89dc84fb4" />

<br></br>

### Employee Profil example
<img width="491" height="751" alt="Screenshot 2025-07-21 at 14 53 56" src="https://github.com/user-attachments/assets/3587de64-bc73-4e0c-a2cf-258becd050c7" />

<br></br>

### Address example
<img width="733" height="735" alt="Screenshot 2025-07-21 at 14 55 56" src="https://github.com/user-attachments/assets/779136b1-3ff9-4ccf-8522-0cd0d7aa3e3c" />

<br></br>

### ⏳ appointments app
* This app contains the appointments logic.
* It has two models: Appointment & DayOff.
    

* The Appointment model gets the info for user, employee and service through</br>
ForeignKey and also its data: date, start_time and comment.
* It has validator that is called in the model's save method.
* The validator 'AppointmentModelCleanValidator', checks if employee, service, </br>
date and start_time are picked.
* Also checks if the Day is valid(present day and working day) and user can book</br>
an appointment only if the range (in minutes) fits the free time between </br>
appointments. In other words it can not book during the time when the</br>
nail artist is awready busy.
    
<br></br>

<img width="414" height="607" alt="Screenshot 2025-07-21 at 14 57 30" src="https://github.com/user-attachments/assets/bfaa92c1-662d-4d03-9e5c-2bfae0a809e8" />

<br></br>

* The price and duration are shown with js:

<br></br>

<img width="413" height="634" alt="Screenshot 2025-07-21 at 14 58 03" src="https://github.com/user-attachments/assets/ff65ea71-3e52-49c6-ae38-ffda6b902f87" />    

<br></br>

* It also have a feature to check for available hours on a current date. 
* The service is looking for available appointments on a</br>
selected date and employee.

<br></br>

<img width="418" height="353" alt="Провери за свободен час" src="https://github.com/user-attachments/assets/4bc4872d-a3c2-4fc5-83e8-ccd6ef7ab285" />
<img width="542" height="472" alt="Налични часове1" src="https://github.com/user-attachments/assets/11509b10-eb5d-44a0-a0d6-f9f790186dbd" />
<img width="530" height="507" alt="Налични часове2" src="https://github.com/user-attachments/assets/2af1b113-136d-444c-a012-55730ed1c648" />

<br></br>

* The DayOff model gets the info for employee also through ForeignKey and</br>
has date fierld. 
* It's main goal is to give the employee opportunity to</br>
take a break on a day of his choice, only if this day is free of appointments.

<br></br>

<img width="423" height="231" alt="Screenshot 2025-07-21 at 15 03 48" src="https://github.com/user-attachments/assets/bcd7b711-2d1c-4238-a1bd-23f00193ac17" />
<img width="516" height="348" alt="Screenshot 2025-07-21 at 15 04 22" src="https://github.com/user-attachments/assets/41887e4c-3bac-4f8b-91a6-49198a51fd37" />

<br></br>

### 📷 photos app
* It has two models: GalleryPhoto & CertificateImage.


* photos app gives the opportunity of the employee to upload:</br>
  * nail photos, showing off her work with clients.
  * Users can see them but only employee can</br>
UPLOAD/DELETE; 


* certificate photos, show degree and are displayed in</br>
the address page, where employee info takes place.
* The employee uploads them through a button in</br>
account details, but deletion process requires</br>
Admin intervention, using Admin panel.

<br></br>

## User point of view
<img width="583" height="471" alt="userview_gallery" src="https://github.com/user-attachments/assets/15a3fdba-b973-45b3-abcd-b551d92b156e" />

<br></br>

## Employee point of view
<img width="608" height="599" alt="employeeview_gallery" src="https://github.com/user-attachments/assets/e8bebc37-0b09-46ba-b1a8-856c60c01122" />

<br></br>

### 💅 services app
* It has one model: BaseService
    

* BaseService model is connected with EmployeeBio model</br>
from accounts app through lazy evaluation ManyToManyField.

* It has a page that shows all available services and a page</br>
for full detail description of the current service.

* Also has a search bar in the top of service_page.
* The logic is in ServiceListView. It uses service</br>
name and service description.

<br></br>

<img width="991" height="831" alt="services" src="https://github.com/user-attachments/assets/20710807-f367-46a6-84cf-a73857f2572b" />
<img width="434" height="616" alt="current_service" src="https://github.com/user-attachments/assets/c2d30442-4a52-4997-9960-5cb8362d22fe" />

<br></br>


### 🏠 studio app
* It has no models


* It's contains the logic for homepage.
* Based on the user role, it shows different content.
    
* If the user is anonymous it renders homepage with no-profile.</br>
This is the landing page and the user have only 'get' permissions.

<img width="661" height="845" alt="homepage_annonumous" src="https://github.com/user-attachments/assets/ee9656bb-061c-4f78-b938-01e929c4f103" />
   
<br></br>

* If the user is authenticated and authorised as a client he has full</br>
CRUD operations upon his profile and appointments.
* The appointments related to him are displayed in his homepage and</br>
if there is a day off for the employee- can see it too.

<br></br>

<img width="630" height="697" alt="homepage_client" src="https://github.com/user-attachments/assets/db5271ad-bdb9-4724-9248-9975079f2f29" />

<br></br>

* If the user is authenticated and authorised as a employee -</br>
full CRUD operations upon his profile and it's own appointments.
* Can see all clients appointments and if there is a day off for</br> 
the employee- can see it too.

<br></br>

<img width="614" height="925" alt="homepage_employee" src="https://github.com/user-attachments/assets/801749f6-fe56-437b-88e3-398debba0efe" />

<br></br>

### Tests

* The project contains tests package. All available tests are inside it.
* The single 'tests.py' files were deleted.
    
### Views tests

* As my SECRET_KEY is not public, the tests need the key assigned as a</br>
variable, or to be placed as raw text in 'settings.py' for local debug.

<br></br>
  
## 💡 👨‍💻 🚀 &nbsp;Upcoming Features

* 📩 Email notification. 
  * using 'Mailjet', when user create/edit/delete an appointment.

<br></br>

