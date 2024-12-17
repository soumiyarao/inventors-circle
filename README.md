# Inventors Circle
A Collaborative Social Network for Inventors

Inventor Circle, is a social media platform designed exclusively for inventors. Our mission is to help inventors expand their professional network by connecting with collaborators and mentors.

Inventors can showcase their research interests, identify like-minded professionals, and work together to generate groundbreaking ideas that could lead to future patents.

Not only that this platform also provides the opportunity for user to leverage the Inventor community to access valuable resources, including legal services, ways to earn royalties, and staying updated on events and opportunities in the innovation ecosystem.

Installations required:
- Node (13.12.0)
- NPM (6.14.4) or Yarn (1.22.4)
- MongoDB (4.2.0)

Python packages required:
- Navigate to /db_utils directory and run the command:
    `pip install -r requirements.txt`
- Navigate to /db_utils directory and run the command:
    `pip install -r requirements.txt`

Instructions to run the web application:
- Clone this repository
- Enter required credentials and configuration info for mongoDB connection in /web/config/config.js
- Open command line in the cloned folder
    - To install dependencies, run  npm install or yarn
    - To run the application for development, run  npm run development or yarn development
- Open localhost:3000 in the browser

To start the Recommendation server:
- navigate to ml_recommendtions directory and run recommendations_server.py
    `python recommendations_server.py`
