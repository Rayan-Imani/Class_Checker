from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
import time
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import sendgrid
from sendgrid.helpers.mail import Mail, Email, To, Content



# Email Configuration
sender_email = "testiclops11@gmail.com"
receiver_email = "rayanimani@gmail.com"
password = "JellyFutbol11!"  # Consider using an app-specific password for security
smtp_server = "smtp.gmail.com"
smtp_port = 587  # For Gmail with STARTTLS


#send email function
def send_email(subject, body):
    sg = sendgrid.SendGridAPIClient('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')
    from_email = Email("rayanimani@gmail.com")  # Your SendGrid account email
    to_email = To("rayanimani@gmail.com")  # Where you want to send the email
    content = Content("text/plain", body)
    mail = Mail(from_email, to_email, subject, content)
    response = sg.client.mail.send.post(request_body=mail.get())
    if response.status_code == 202:
        print("Email sent successfully")
    else:
        print(f"Failed to send email, status code: {response.status_code}")

        



courseID = ["r-160", "r-180", "r-186", "r-173"]

chrome_driver_path = r"C:\Users\rayan\OneDrive\Desktop\chromedriver-win64\chromedriver.exe"


options = Options()
options.headless = True
options.add_argument('--ignore-certificate-errors')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
options.add_argument('--disable-gpu')



service = Service(chrome_driver_path)
driver = webdriver.Chrome(service = service, options=options)


driver.get('https://coursebook.utdallas.edu/guidedsearch')

time.sleep(2)

dropDownList = driver.find_element(By.ID, 'combobox_cp')
dropdown = Select(dropDownList)
dropdown.select_by_value('cp_cs')

time.sleep(3)

driver.execute_script("do_guided_search();")


time.sleep(3)

for course in courseID:
    class_row = driver.find_element(By.ID, course)
    status_elements = class_row.find_elements(By.CLASS_NAME, 'section-closed')
    course_name_element = class_row.find_elements(By.TAG_NAME, "td")[3]  # Adjust index as necessary
    course_name = course_name_element.text

    if status_elements:
        status = status_elements[0].text
        if status.lower() == 'full':
            print(f"The class {course_name} is full")
        else:
            print(f"Class {course_name} is open!")
            send_email("Class Opened Up fatass", f"The class {course_name} with ID {course} is now open.")
    else: 
        print(f"This class {course_name} is open!")
        send_email("Class Opened up!", f"The class {course_name} with ID {course} is now open.")


driver.quit()

