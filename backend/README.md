# Daycare-Network
### An app, focused on delivering two-way daycare services. Parents can take care of other parents' children.
v. 1.0.0.
Setup:
1. Install the packages from requirements.txt  
2. Setup database  
3. Migrate  
4. Make sure the site id in database is the same as the one in setting.py (for the google login)  
5. Run server  
6. Enjoy! :)  

### Steps in development:  
1. Setup settings.py, create database
2. Setup urls.py
3. Create the basic models in models.py  
3.1. Add custom validation in validators.py  
3.2. Make migrations and add them to the database  
4. Create the basic templates
5. Create custom forms in forms.py and make input validations (the same as for the models)
6. Create views and forms and make corresponding changes to the rest of the app:   
6.1. Create register new user view  
6.2. Create login view and authentication  
6.3. Create logout view  
6.4. Implement password hash
6.5. Customize each user homepage template
7. Add settings section, where each user can edit his/her login or personal information
8. Add search panels  
8.1. Search panel for daycare services (find service)  
8.2. Search panel for daycare offers (find job)
9. Add change username/password options
10. Add edit user data functionality
11. Add delete user functionality
12. Add display all users functionality
13. Add create new offer functionality
14. Fix register new user functionality - add error message when username is already taken.
