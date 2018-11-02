# -*- coding: utf-8 -*-
import ConfigParser
import argparse
import msvcrt as m
import sys
from time import sleep

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, WebDriverException
from selenium.webdriver.chrome.options import Options

Config = ConfigParser.ConfigParser()
print "[+] Loading Settings From Config.ini "
Config.read("Config.ini")

"""
Global parameters :
"""
MAX_CLICK_TRIES = Config.getint("Global","max_click_tries")

Element_account_card = Config.get("Elements","account_card")
Element_name = Config.get("Elements","account_name")
Element_Account_description = Config.get("Elements","account_description")
Element_button_my_network = Config.get("Elements","button_my_network")
Element_no_ressult_text = Config.get("Elements","no_ressult_text")
Element_button_in_search_result = Config.get("Elements","button_in_search_result")
Element_button_in_search_result_send = Config.get("Elements","button_in_search_result_send")


def Get_Chrome_Options():
    """
    Load Chrome Option from Config.ini with a pythonic way ;)
    :return:
    """
    chrome_options = Options()
    for Option in ConfigSectionMap("Chrome_Options"):
        if Option in ['log_level']:
            chrome_options.add_argument('log-level={}'.format(ConfigSectionMap("Chrome_Options")['log_level']))
            continue
        # print Option
        if Config.getboolean("Chrome_Options", Option):
            print "Activating Option : {}".format(Option.replace("_", "-"))
            chrome_options.add_argument("--{}".format(Option.replace("_", "-")))
    return chrome_options

def ConfigSectionMap(section):
    dict1 = {}
    options = Config.options(section)
    for option in options:
        try:
            dict1[option] = Config.get(section, option)
            if dict1[option] == -1:
                print ("skip: %s" % option)
        except:
            print("exception on %s!" % option)
            dict1[option] = None
    return dict1

def click(by, what_to_click):
    """
    # this function Click on elements "what_to_click" by the "by" argument
    # and makes MAX_CLICK_TRIES Tries
    #
    # :param by: how to search ... by class or xpath ...
    # :param what_to_click: what to element you want to click
    """
    clicked = False
    tries = 0
    while not clicked and tries < MAX_CLICK_TRIES:
        try:
            if by == "class":
                driver.find_element_by_class_name(what_to_click).click()
            elif by == "xpath":
                driver.find_element_by_xpath(what_to_click).click()
            elif by == "id":
                driver.find_element_by_id(what_to_click).click()
            clicked = True
        except:
            tries += 1
            print "[+] Can't Add  ! (" + str(tries) + "/" + str(MAX_CLICK_TRIES) + ") Trying Again !"
            sleep(1)


def connect_to_linkedin(e, p):
    """
    Establish Connection to linkedin with the given email and password
    :param e: email
    :param p: password
    """
    print "[+] Connecting with ", e, " and pass ", "*" * len(p)
    driver.get("https://www.linkedin.com/")
    driver.find_element_by_xpath('//*[@id="login-email"]').send_keys(e)
    driver.find_element_by_xpath('//*[@id="login-password"]').send_keys(p)
    click("class", "login")


def scrap_accounts(max):
    """
    look for accounts by scrolling till we reach th given max value or more
    :param max: how much you want
    :return: returns All the accounts found
    """
    accounts = []
    while len(accounts) <= max:
        accounts = driver.find_elements_by_class_name(Element_account_card)
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        print "[+] Found ", len(accounts), " Accounts - Scroling ...", "\r",
        sys.stdout.flush()

    return accounts


def connect_to_my_network(accounts):
    """
    Connect to each account given also print the name and info about the accounts
    at the end the results of connecting
    :param accounts:  a list of selinuim objects refers to accounts
    :return:  nothing
    """
    print "[+] Start Connecting ..."
    Connected = 0
    for acc in accounts:
        try:
            name, info = acc.find_element_by_class_name(
                Element_name), acc.find_element_by_class_name(
                Element_Account_description)
            print "[+] Found ", name.text, " | ", info.text, " => Adding ...",
        except UnicodeEncodeError:
            pass
        except NoSuchElementException:
            print "[+] Can't find Name Or info of this Contact !"
        try:
            sleep(0.5)
            acc.find_element_by_class_name(Element_button_my_network).click()
            Connected += 1
        except:
            print "Error :  Next ."
        finally:
            print  "Ok."
    print "[+] Total Connected :", Connected


