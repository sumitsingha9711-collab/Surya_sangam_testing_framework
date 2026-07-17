from pages.contact_form_component import ContactFormComponent
from utils.driver_factory import DriverFactory
from selenium.common.exceptions import TimeoutException, WebDriverException

URL = "https://www.suryasangam.com/"

def main():
    driver = None
    try:
        driver = DriverFactory.create_chrome_driver()
        driver.get(URL)
        form = ContactFormComponent(driver)
        try:
            f = form.get_form()
            print('Form found:', bool(f))
        except TimeoutException as e:
            print('Timeout waiting for form:', e)
        try:
            btn = form.get_submit_button()
            print('Submit button found:', bool(btn))
        except TimeoutException as e:
            print('Timeout waiting for submit button:', e)
        print('Page title:', driver.title)
        print('Body text sample:', driver.find_element('tag name','body').text[:200])
    except WebDriverException as e:
        print('WebDriver error:', e)
    finally:
        if driver:
            driver.quit()

if __name__ == '__main__':
    main()
