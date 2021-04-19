# Back-end

  ### Setting up the back-end server:
  To setup your backend server you first need to install all the python dependencies with:
  
   ``` 
   pip install -r requirements.txt
   ```
   
   Once you have installed the required packages you need to change directory to: 
   
   ``` 
   cd yourpath\TL20-50\back-end\
   ```
   
   Then in order to run the server at the port 8765 you have to command:
   
   ``` 
   python manage.py runserver 8765 
   ```
  
  
  ### Database dump (json):
  
  In order to connect with your database, create all the necessery tables and insert data you have to do the following:
  
  Open the file yourpath\TL20-50\back-end\backend\settings.py find the section DATABASES = {} and fill it with your database credentials.
  
  Then in order to create the tables in the database you have to command:
  
   ``` 
   python manage.py migrate
   ```
   
   Congratulations now you have created your database!
   Now we have to fill the database with data.
   
   First of all we need to create our admin:
   ``` 
   python manage.py createsuperuser
   ```
   
   For the name of our admin we choose:  admin
   
   For the password of admin we choose: petrol4ever
   
   Fill in the rest fields as you wish.
   
   
   All we need to do now is type the following commands with the below order:
   
   ``` 
   python manage.py loaddata auth_user_hash.json
   ```
   
   ``` 
   python manage.py loaddata auth_user_groups.json
   ```
   
   ``` 
   python manage.py loaddata backendapp_apikeys.json
   ```
   
   ``` 
   python manage.py loaddata backendapp_area.json
   ```
   
   ``` 
   python manage.py loaddata backendapp_point_operator.json
   ```
   
   ``` 
   python manage.py loaddata backendapp_user.json
   ```
   
   ``` 
   python manage.py loaddata backendapp_vehicle.json
   ```
   
   ``` 
   python manage.py loaddata energy_providers.json
   ```
   
   ``` 
   python manage.py loaddata backendapp_monthly_charge.json
   ```
   
   ``` 
   python manage.py loaddata backendapp_locations_of_stations.json
   ```
   
   ``` 
   python manage.py loaddata backendapp_station.json
   ```
   
   ``` 
   python manage.py loaddata backendapp_stationrating.json
   ```
   
  ``` 
   python manage.py loaddata backendapp_charge.json
   ```
  
  
  To run our functional and unit tests you have to do:
  ``` 
   python manage.py test backendapp
   ```

