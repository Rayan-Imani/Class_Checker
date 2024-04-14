from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
import time
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import sendgrid
from sendgrid.helpers.mail import Mail, Email, To, Content
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait



# Setting up Email credentials
sender_email = "testiclops11@gmail.com"
receiver_email = "rayanimani@gmail.com"
password = "JellyFutbol11!"  # The password for your email account
smtp_server = "smtp.gmail.com"
smtp_port = 587  # For Gmail 


#send email function
def send_email(subject, body):
    sg = sendgrid.SendGridAPIClient('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')
    from_email = Email("rayanimani@gmail.com")  # The SendGrid account email
    to_email = To("rayanimani@gmail.com")  # Where you want to send the email
    content = Content("text/plain", body)
    mail = Mail(from_email, to_email, subject, content)
    response = sg.client.mail.send.post(request_body=mail.get())
    if response.status_code == 202:
        print("Email sent successfully")
    else:
        print(f"Failed to send email, status code: {response.status_code}")

        



courseID = ["cs4376", "cs4391", "cs4389", "cs4371", "cs4352"]

chrome_driver_path = r"C:\Users\rayan\OneDrive\Desktop\chromedriver-win64\chromedriver.exe"


options = Options()
options.headless = True
options.add_argument('--ignore-certificate-errors')
options.add_argument('--allow-insecure-localhost')
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
    courses = WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.XPATH, f"//tr[starts-with(@data-id, '{course}')]"))
    )
    for class_row in courses:
        try:
            status_elements = class_row.find_elements(By.CLASS_NAME, 'section-closed')
            course_name_element = class_row.find_elements(By.TAG_NAME, "td")[3]
            course_name = course_name_element.text
            if status_elements and status_elements[0].text.lower() == 'full':
                print(f"The class {course_name} is full")
            else:
                print(f"Class {course_name} is open!")
                send_email("Class open bitch", f"Class {course} {course_name} is now open you pussy bitch")
        except Exception as e:
            print(f"Error processing row: {e}")


driver.quit()

