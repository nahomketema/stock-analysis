# Introductions
Have you ever missed out on popular stocks because you missed the trend? Have you ever found yourself browsing through reddit/twitter trying to find the next big stock that is going to go to the moon? If so, you're at the right place.
Welcome to **Stock Analysis**, where the goal of this program is to give users a one-stop place to view and analyze stocks they are interested in investing.

# Setup Instructions
Once you have downloaded this program, There are a few steps needed before you can run it. 
1. In order to install all of the required dependencies, type in ``pip3 install -r requirements.txt``. Note that some libraries might need admin permissions in order to install.
2. Once that is done sign up for an Alphavantage API key as well as a Twitter API Key. After you obtain those APIs, navigate to the file called **api.py** and paste your API keys there.
3. Before running this program, make sure that all of the files within that program have enough permissions in order to run.
4. Upon completion of the steps above, you can run the program by typing in ``python3 main.py``.

# Disclaimers
* If you plan on investing, invest at your own risk. By using this program, you accept that neither **Stock Analysis** nor the developers are liable for any losses incurred by the usage of this program.
* Note that this program is still under development and therefore has features not fully developed and is prone to errors.
* In order to use this program you would need to acquire API keys from Alphavantage/Twitter. Look into the **Setup Instructions** section to learn more about how to use those
* Some of the files within this program are not implemented yet and therefore are not required for this program to run. These files are **database.py** and **flask_routes.py** respectively.

# Contact Info

Name          | Email
--------------|-------------
Nahom Ketema  |  nketema1@gmail.com

# License
[GNU general public license](license/license.md)

> Special thanks to Alphavantage and Twitter for providing free APIs which had more than enough calls with which this program could operate. Also special thanks to the developers of the many libraries that were used to make this program.