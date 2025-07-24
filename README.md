# The Nail Lab PetqG


## Short description
    The Nail Lab PetqG is a Django Web Project.
        
        The website has a home page for users who do not have a user profile,
        with brief information about the site.
        
<img width="632" height="841" alt="Screenshot 2025-07-21 at 14 36 07" src="https://github.com/user-attachments/assets/632ff90a-fcf3-47af-9d9d-4d75982a779f" />

        Options to log in (if they have an account, they can also log in with Google) 
        or register.

<img width="1025" height="842" alt="Screenshot 2025-07-21 at 14 37 54" src="https://github.com/user-attachments/assets/fd8577b6-4465-494f-bcd8-1caa1be6d157" />
<img width="481" height="796" alt="Screenshot 2025-07-21 at 14 38 19" src="https://github.com/user-attachments/assets/3151b42b-6c25-4181-893b-4d4072c48bdc" />      

        The website also has a home page for users who already have a user profile,
        having permission for full CRUD operations over their profile 
        and current appointments.

<img width="624" height="734" alt="Screenshot 2025-07-21 at 14 41 00" src="https://github.com/user-attachments/assets/e1d041c5-4579-4c56-b59a-ea8c63d782ef" />

## Purpose
        Its purpose is:
            to show what services the specialist offers;
            to check if there are free hours and book if it's possible;
            to reserve manicure hours;
            to show reserved hours only to the client and the specialist for 
                whom the appointment is made;
            to edit its appointment and change it if its available.        
            to show if the specialist has a day off
            to show a gallery in which only the employee can upload photos 
                of their work;
            to show contacts and information about the specialist

            The user has access to their profile and can accordingly edit 
                and delete it if they wish;

## The project has 5 apps
    
    👤 accounts;
    ⏳ appointments;
    📷 photos;
    💅 services;
    🏠 studio;

### 👤 accounts app
    This app, contains the user profile logic.
    It has One BaseUser model and two children for 
    different user roles(EmployeeBio and ClientProfile).

    Models have additional validators for img size and 
    phone number validation.

    Every new user is set as client with the help of a signal.
    The employee profiles are set only 
    by admin user through admin panel and the Admin HAVE TO assign
    their services through EmployeeBioAdmin(through admin panel). 
    Upon creation the signal checks if the new user has status and
    if not employee- it is set as client.
    
    The user has option to authenticat with its email. 
    The 'ModelBackend' is rewritten.
    
    It has also an option to log in with Google email. 
    It uses a pipeline which checks if the user logs for first time,
    redirecting it to fill a form for completing it's profile(Save in DB).
    The authentication process goes through SOCIAL_AUTH_PIPELINE steps using 
    social authentication, such as Google authentication via django-allauth 
    or social-auth-app-django.
    They are arranged in order and sepparated with comments for better readability.

    The client profile has full CRUD operations on his profil and can:
        upload profile picture;
        edit profil info;
        delete profil.
    In addition, the employee profil has a biography section and has the 
    permission to add certificates, which appear in the Contacts page as
    part of personal business card.

### Client Profil example
<img width="609" height="683" alt="Screenshot 2025-07-21 at 14 52 17" src="https://github.com/user-attachments/assets/b447d643-be4c-42f8-bd85-23e89dc84fb4" />

### Employee Profil example
<img width="491" height="751" alt="Screenshot 2025-07-21 at 14 53 56" src="https://github.com/user-attachments/assets/3587de64-bc73-4e0c-a2cf-258becd050c7" />

### Address example
<img width="733" height="735" alt="Screenshot 2025-07-21 at 14 55 56" src="https://github.com/user-attachments/assets/779136b1-3ff9-4ccf-8522-0cd0d7aa3e3c" />

### ⏳ appointments app
    This app contains the appointments logic.
    It has two models: Appointment & DayOff
    
    The Appointment model gets the info for user, employee and service through 
    ForeignKey and also its data: date, start_time and comment.
    It has validator that is called in the model's save method.
    The validator 'AppointmentModelCleanValidator', checks if employee, service, 
    date and start_time are picked.
    Also checks if the Day is valid(present day and working day) and user can book
    an appointment only if the range (in minutes) fits the free time between 
    appointments. In other words it can not book during the time when the
    nail artist is awready busy.
    
