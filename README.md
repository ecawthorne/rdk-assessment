# rdk-assessment
Simple MVC architecture. 

Unit tests for the model and controller could be added fairly easily, the model's database could be replaced with an 
RDBMS or something similar, view could be replaced by another front end such as a webpage.

Important static data is kept in a config file, other options could be added there as needed. 

API key is assumed to be stored in an environment variable called <OPENWEATHER_API_KEY>.  

Input validation, JSON validation, response and error handling would be the first things I would improve if the 
development of this app was continued.

Python 3.10+ required to run as the main module uses the match case functionality.
