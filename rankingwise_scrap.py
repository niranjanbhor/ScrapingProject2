import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import pandas as pd
from selenium.common.exceptions import NoSuchElementException, NoSuchFrameException
import csv


def main():
    """defining main function"""
    get_driver()


def get_driver():
    """getting driver"""
    try:
        chromeoptions = webdriver.ChromeOptions()
        chromeoptions.add_argument('--window-size=1920,1080')
        chromeoptions.headless = False
        chromeoptions.add_argument('--no-sandbox')
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chromeoptions)
        get_ranking_wise_url(driver)
    except NoSuchElementException:
        pass


def get_ranking_wise_url(driver):
    """Getting url for scrapping ranking wise player data"""
    try:
        driver.get("https://247sports.com/college/football/recruiting/")
        time.sleep(5)
        driver.implicitly_wait(10)
        driver.find_element(By.XPATH, "//a[text()='Player Rankings']").click()
        driver.find_element(By.XPATH, "/html/body/section[1]/section/div/section/header/div/div[1]/a[1]").click()
        driver.find_element(By.XPATH,
                            "/html/body/section[1]/section/div/section/header/div/div[1]/div[1]/ul/li[5]/a").click()
        driver.find_element(By.XPATH, "/html/body/section[1]/section/div/section/header/div/div[1]/a[2]").click()
        driver.find_element(By.XPATH,
                            "/html/body/section[1]/section/div/section/header/div/div[1]/div[2]/ul/li[2]/a").click()
        driver.find_element(By.XPATH, "/html/body/section[1]/section/div/section/section/div/div[1]/a[1]").click()
        link = driver.find_elements(By.XPATH,
                                    "/html/body/section[1]/section/div/section/section/div/ul/li[*]/div[1]/div[3]/a")
        templist = []
        for i in range(0, 80):
            link = driver.find_elements(By.XPATH,
                                        "/html/body/section[1]/section/div/section/section/div/ul/li[*]/div[1]/div[3]/a")
            print(len(link))
            driver.implicitly_wait(10)
            driver.execute_script("arguments[0].click();", link[i])
            time.sleep(2)
            data = ranking_player_attributes(driver)
            # store data after every loop cycle
            with open('Ranking_wise.csv', mode='a', encoding='utf-8', newline='') as f:
                write_object = csv.DictWriter(f, fieldnames=list(data.keys()))
                write_object.writerow(data)
            driver.back()
            try:
                driver.find_element(By.XPATH,
                                    "/html/body/section[1]/section/div/section/header/div/div[1]/a[2]").click()
                driver.find_element(By.XPATH,
                                    "/html/body/section[1]/section/div/section/header/div/div[1]/div[2]/ul/li[2]/a").click()
                driver.find_element(By.XPATH,
                                    "/html/body/section[1]/section/div/section/section/div/div[1]/a[1]").click()
            except NoSuchElementException:
                pass

        # df = pd.DataFrame(templist)
        # df.to_csv('Ranking_wise.csv', mode='a', index=False, encoding='utf-8', header=True)
        driver.quit()
    except NoSuchElementException:
        pass
    except IndexError:
        pass


