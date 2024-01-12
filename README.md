# InventoryManagementSystem
InventoryManagementSystem is a simple dashboard that makes use of MongoDB and Dash. I created this program for the experience of full-stack development.

### Dependencies
This program uses the following libraries:
* Dash
* pymongo

### How to Use
1. Start a local MongoDB server.
2. Run the program.
3. Access the Dash server through your web browser using the address "localhost:8050".
4. Use the following credentials to login: username = "user", password = "password".
5. Select any row in the table that generates.
6. Use the modification menu under the table to modify the database.
7. Use the "Delete Database" button to remove the generated database and user account.
8. Close the program through your IDE.

### Important Notes
This program will create a local database of 100 entries using MongoDB. A user will also be created and given read/write access to the generated database. Because Dash's run_server() function is a blocking function, the system cannot properly delete the database automatically once the program is closed. To remedy this, I added a "Delete Database" button that needs to be used after logging in. This button will delete the database and the user before logging out of the system. The program can then be closed through your IDE without worry of storing any data to the database.

### Photos
When you first open the application in your browser, you will be greeted with this screen because you are not logged in:
![Dash Not Logged In](https://github.com/JacobWhetham/InventoryManagementSystem/assets/65636798/d3f5447f-af5d-444a-ba1d-091cfbb986b4)

If you do not use the proper credentials ("user" for the username and "password" for the password), you'll be met with this screen:
![Dash Invalid Creds](https://github.com/JacobWhetham/InventoryManagementSystem/assets/65636798/6cf5c56a-9008-4da5-86b4-8955431189b4)

Finally, after you log in, the data will be loaded into a table and you will be able to add, remove, or edit any entries:
![Dash Logged In](https://github.com/JacobWhetham/InventoryManagementSystem/assets/65636798/b93dbe66-35d9-437b-a13a-499b7c44e9bb)