def connect_by_keywords(keywords, max):
    """
    Search for each keyword on linkedin and add page by page till we reach the max accounts given
    it handles the pop up menu to add notes by skipping it (pressing "Send Now")
    :param keywords:
    :param max:
    :return:
    """
    for word in keywords:
        print "[+] Working On Keyword :", word, " ..."
        page, added = 1, 0
        while added < max:
            print  "[+] Page : ", page, "." * page
            driver.get("https://www.linkedin.com/search/results/people/?keywords=" + word + "&page=" + str(page))
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            sleep(0.2)
            try:
                if "No results found" in driver.find_element_by_class_name(Element_no_ressult_text).text:
                    break
            except NoSuchElementException:
                pass
            Accounts = driver.find_elements_by_class_name(Element_button_in_search_result)
            States = []
            for i in Accounts:
                States += [i.text]
            print "[+] Found ", len(Accounts), " Accounts On this Page "
            print "          - ", str(States.count("Message")), " - ALready Added"
            print "          - ", str(States.count("Connect")), " - Can Connect With"
            # print "          - ",str(States.count("Follow"))," - To Follow"

            for Connect in Accounts:
                if "Connect" in Connect.text:
                    driver.execute_script("arguments[0].click();", Connect)
                    sleep(0.2)
                    try:
                        click("class", "button-primary-large")
                        added += 1
                        print "[+] ", added, " invite Sent !"
                    except:
                        print "Add Note Notification ! Skipping by \"send Now\"..."
                        continue
            page += 1

        print "[+] Congrats ! you Added ", added, "Connection with Keyword", word


def wait(time):
    """
    just a sleep with some text :p
    :param time:
    """
    print "[!] Waiting For page To load ...",
    sleep(time)
    print "Ok"


def withdraw_all():
    """
    open the page of invitations you have sent and withdraw all the request
    ALERT !! : once you withdraw an invitation, you need to wait until 21 days again to re-invite that person  !
    :return:
    """
    print "[+] Removing All Sent Connections "
    driver.get("https://www.linkedin.com/mynetwork/invitation-manager/sent/")
    wait(2)
    while len(driver.find_elements_by_class_name("invitation-card__action-btn")):
        try:
            driver.find_element_by_xpath(
                "/html/body/div[5]/div[5]/div[2]/div/div/div/div/div/div/section/div/ul/li[1]/label").click()
            click("class", "button-primary-medium")
            print "[+] " + str(
                len(driver.find_elements_by_class_name("invitation-card__action-btn"))) + " sent Connection Withdrawn "
            wait(2)
        except WebDriverException:
            print "[+] Done ! You have 0 invitations sent"
            break


def Confirm():
    """
    just a confirmation name instead of using m.getch() avoiding ambiguity
    :return:
    """
    m.getch()


def menu():
    """
    Main menu for choosing witch task to do from the 3 modes
    :return:
    """
    logo = """                            _                      
    |   o __  |  _  _| o __    |_) __ _ __  _ _|_ _  __
    |__ | | | |<(/_(_| | | |   |   | (_)|||(_) |_(/_ | 
    """

    while True:
        print "=" * 80
        print logo
        print " " * 9, "Linkedin Promoter - By Venus-Dev"
        print "=" * 80
        print " " * 10, "[1] - Add from section People you may know"
        print " " * 10, "[2] - Add By keywords and Topics "
        print " " * 10, "[3] - Withdraw All Sent Connections"
        print "=" * 80
        try:
            choice = input("[+] Your Choice :")
            if choice in [1, 2, 3]:
                break
        except SyntaxError:
            pass

    if choice == 1:
        print "=" * 80
        max_accounts = input("[+] Enter Max accounts to scrap (ex :100):")
        driver.get("https://www.linkedin.com/mynetwork/")
        connect_to_my_network(scrap_accounts(max_accounts))

    elif choice == 2:
        print "=" * 80
        keywords = raw_input("[+] Please Enter your Keywords separated by '+' :").split("+")
        max_accounts = input("[+] Enter Max accounts to scrap (ex :100):")
        connect_by_keywords(keywords, max_accounts)
        return

        print "!" * 80
        print "[+] ALERT !! : once you withdraw an invitation, you need to wait until 21 days again to re-invite that " \
              "person  ! "
        print  "!" * 80
        print "[!] Press Enter to Continue"
        Confirm()
        print "[!] Are you Sure !! , if So Press Enter to Continue "
        Confirm()
        withdraw_all()


def main():
    """
    Parcing the COnfig data and doing the main tasks
    :return:
    """
    """
    Parce user Data from the args 
    """


    parser = argparse.ArgumentParser(add_help=True,
                                     description='Promote your linkedin Account by enlarging your network ')
    parser.add_argument('-e', type=str, help="your linkedin email .")
    parser.add_argument('-p', type=str, help="your linkedin password .")
    args = parser.parse_args()

    connect_to_linkedin(args.e, args.p)
    try:
        while True:
            menu()
    except KeyboardInterrupt:
        print  "[-] Good Bye"
        exit(0)
    except WebDriverException:
        print "Selenuim Error ! ", sys.exc_info()


print "[+] Starting Browser ...",
driver = webdriver.Chrome('ChromeDriver', chrome_options=Get_Chrome_Options())
print " OK"

if __name__ == '__main__':
    main()
