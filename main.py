from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import time
import selenium
import re

PATH = "C:\Program Files (x86)\chromedriver.exe"
driver = webdriver.Chrome(PATH)
driver.get("https://www.educationperfect.com/app/#/dashboard")


username = ''
password = ''
driver.maximize_window()

print(F"Type 'help' for a list of commands")
def login():
    try:
        driver.find_element_by_id("login-username").send_keys(username)
        driver.find_element_by_id("login-password").send_keys(password)
        driver.find_element_by_id("login-submit-button").click()
        print("Logged In")
    except selenium.common.exceptions.NoSuchElementException:
        print("Wait for login screen to appear on screen")
translations = {}



def extract_data():
    infinity_button = driver.find_element_by_xpath('//*[@id="number-of-questions-selector"]/li[5]/div')
    scroll_bar = driver.find_element_by_xpath('//*[@id="preview-grid-container"]/div[2]')
    word_count = str(driver.find_element_by_id('word-count').text).split(' ')[0]
    #print(word_count)
    ActionChains(driver).move_to_element(driver.find_elements_by_class_name('targetLanguage')[1])
    start_button = driver.find_element_by_id('start-button-main-content')
    quiz_button = driver.find_element_by_xpath('//*[@id="test-mode-options"]/li[2]')

    for i in range(0, int(word_count)):
        scroll_to = driver.find_elements_by_class_name('targetLanguage')[i]
        driver.execute_script("arguments[0].scrollIntoView();",scroll_to)
        word = str(driver.find_elements_by_class_name('targetLanguage')[i].text)
        answer = str(driver.find_elements_by_class_name('baseLanguage')[i].text)
        translations.update({word.replace(';', ','):answer.split(';')[0]})
        translations.update({answer.replace(';', ','):word.split(";")[0]})
    ActionChains(driver).move_to_element(quiz_button).perform()
    driver.execute_script("arguments[0].scrollIntoView();", infinity_button)
    time.sleep(0.2)
    infinity_button.click()
    #print(translations)
    time.sleep(0.2)
    print("answers got")
    start_button.click()
    time.sleep(1)
    print("Starting bot")
    start_answers()


def start_answers():
    try:
        while True:
            question_text = driver.find_element_by_id('question-text').text
            if question_text in translations:
                answer_text = translations.get(question_text)
                #print(answer_text)
                answer_input = driver.find_element_by_id("answer-text")
                ActionChains(driver).move_to_element(answer_input).send_keys(answer_text).perform()
                driver.find_element_by_id('submit-button').click()
            else:
                driver.find_element_by_id('hint-button').click()
                time.sleep(0.2)
                correct_answer = driver.find_element_by_id('correct-answer-field').text
                #print(question_text)
                #print(correct_answer)
                translations.update({question_text:correct_answer})
                driver.find_element_by_xpath('//*[@id="viewport"]/div[1]/div/div/div[2]/button').click()

    except selenium.common.exceptions.ElementClickInterceptedException:
        pass
        try:
            time.sleep(0.2)
            should_text = driver.find_element_by_id('question-text').text
            should_answer =  str(driver.find_element_by_id('correct-answer-field').text)
            translations.update({should_text:should_answer.split(',')[0]})
            translations.update({should_answer:should_text})
            time.sleep(0.2)
            driver.find_element_by_id('continue-button').click()
            time.sleep(0.2)
            start_answers()
            print(f"{should_text} : {should_answer.split(',')[0]}")
        except selenium.common.exceptions.NoSuchElementException:
            pass

    except selenium.common.exceptions.NoSuchElementException:
        print("List Closed")

def add_to_translation():
    translation = input('Q:A: ')
    add_question = translation.split(':')[0]
    add_answer = translation.split(':')[1]
    translations.update({add_question:add_answer})




while True:
    command = input("> ").lower()
    if command == 'login':
        login()
    elif command == 'data':
        extract_data()
    elif command == 'start':
        print("Starting Bot")
        start_answers()
    elif command == 'reset':
        translations = {}
        print("Reset")
    elif command == 'quit':
        driver.close()
        break
    elif command == 'add':
        add_to_translation()
    elif command == 'help':
        print(
        '''
        login - To login
        data - To extract data
        reset - To reset translation dictionary
        add - To add to translation dictionary
        quit - To quit
        ''')
    else:
        print(f"Unknown command, type 'help' for a list of commands")

  
