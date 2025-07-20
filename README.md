# The Nail Lab Website


## Short description
    The Nail Lab is a Django Web Project.
        
        The website has a home page for users who do not have a user profile,
        with brief information about the site.
        
<img width="632" height="846" alt="Screenshot 2025-07-19 at 18 29 09" src="https://github.com/user-attachments/assets/7d3c8e15-0b34-4562-88c1-8bcb71bd3185" />

        Options to log in (if they have an account, they can also log in with Google) 
        or register.

<img width="933" height="800" alt="Screenshot 2025-07-19 at 18 28 53" src="https://github.com/user-attachments/assets/544fa6ef-db9c-4fad-85fa-4766730c4d90" />
<img width="380" height="906" alt="Screenshot 2025-07-19 at 18 37 53" src="https://github.com/user-attachments/assets/4f14ba29-64cf-4f77-8c5a-6a7f89350621" />       

        The website also has a home page for users who already have a user profile,
        having permission for full CRUD operations over their profile and current appointments.

<img width="628" height="764" alt="Screenshot 2025-07-18 at 18 54 37" src="https://github.com/user-attachments/assets/7fa0c61a-8481-4159-b292-cd65931ec7dd" />

        Its purpose is to:
            To show what services the specialist offers;
            To check if there are free hours and book if it's possible;
            To reserve manicure hours;
            To show reserved hours only to the client and the specialist for whom the appointment is made;
            To edit its appointment and change it if its available.        
            To show if the specialist has a day off
            To show a gallery in which only the employee can upload photos of their work;
            To show contacts and information about the specialist
            The user has access to their profile and can accordingly edit and delete it if they wish;

## The project has 5 apps
    
    👤 accounts;
    ⏳ appointments;
    📷 photos;
    💅 services;
    🏠 studio;

### 👤 accounts app
    This app, contains the user profile logic.
    It has One BaseUser model and two children for different user roles(EmployeeBio and ClientProfile).
    Models have additional validators for img size and phone number validation.
    Every new user is set as client with the help of a signal. The employee profiles are set only 
    by admin user through admin panel. Upon creation the signal checks if the new user has status and 
    if not employee it is set as client.
    The user has option to authenticat with its email. The 'ModelBackend' is rewritten.
    
    It has also an option to log in with Google email. It uses a pipeline which checks if the user logs for first time,
    redirecting it to fill a form for to complete it's profile(Save in DB).
    The authentication process goes through SOCIAL_AUTH_PIPELINE steps using 
    social authentication, such as Google authentication via django-allauth or social-auth-app-django.
    They are arranged in order and sepparated with comments for better readability.

    The client profile has full CRUD operations on his profil and can:
        upload profile picture;
        edit profil info;
        delete profil.
    In addition, the employee profil has a biography section and has the permission to add certificates,
    which appear in the Contacts page as part of his business card.

### Client Profil example
<img width="581" height="781" alt="Screenshot 2025-07-20 at 2 59 39" src="https://github.com/user-attachments/assets/d55cff37-4208-4cf2-8508-87e454713426" />

### Employee Profil example
<img width="447" height="816" alt="Screenshot 2025-07-20 at 3 00 45" src="https://github.com/user-attachments/assets/9a5e1fac-753b-4d46-a906-2159dcb5741f" />

### appointments app
    This app contains the appointments logic.
    It has two models: Appointment & DayOff
    
    The Appointment model gets the info for user, employee and service through ForeignKey and also its data:
    date, start_time and comment.
    It has validator that is called in the model's save method.
    The validator 'AppointmentModelCleanValidator', checks if employee, service, date and start_time are picked.
    Also checks if the Day is valid(present day and working day) and user can book an appointment only if the 
    range (in minutes) fits the free time between appointments. In other words it can not book during the time when the
    nail artist is awready busy.
    
    The DayOff model gets the info for employee also through ForeignKey and has date fierld.
    It's main goal is to give the employee opportunity to take a break on a day of his choice, only if this day
    is free of appointments.