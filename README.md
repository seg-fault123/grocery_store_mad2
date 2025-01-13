# Modern Application Development 2 Projet
## IIT Madras Online BS Degree in Data Science and Applications (Diploma Level)
## September 2023
### Grocery Store Application
The Grocery Store Web Application is a full-stack platform designed to streamline the shopping experience for customers, simplify inventory management for store managers, and provide robust administrative controls for system administrators. Built between September 2023 and November 2023, the application supports three user roles:

* Customers: Can browse available products, make purchases, and review their order history with ease. Additionally, they receive automated reminders and notifications via email, enhancing user engagement and convenience.
* Store Managers: Have access to tools for adding, renewing, and tracking product inventory, helping manage stock efficiently and monitor revenue.
* Administrators: Are empowered to approve manager requests, manage product categories, and oversee the smooth functioning of the platform.

The application was developed using Flask (Python) to build the backend API, SQL for database management, and VueJS (JavaScript) for creating a dynamic and responsive frontend interface. To further improve performance and user experience, Redis was integrated for caching, significantly reducing response times for frequent operations. Additionally, the application includes email functionality to notify and remind customers, ensuring seamless communication and user retention. This functionality was implemented using Celery.

This project showcases the seamless integration of multiple technologies to deliver a feature-rich, user-friendly, and efficient web application tailored to the needs of a modern grocery store.

### Project Structure
The project is divided into two main directories:
* `backend/` : This directory contains the code to run the backend tasks.
    * `app.py` : The file that initializes the Flask Application for backend tasks.
    * `celeryconfig.py` : contains the configuration for initializing the celery instance
    * `application/` : This directory contains the helper modeules that are required by the app.
        * `admin_api.py` : Code for end points specific to the Admin in the app.
        * `api.py` : code for initializing the JWTManager and api instance.
        * `customer_api.py` : Code for end points specific to the Customer in the app.
        * `database.py` : code for initializing the database instance for the app.
        * `models.py` : ORMs for the database.
        * `my_mail.py`: code for sending the mails.
        * `store_manager.py` : Code for end points specific to the Store Manager in the app.
        * `tasks.py` : code for doing asynchronous tasks for celery.
        * `worker.py` : Initialize a celery worker

* `frontend/` :  This directory contains the code to run the frontend tasks. The main code for frontend is present in the `src/` subdirectory. 
    * `src/components/` : This directory has all the vue components used to create the frontend. 
        * `admin/` : all vue components related to the Admin part of the frontend. 
        * `customer/` : all vue components related to the Customer part of the frontend. 
        * `store_manager/` : all vue components related to the Store Manager part of the frontend. 
    * `src/router/index.js` : This file has all the routing configurations that govern the url structure of the application.
    * `App.vue` : code for initializing the Vue app.
    * `main.js` : code for linking the vue app, vue store manager, and vue router. 

The Entity Relationship diagram of the objects in the data flow is present in `Flowchart.png`

To look at the demo of the project, view the [here](https://drive.google.com/file/d/1bxUNI1XlOvmkWwfi62kWxrfYFbskF1uf/view?usp=sharing).