def ranking_player_attributes(driver):
    """defining function to getting player attributes"""
    data = {}
    name_data = []
    try:
        try:
            name = driver.find_elements(By.XPATH, "/html/body/section[1]/section/div/section/header/div[1]/h1")
            name_data = [p.text for p in name]
            print(name_data)
            time.sleep(5)
        except NoSuchElementException:
            pass

        '''image scraping'''
        image_data = []
        try:
            image = driver.find_elements(By.XPATH,
                                         "/html/body/section[1]/section/div/section/header/div[1]/div[1]/div/img")
            image_data = [p.get_attribute('src') for p in image]
            print(image_data)
            time.sleep(5)
        except NoSuchElementException:
            pass

        '''Prospect data scraping'''
        prospect_info_data = []
        try:
            prospect_info = driver.find_elements(By.XPATH,
                                                 "/html/body/section[1]/section/div/section/header/div[1]/ul[1]/li[*]/span[2]")
            prospect_info_data = [p.text for p in prospect_info]
            print(prospect_info_data)
            time.sleep(5)
        except NoSuchElementException:
            pass

        '''School data scraping'''
        try:
            junior_college = driver.find_element(By.XPATH,
                                                 "/html/body/section[1]/section/div/section/header/div[1]/ul[3]/li[1]/div/span[2]").text

            school = driver.find_elements(By.XPATH,
                                          "/html/body/section[1]/section/div/section/header/div[1]/ul[3]/li[*]/span[2]")
            school_data = [p.text for p in school]
            school_data.insert(0, junior_college)
            print(school_data)
            if len(school_data) != 3:
                school_data = ['null', 'null', 'null']

        except NoSuchElementException:
            school = driver.find_elements(By.XPATH,
                                          "/html/body/section[1]/section/div/section/header/div[1]/ul[3]/li[*]/span[2]")
            school_data = [p.text for p in school]
            print(school_data)
            time.sleep(5)
            if len(school_data) != 3:
                school_data = ['null', 'null', 'null']

        """ Twitter account details scrapping"""
        twitter_data = {}
        try:
            driver.switch_to.frame('twitter-widget-0')
            twitter = driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div/div[1]/a/div/a/span").text
            profile = list(twitter.split(' '))
            twitter_data = profile[2]
            print(twitter_data)
            time.sleep(5)
            driver.refresh()
        except NoSuchElementException:
            pass
        except (IndexError, NoSuchFrameException):
            pass

        '''offers scraping'''
        try:
            element1 = driver.find_element(By.XPATH,
                                           "//*[@id='page-content']/div[2]/section/header/div[2]/section[2]/div[2]/a")
            driver.execute_script("arguments[0].click();", element1)
            offers = driver.find_element(By.XPATH,
                                         "/html/body/section[1]/section/div[2]/section/section/header/div/span[1]")
            offers_data = [offers.get_attribute('textContent')]
            print(offers_data)
        except NoSuchElementException:
            offers = driver.find_element(By.XPATH,
                                         "/html/body/section[1]/section/div[2]/section/section/header/div/span[1]")
            offers_data = [offers.get_attribute('textContent')]
            print(offers_data)

        '''scrapping data for players who committed and for them scraping recruited by data'''
        recruited_by = []
        commit_status = []
        try:
            commit = driver.find_elements(By.XPATH,
                                          "/html/body/section[1]/section/div/section/section/div/ul/li[1]/span")
            t_name = driver.find_element(By.XPATH,
                                         "/html/body/section[1]/section/div/section/section/div/ul/li[1]/div[1]/a[1]").text

            for c in commit:
                if c.text == 'Enrolled' or 'Signed' or 'Cool' or 'Warmer':
                    commit_status = {c.text: t_name}
                    print(commit_status)
                    recruited = driver.find_elements(By.XPATH,
                                                     "/html/body/section[1]/section/div/section/section/div/ul/li[1]/div[3]/div[*]/a")
                    recruited_by = [p.text for p in recruited]
                    if 0 == len(recruited_by):
                        recruited_by = ['No Recruited By data']
                else:
                    recruited_by = ['']
                    commit_status = ['']
            print(recruited_by)
            time.sleep(5)
        except NoSuchElementException:
            pass

        '''college complete details'''
        college = {}
        try:
            web_open_wait = 5
            time.sleep(web_open_wait)
            element = driver.find_element(By.XPATH,
                                          "/html/body/section[1]/section/div[2]/section/section/footer/a[1]")
            driver.execute_script("arguments[0].click();", element)
            time.sleep(5)
            college_logo = driver.find_elements(By.XPATH,
                                                "//*[@id='page-content']/div/section[2]/section/section/ul/li[*]/img")
            college_name = driver.find_elements(By.XPATH,
                                                "//ul[@class='recruit-interest-index_lst']/li//div[@class='first_blk']/a[1]")
            current_scroll_position, new_height = 0, 1
            speed = 3
            while current_scroll_position <= new_height:
                current_scroll_position += speed
                driver.execute_script("window.scrollTo(0, {});".format(current_scroll_position))
                new_height = driver.execute_script("return document.body.scrollHeight")

            college_logo_data = [p.get_attribute('src') for p in college_logo]
            time.sleep(5)
            college_name_data = [p.text for p in college_name]
            time.sleep(5)
            college = {college_name_data[i]: college_logo_data[i] for i in range(len(college_name_data))}
            print(college)
            driver.back()
            driver.back()
        except NoSuchElementException:
            pass

        data = {'Name': name_data[0], 'Image': image_data[0],
                'Position': prospect_info_data[0], 'Height': prospect_info_data[1], 'Weight': prospect_info_data[2],
                'School': school_data[0], 'City': school_data[1], 'Class': school_data[2],
                'Offers': offers_data[0],
                'College Details': college, 'Commit Status': commit_status, 'Recruited By': recruited_by,
                'Twitter_profile': {twitter_data}}

    except NoSuchElementException:
        pass
    return data


# Calling main function


if __name__ == "__main__":
    main()
