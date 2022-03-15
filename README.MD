# MS LMS

### Creator [Raphael Katana]('https://github.com/users/RKatana')
An open sourece Moringa school learning management system

## Project Board 
---
Check out the project board for tasks and features on [Pivotal Tracker]('https://www.pivotaltracker.com/n/projects/2558537')

<img src="./media/images/pivotal-tracker.png" width="90%" alt="Screenshot Pivotal tracker">


## Technologies and Packages Used
---
- Python
- Django
- Pillow
- Pipenv
- SQL
- Whitenoise
- Cloudinary
- Django Embed Video
- Django Registration
- Django braces


## Set up and Installation
- `git clone git@github.com:RKatana/ms-lms.git`
- `cd ms-lms; pipenv shell; pipenv install` #This commands basically navigates you to the cloned repo, creates a virtual environment using pipenv and the installs the dependencies from *Pipfile.lock*
- `touch .env` #create a dotenv file and then configure it to match the *.env-sample* file 
- `source .env` #source the .env to load the environment variables
- `make server` #run the development server and open the link in your browser

#### Installation Assumptions
- The above instructions assumes you are using a Unix based OS.
- I also assume that you have pipenv installed.

### App Screenshots
---
<p><img src="./media/images/ms-register.png" width="90%" alt="Screenshot Pivotal tracker"></p>
<p><img src="./media/images/ms-login.png" width="90%" alt="Screenshot Pivotal tracker"></p>
<p><img src="./media/images/ms-admin.png" width="90%" alt="Screenshot Pivotal tracker"></p>
<p><img src="./media/images/ms-student.png" width="90%" alt="Screenshot Pivotal tracker"></p>
<p><img src="./media/images/admin-login.png" width="90%" alt="Screenshot Pivotal tracker"></p>
<p><img src="./media/images/ms-admin-panel.png" width="90%" alt="Screenshot Pivotal tracker"></p>

### Licence: [BSD]('./LICENSE')