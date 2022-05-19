from lib2to3.pgen2 import driver
from tkinter import N
from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from colorama import Fore
import time
import os
import random
import instaloader
import ast

os.system('cls')
print(Fore.YELLOW + ' Only for Windows users!' + Fore.RESET)


class Bot:
    path = Service('geckodriver.exe')
    driver = webdriver.Firefox(service=path)
    driver.get('https://www.instagram.com/accounts/login/')

    def login_instaloader(self, username, password):
        try:
            L = instaloader.Instaloader()
            L.login(username, password)
            print(Fore.GREEN + 'Login to instaloader successful' + Fore.RESET)
            print('opend users.txt')
            with open('users.txt', 'r') as users:
                users = users.read().split('\n')
                print(users)
                if users is not None or users is not '':
                    for user in users:
                        print(user)
                        print(f'get to {user} profile')
                        profile = instaloader.Profile.from_username(
                            L.context, user)
                        count = 0
                        print(f'Extracting followers from {user} followers')
                        for follower in profile.get_followers():
                            with open('targets.txt', 'r') as targets:
                                targets = targets.read().split('\n')
                                if targets is not None or targets is not '':
                                    if follower.username not in targets:
                                        follower_count = follower.get_followers().count
                                        if 100 < int(follower_count) < 10000:
                                            with open('targets.txt', 'a') as targets:
                                                targets.write(
                                                    follower.username + '\n')
                                                count += 1
                                                print(
                                                    Fore.GREEN + 'Added ' + follower.username + ' to targets.txt' + Fore.RESET)
                                                if count == 2:
                                                    print('Extract Done!')
                                                    break

                                        else:
                                            print(
                                                Fore.RED + 'Skipped ' + follower.username + ' because of follower count' + Fore.RESET)
                                    else:
                                        print(Fore.RED + 'Skipped ' + follower.username +
                                              ' because it is already in targets.txt' + Fore.RESET)
                                else:
                                    with open('targets.txt', 'a') as targets:
                                        targets.write('username' + '\n')
                        return True
                else:
                    print('users.txt is empty')
                    return False
        except:
            print(instaloader.exceptions)
            return False

    def login_instagram(self, username, password):
        self.driver.get('https://www.instagram.com/accounts/login/')
        time.sleep(2)
        try:
            username_field = self.driver.find_element(
                By.XPATH, '//input[@name="username"]')
            username_field.send_keys(username)
        except:
            print(f'{Fore.RED}Username field not found{Fore.RESET}')
        try:
            password_field = self.driver.find_element(
                By.XPATH, '//input[@name="password"]')
            password_field.send_keys(password)
            password_field.send_keys(Keys.ENTER)
            time.sleep(10)
            self.driver.get(f'https://www.instagram.com/{username}/')
            time.sleep(5)
        except:
            print(f'{Fore.RED}Password field not found{Fore.RESET}')

    def get_to_post(self):
        with open('post_links.txt', 'r') as post_links:
            post_links = post_links.read().split('\n')
            for post in post_links:
                print(f'get to {post}')
                self.driver.get(post)
                time.sleep(5)
                with open('targets.txt', 'r') as targets:
                    targets = targets.read().split('\n')
                    target_list = []
                    if targets is not None or targets is not '':
                        for target in targets:
                            with open('target_done.txt', 'r') as target_done:
                                target_done = target_done.read().split('\n')
                                if target_done is not None or target_done is not '':
                                    if target in target_done:
                                        print(
                                            Fore.RED + f'{target} is already in target_done.txt' + Fore.RESET)
                                        with open('targets.txt', 'r') as target_delete:
                                            lines = target_delete.readlines()
                                            with open('targets.txt', 'w') as target_delete:
                                                for line in lines:
                                                    if line.strip('\n') != target:
                                                        target_delete.write(line)
                                    else:
                                        target_list.append(target)
                                        if len(target_list) == 2:
                                            break
                                else:
                                    print('target_done.txt is empty')
                        for target_user in target_list:
                            try:
                                self.driver.find_element(
                                    By.XPATH, '/html/body/div[1]/section/main/div/div[1]/article/div/div[2]/div/div[2]/section[1]/span[2]/button').click()
                                time.sleep(5)
                            except:
                                print('No send button')
                                continue

                            try:
                                query_box = self.driver.find_element(
                                    By.XPATH, '//input[@name="queryBox"]')
                                query_box.send_keys(target_user)
                                time.sleep(20)
                            except:
                                print('no query box')
                                continue
                            try:
                                self.driver.find_element(
                                    By.XPATH, '/html/body/div[5]/div/div/div[2]/div[2]/div[1]/div/div[2]/div[1]/div/div').click()
                                time.sleep(2)
                                # if check_username.text == target_user:
                                #     check_username.click()
                                #     time.sleep(5)
                                # else:
                                #     check_username.click()
                                #     time.sleep(5)
                            except:
                                print('no check username')
                                continue
                            try:
                                self.driver.find_element(
                                    By.XPATH, '/html/body/div[5]/div/div/div[2]/div[4]/button').click()
                                time.sleep(3)
                            except:
                                print('no submit button')
                                continue
                            with open('target_done.txt', 'a') as target_done:
                                target_done.write(
                                    target_user + '\n')
                                print(
                                    Fore.GREEN + f'Added {target_user} to target_done.txt' + Fore.RESET)
                                random_time = random.randint(
                                    120, 180)
                                print(
                                    'send post to ' + target_user)
                                print(
                                    'Sleeping for ' + str(random_time) + ' seconds')
                                time.sleep(random_time)

                    else:
                        print('targets.txt is empty')
                        break

    def logout_instagram(self):
        print('logout')
        self.driver.get('https://www.instagram.com/accounts/logout/')
        time.sleep(2)

    def start_bot(self):
        with open('accounts.txt', 'r') as accounts:
            accounts = accounts.read().split('-')
            for account in accounts:
                new_account = ast.literal_eval(account)
                username = new_account.get('username')
                password = new_account.get('password')
                # self.login_instaloader(username=username, password=password)
                if self.login_instaloader(username=username, password=password):
                    self.login_instagram(username, password)
                    self.get_to_post()
                    self.logout_instagram()
                else:
                    print(
                        f'{Fore.RED}{username}: Login to instaloader failed{Fore.RESET}')
                    continue


bot = Bot()
bot.start_bot()
