Contact +2349061296934 via whatsapp for any further issue

# Audience

This documentation is intended for developers or individuals aiming to utilize this API for development or personal purposes.

## Getting Started on Your Local Machine

### REQUREMENTS AND RECOMMENDATIONS

**Note:** All required dependencies are listed in `requirements.txt`, which is located at the root directory (`/TODO/requirements.txt`), use this comand to install all requirement `pip install -r requirements.txt`. To ensure clarity, the following prerequisites must be met to successfully run the application on your local machine:

1. **Python**

   - It is recommended to install the slightly older stable version of Python (version 3.12.7) using [this link](https://www.python.org/downloads/release/python-3127/) to avoid potential errors during the installation of `mysqlclient` using `pip install mysqlclient`. The current version of`mysqlclient`may lack pre-compiled`.whl` support for the latest Python releases.

   - Ensure to follow the proper Python installation steps.

2. **Pillow**

   - The latest version of `Pillow` is fully supported and compatible.

3. **Django**

   - The current version of Django works efficiently with the project setup.

4. **Django Rest Framework**

   - As the `API` is built using Django Rest Framework, installing the latest version of Django Rest Framework works fine.

5. **argon2-cffi**
   - The `argon2-cffi` library implements the Argon2 password hashing algorithm, which is essential for secure password hashing. Installing the latest version does not negatively affect this `API`.
   <h2>Installation Guide</h2>
   <ol>
       <li>
           <strong>Download the Project:</strong> Begin by downloading the zip file for this project to your local machine.
       </li>
       <li>
           <strong>Install Python:</strong> Download and install Python from <a href="https://www.python.org/downloads/release/python-3127/">this link</a>. During installation, ensure that the following options are checked:
           <ul>
               <li style="color: red;">
                   <strong>Important:</strong> Check the box to "Add Python to PATH" and select the option to use administrative privileges.
               </li>
           </ul>
           After installation, verify the successful setup by running the following commands in your terminal:
           <ul>
               <li><code>python --version</code> or <code>pip --version</code></li>
           </ul>
           If an error occurs, locate the installed Python path by running:
           <ul>
               <li><code>where python</code> (on Windows) or <code>which python</code> (on macOS/Linux).</li>
           </ul>
           Once located, ensure both <code>pip</code> and <code>python</code> are fully functional.
       </li>
       <li>
           <strong>Install Dependencies:</strong> Use the following commands to install the necessary packages:
           <ul>
               <li><code>pip install pillow</code></li>
               <li><code>pip install django</code></li>
               <li><code>pip install djangorestframework</code></li>
               <li><code>pip install argon2-cffi</code></li>
           </ul>
       </li>
   </ol>

<h2>Database Setup</h2>
<p>
    The project uses a <code>MySQL</code> database. Create your database and update the database configuration in the <code>settings.py</code> file accordingly.
</p>

<h2>Running the Server</h2>
<p>
    Before running the server, prepare and apply the migrations with the following commands:
</p>
<ul>
    <li><code>python manage.py makemigrations</code></li>
    <li><code>python manage.py migrate</code></li>
</ul>
<p>
    Once migrations are complete, start the server with:
    <code>python manage.py runserver</code>.
    The local server will be accessible at <code>https://127.0.0.1:8000</code>.
</p>
