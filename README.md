![image](https://imgur.com/3HM0FJA.png)

## 📝 Description
Pin Flask is a unique project in order to find the right idea and inspiration.

Search and explore the expanses of PinFlask to find something new.

Create and share your own unique, authored content and rate the work of others.

> [!CAUTION]
> 🔐 The project is at an early stage of its development, development is underway, at the moment the current version is beta, stable operation is not provided. All features have not been added yet, expect further updates.

### 🖌️Features
1. 🔰 Easy interface: Fast loading and low server load
2. ⚙️ User-friendly and optimized interface
3. 🖼️ The ability to create posts
4. 📩 Saving images in their original resolution
5. 🛜 The ability to share your posts with other users.
6. 📨 Email Authorization and Validation
7. 🤖 AI fatures (soon)

### 🗝️ Used in the project
1. MySQL databases for data storage
2. Flask for the back part
3. Algorithms based on neural networks for selecting recommendations (soon)
4. Self-moderation of content (soon)

## 💽 First startup
`pip install flask flask-sqlalchemy flask-login flask-wtf flask-uploads python-dotenv pillow email_validator`
1. Check all files for integrity and activate the virtual environment
2. If necessary, go create a database
Start terminal and open `flask shell`.
`>>> from app import models`
   `>>> db.drop_all()`
   `>>> db.create_all()`

3. Run `flask run` or run.py file.
