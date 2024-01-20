from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time


chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option("detach", True)


class InstaLogin:
    def __init__(self, user_mail, user_pass):
        """takes user mail and password to logged in the website."""

        self.__user_mail = user_mail
        self.__user_password = user_pass
        self.__account_search = None
        self.__follow_act = None
        self.__unfollow_act = None
        self.__follow_max_limit = None
        self.__unfollow_max_limit = None
        self.__person_to_unfollow = None
        self.__total_following = None
        self.__following_list = None

        self.__driver = webdriver.Chrome(chrome_options)
        self.__driver.get("https://www.instagram.com/")
        time.sleep(3)

        email_fill = self.__driver.find_element(By.XPATH, '//*[@id="loginForm"]/div/div[1]/div/label/input')
        email_fill.click()
        time.sleep(2)
        email_fill.send_keys(self.__user_mail, Keys.TAB)
        time.sleep(2)

        pass_fill = self.__driver.find_element(By.XPATH, '//*[@id="loginForm"]/div/div[2]/div/label/input')
        pass_fill.send_keys(self.__user_password)
        time.sleep(2)
        pass_fill.submit()

        print("login successful.")

    def search_account(self, account_to_search, follow_searched_act: bool = False, unfollow_searched_act: bool = False):
        """it will open the first account appear with same name in search box.
         By default, follow and unfollow_searched_act will be False, if selected True, account will be followed
         or unfollowed accordingly. note that you can't unfollow a person you're not following currently.
        """

        self.__account_search = account_to_search
        self.__follow_act = follow_searched_act
        self.__unfollow_act = unfollow_searched_act

        try:
            time.sleep(8)
            search_button = self.__driver.find_element(By.XPATH, '/html/body/div[2]/div/div/div[2]/div/div/div/div[1]/div[1]/div[1]/div/div/div/div/div[2]/div[2]/span/div/a/div')
            time.sleep(5)
            search_button.click()
        except Exception as error:
            print(error)
        else:
            time.sleep(5)
            search_account = self.__driver.find_element(By.XPATH, '/html/body/div[2]/div/div/div[2]/div/div/div/div[1]/div[1]/div[1]/div/div/div[2]/div/div/div[2]/div/div/div[1]/div/div/input')
            time.sleep(5)
            search_account.click()
            time.sleep(3)

            search_account.send_keys(self.__account_search)
            time.sleep(3)
            search_account.send_keys(Keys.TAB, Keys.TAB, Keys.ENTER)    # fill account name in search box and hit enter

            print(f"search {self.__account_search} successful.")
            time.sleep(5)

        if self.__follow_act or self.__unfollow_act:
            already_following = self.__driver.find_element(By.XPATH, '/html/body/div[2]/div/div/div[2]/div/div/div/div[1]/div[1]/div[2]/div[2]/section/main/div/header/section/div[1]/div[2]/div/div[1]/button/div/div[1]')

            if already_following.text != "Follow":
                print(f"you already followed {self.__account_search} account.")

                if self.__unfollow_act:  # if user want to unfollow an account from account handle.
                    already_following.click()
                    time.sleep(2)

                    try:
                        time.sleep(3)  # pop will appear where we have to click on unfollow
                        popup = WebDriverWait(self.__driver, 10).until(
                            EC.presence_of_element_located((By.XPATH, "//div[@role='dialog']"))
                        )

                        unfollow_button = WebDriverWait(popup, 10).until(
                            EC.presence_of_element_located((By.XPATH, "//span[text()='Unfollow']"))
                        )
                        unfollow_button.click()
                        time.sleep(2)

                    except Exception as e:
                        print(e)
                        print("code is not detecting path. code need improvement.")

                    print(f"you choose to unfollow {self.__account_search}")
                    time.sleep(3)

            else:
                time.sleep(3)
                follow = self.__driver.find_element(By.XPATH, '/html/body/div[2]/div/div/div[2]/div/div/div/div[1]/div[1]/div[2]/div[2]/section/main/div/header/section/div[1]/div[2]/div/div[1]/button')
                time.sleep(5)
                follow.click()
                time.sleep(5)
                print(f"you choose to follow '{self.__account_search}'")

    def start_following(self, one_time_limit: int):
        """check followers of an account inside the page you've searched and start following. you can set following
        limit. maximum one time limit of following is 25.
        note: you should be inside the account whose followers you want to follow"""

        self.__follow_max_limit = int(one_time_limit)

        if self.__follow_max_limit < 25:
            self.__follow_max_limit = int(one_time_limit)
        else:
            self.__follow_max_limit = 25
            print("only 25 person's can be followed in one time.")

        time.sleep(5)
        followers_of_account = self.__driver.find_element(By.XPATH, '/html/body/div[2]/div/div/div[2]/div/div/div/div[1]/div[1]/div[2]/div[2]/section/main/div/header/section/ul/li[2]/a')
        time.sleep(5)
        followers_of_account.click()

        try:
            time.sleep(3)

            for i in range(1, self.__follow_max_limit + 1):

                time.sleep(3)
                person_already_followed = self.__driver.find_element(By.XPATH,f'/html/body/div[5]/div[1]/div/div[2]/div/div/div/div/div[2]/div/div/div[2]/div[2]/div/div[{i}]/div/div/div/div[3]/div/button/div/div')
                if person_already_followed.text != "Follow":
                    print("already_following:", person_already_followed.text)
                    if i > 1:
                        i -= 1
                    continue

                time.sleep(3)
                start_following_list = self.__driver.find_element(By.XPATH, f'/html/body/div[5]/div[1]/div/div[2]/div/div/div/div/div[2]/div/div/div[2]/div[2]/div/div[{i}]/div/div/div/div[3]/div/button')
                time.sleep(2)
                start_following_list.click()
                print(f"started following someone no.{i}")
                time.sleep(2)

        except Exception as e:
            print("there is some issue, can't continue following.")
            print(e)
        else:
            WebDriverWait(self.__driver, 10).until(EC.element_to_be_clickable(
                (By.XPATH, "/html/body/div[5]/div[1]/div/div[2]/div/div/div/div/div[2]/div/div/div[1]/div/div[3]/div/button/div"))).click()

    def my_profile_page(self):
        """this will bring you to your profile page and returns your total following."""

        time.sleep(3)
        profile = self.__driver.find_element(By.XPATH, '/html/body/div[2]/div/div/div[2]/div/div/div/div[1]/div[1]/div[1]/div/div/div/div/div[2]/div[8]/div/span/div/a/div')
        time.sleep(3)
        profile.click()
        print("you are now in your profile page")
        time.sleep(3)

        total_following = self.__driver.find_element(By.XPATH,'/html/body/div[2]/div/div/div[2]/div/div/div/div[1]/div[1]/div[2]/div[2]/section/main/div/header/section/ul/li[3]/a/span/span')
        time.sleep(5)
        print(f"you are following: {total_following.text} person/persons.")
        return int(total_following.text)

    def following_names(self) -> list:
        """this will open profile page and then following list. finally returns a list of followings"""

        time.sleep(5)
        self.__total_following = self.my_profile_page()

        time.sleep(3)
        my_following = self.__driver.find_element(By.XPATH, '/html/body/div[2]/div/div/div[2]/div/div/div/div[1]/div[1]/div[2]/div[2]/section/main/div/header/section/ul/li[3]/a')
        time.sleep(2)
        my_following.click()
        time.sleep(2)

        self.__following_list = []

        for i in range(1, self.__total_following):
            time.sleep(2)
            person_name = self.__driver.find_element(By.XPATH,f'/html/body/div[5]/div[1]/div/div[2]/div/div/div/div/div[2]/div/div/div[4]/div[1]/div/div[{i}]/div/div/div/div[2]/div/div/div/div/div/a/div/div')
            time.sleep(3)
            self.__following_list.append(person_name.text)
            print(person_name.text)

        WebDriverWait(self.__driver, 10).until(EC.element_to_be_clickable(
            (By.XPATH, "/html/body/div[5]/div[1]/div/div[2]/div/div/div/div/div[2]/div/div/div[1]/div/div[3]/div/button/div"))).click()

        return self.__following_list

    def unfollow_accounts(self, max_limit: int):
        """unfollow those whom you're following. maximum limit should not be above the current following."""

        self.__unfollow_max_limit = int(max_limit)

        time.sleep(10)
        self.__total_following = self.my_profile_page()

        if int(self.__total_following) < self.__unfollow_max_limit:
            print(f"you are currently following {self.__total_following} persons. You can't unfollow {self.__unfollow_max_limit}")

        else:
            time.sleep(5)
            my_following = self.__driver.find_element(By.XPATH, '/html/body/div[2]/div/div/div[2]/div/div/div/div[1]/div[1]/div[2]/div[2]/section/main/div/header/section/ul/li[3]/a')
            time.sleep(3)
            my_following.click()
            time.sleep(5)

            for i in range(1, self.__unfollow_max_limit + 1):

                time.sleep(2)
                person_list = self.__driver.find_element(By.XPATH, f'/html/body/div[5]/div[1]/div/div[2]/div/div/div/div/div[2]/div/div/div[4]/div[1]/div/div[{i}]/div/div/div/div[3]')
                time.sleep(3)
                person_list.click()
                time.sleep(3)

                WebDriverWait(self.__driver, 10).until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[6]/div[1]/div/div[2]/div/div/div/div/div/div/button[1]"))).click()
                time.sleep(3)
                print(f"unfollowing person no.{i}")

            WebDriverWait(self.__driver, 10).until(EC.element_to_be_clickable(
                (By.XPATH, "/html/body/div[5]/div[1]/div/div[2]/div/div/div/div/div[2]/div/div/div[1]/div/div[3]/div/button/div"))).click()

    def unfollow_a_person(self, person: list):
        """take list as an input. open profile page and then following tab. search for the names provided
        by user and remove person from following"""

        self.__person_to_unfollow = person
        time.sleep(5)
        self.__total_following = self.my_profile_page()

        time.sleep(3)
        my_following = self.__driver.find_element(By.XPATH, '/html/body/div[2]/div/div/div[2]/div/div/div/div[1]/div[1]/div[2]/div[2]/section/main/div/header/section/ul/li[3]/a')
        time.sleep(3)
        my_following.click()
        time.sleep(3)

        for i in range(1, self.__total_following):

            if len(self.__person_to_unfollow) == 0:
                break

            else:
                time.sleep(2)
                person_name = self.__driver.find_element(By.XPATH, f'/html/body/div[5]/div[1]/div/div[2]/div/div/div/div/div[2]/div/div/div[4]/div[1]/div/div[{i}]/div/div/div/div[2]/div/div/div/div/div/a/div/div')
                time.sleep(3)
                print(person_name.text)

                if person_name.text in self.__person_to_unfollow:

                    time.sleep(3)
                    person_list = self.__driver.find_element(By.XPATH, f'/html/body/div[5]/div[1]/div/div[2]/div/div/div/div/div[2]/div/div/div[4]/div[1]/div/div[{i}]/div/div/div/div[3]')
                    time.sleep(3)
                    person_list.click()
                    time.sleep(3)

                    WebDriverWait(self.__driver, 10).until(EC.element_to_be_clickable(
                        (By.XPATH, "/html/body/div[6]/div[1]/div/div[2]/div/div/div/div/div/div/button[1]"))).click()
                    time.sleep(3)

                    print(f"unfollowing person {person_name.text}")
                    self.__person_to_unfollow.remove(person_name.text)

                else:
                    print(f"{person_name.text} is not the person you want to unfollow.")

        print(f"{self.__person_to_unfollow} not found in your following.")
        try:
            WebDriverWait(self.__driver, 10).until(EC.element_to_be_clickable(
                (By.XPATH, "/html/body/div[5]/div[1]/div/div[2]/div/div/div/div/div[2]/div/div/div[1]/div/div[3]/div/button/div"))).click()
        except:
            pass