<img width="414" height="607" alt="Screenshot 2025-07-21 at 14 57 30" src="https://github.com/user-attachments/assets/bfaa92c1-662d-4d03-9e5c-2bfae0a809e8" />

    The price and duration are shown with js:
<img width="413" height="634" alt="Screenshot 2025-07-21 at 14 58 03" src="https://github.com/user-attachments/assets/ff65ea71-3e52-49c6-ae38-ffda6b902f87" />    

    It also have a feature to check for available hours on a current date. 
    The service is looking for available appointments on a 
    selected date and employee.

<img width="418" height="353" alt="Провери за свободен час" src="https://github.com/user-attachments/assets/4bc4872d-a3c2-4fc5-83e8-ccd6ef7ab285" />
<img width="542" height="472" alt="Налични часове1" src="https://github.com/user-attachments/assets/11509b10-eb5d-44a0-a0d6-f9f790186dbd" />
<img width="530" height="507" alt="Налични часове2" src="https://github.com/user-attachments/assets/2af1b113-136d-444c-a012-55730ed1c648" />

    The DayOff model gets the info for employee also through ForeignKey and 
    has date fierld. It's main goal is to give the employee opportunity to 
    take a break on a day of his choice, only if this day is free of appointments.
<img width="423" height="231" alt="Screenshot 2025-07-21 at 15 03 48" src="https://github.com/user-attachments/assets/bcd7b711-2d1c-4238-a1bd-23f00193ac17" />
<img width="516" height="348" alt="Screenshot 2025-07-21 at 15 04 22" src="https://github.com/user-attachments/assets/41887e4c-3bac-4f8b-91a6-49198a51fd37" />

### 📷 photos app
    It has two models: GalleryPhoto & CertificateImage

    photos app gives the opportunity of the employee to upload:
        nail photos, showing off her work with clients
            Users can see them but only employee can 
            UPLOAD/DELETE; 

        certificate photos, show degree and are displayed in
            the address page, where employee info takes place.
            The employee uploads them through a button in 
            account details, but deletion process requires
            Admin intervention, using Admin panel.

## User point of view
<img width="583" height="471" alt="userview_gallery" src="https://github.com/user-attachments/assets/15a3fdba-b973-45b3-abcd-b551d92b156e" />
<img width="733" height="735" alt="certificates" src="https://github.com/user-attachments/assets/a0381ad7-fe2f-4a63-b55f-92e251619096" />

## Employee point of view
<img width="608" height="599" alt="employeeview_gallery" src="https://github.com/user-attachments/assets/e8bebc37-0b09-46ba-b1a8-856c60c01122" />



### 💅 services app
    It has one model: BaseService
    
    BaseService model is connected with EmployeeBio model 
    from accounts app through lazy evaluation ManyToManyField

    It has a page that shows all available services and a page
    for full detail description of the current service.

    Also has a search bar in the top of service_page.
    The logic is in ServiceListView. It uses service
    name and service description.

<img width="991" height="831" alt="services" src="https://github.com/user-attachments/assets/20710807-f367-46a6-84cf-a73857f2572b" />
<img width="434" height="616" alt="current_service" src="https://github.com/user-attachments/assets/c2d30442-4a52-4997-9960-5cb8362d22fe" />



### 🏠 studio app
    It has no models

    It's contains the logic for homepage.
    Based on the user role, it shows different content.
    
    If the user is anonymous it renders homepage with no-profile.
    This is the landing page and the user have only 'get' permissions.
<img width="661" height="845" alt="homepage_annonumous" src="https://github.com/user-attachments/assets/ee9656bb-061c-4f78-b938-01e929c4f103" />
    
    If the user is authenticated and authorised as a client he has full
    CRUD operations upon his profile and appointments.
    The appointments related to him are displayed in his homepage and
    if there is a day off for the employee- can see it too.
<img width="630" height="697" alt="homepage_client" src="https://github.com/user-attachments/assets/db5271ad-bdb9-4724-9248-9975079f2f29" />

    If the user is authenticated and authorised as a employee -
    full CRUD operations upon his profile and it's own appointments.
    Can see all clients appointments and if there is a day off for 
    the employee- can see it too.
<img width="614" height="925" alt="homepage_employee" src="https://github.com/user-attachments/assets/801749f6-fe56-437b-88e3-398debba0efe" />


