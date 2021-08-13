# Library-Management-System

This is a comprehensive LMS that runs on the command line. To run this system, please download all the files and keep them in the same folder. Execute the lms.py file to begin. Any changes that are made in the system will remain intact even if the system is shut down. 

## Features of the System:
There are 2 types of users: admin and regular user. Dummy users have been created for both initially.
The admin can do the following tasks:
1. Issue and return books
2. See available stock
3. Block and Unblock users
4. Delete users
5. See books issued to any user
6. Change password

The regular user can:
1. Issue and return books
2. See books issued to them
3. Change password

Anyone who is not a user or admin, can also see what books are availble at the library and which ones are in stock. Unfortunately, they will have to create an account with the library to issue books.

The system users can press the key "b" at any time to go back one step in the system. While in the main menu, key "q" can be used to safely quit.

Libraries Used:
1. Pandas
2. getpass
3. os
4. re
