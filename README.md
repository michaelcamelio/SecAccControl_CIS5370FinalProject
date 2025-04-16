# Secure Access Control for Environmental Sensors
Principles of Cybersecurity (CIS 5370) Final Project for Michael Camelio, Carlos Amasifuen, Isha Bhardwaj at Florida International University

## Requirements
- [Python 3.11.3 or greater](https://www.python.org/downloads/) - Our project runs on Python.
- Pip - Pip is used to install packages for our requirements.txt

## How to Run the Project

1. Clone repository:
   ```bash
    git clone https://github.com/michaelcamelio/SecAccControl_CIS5370FinalProject.git
   ```
   
2. Navigate to the project folder:
   ```bash
   cd SecAccControl_CIS5370FinalProject
   ```
3. Install the packages
   ```bash
   pip install -r requirements.txt
   ```
4. Virtual Environment (Optional)
   - **Create a Virtual Enviroment (Windows)**
     ```bash
     python -m venv venv
     ```
   - **Activate the Enviroment (Windows)**
      ```bash
      .\venv\Scripts\Activate.ps1
      ```
   - **Create a Virtual Enviroment (Mac OS)**
     ```bash
     python3 -m venv venv
     ``` 
   - **Activate the Enviroment (Mac OS)**
      ```bash
      source venv/bin/activate
      ``` 


5. Run the project (main.py)
   Navigate to the app folder and run the main.py script.
   ```bash
   cd app
   python main.py
   ```
   Your terminal should output:
   ```bash
   Running on http://<ip address>:<port>
   ```
   Visit the url to view the project running in your browser.
