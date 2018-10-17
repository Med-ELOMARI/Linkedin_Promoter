# Linkedin Promoter 
#### By MOHAMED EL OMARI - Venus-Dev
Promote your linkedin Account with -Linkedin_Promoter- to enlarge your network - By :
  - Mass Adding from section People you may know
  - Add By your own keywords and interest **YAAY !**
  - Withdraw All Sent Connections to start again (once you withdraw an invitation, you need to wait until 21 days again to re-invite that)
  - specifie how much you want to add 

# Features !
  - handle and skip the pop-up box asking to add a note
  - Login once by saving the session cookies ( Removed due to chrome and ChromeDriver version conflict )

# Used Tech :
### - Selenium
* Selenium automates browsers. That's it! What you do with that power is entirely up to you. Primarily, it is for automating web applications for testing purposes, but is certainly not limited to just that. Boring web-based administration tasks can (and should!) be automated as well.
### - ChromeDriver - WebDriver for Chrome
* WebDriver is an open source tool for automated testing of webapps across many browsers. It provides capabilities for navigating to web pages, user input, JavaScript execution, and more.  ChromeDriver is a standalone server which implements WebDriver's wire protocol for Chromium. 
### - Python 2.7

# Installation :

Install the dependencies and devDependencies and start the server.
```cmd
 pip install selenium
```
And Download **ChromeDriver - WebDriver for Chrome** from [here] 
Make sure to put the **ChromeDrive** next to the script and named *ChromeDriver.exe*
# Usage :
```cmd
python linkedin_Promoter.py -e YOUR_EMAIL -p YOUR_PASSWORD
```
- Make sure to check if you're connected or not because There no Test are done by the script (This version ).
- You can change the times of retry from **MAX_CLICK_TRIES** .
- when you choose an option you can enter the maximum namber of accounts to add (Maybe more some times) .
- in the second choice (**Add By your own keywords and interest**) you can type as much you want of keywords seprated by space  .
- You can play around with these arguments like making it headless or changing loging level it's on your court now ;) : 
- - *chrome_options.add_argument("--disable-logging")
chrome_options.add_argument('log-level=3')
chrome_options.add_argument("--headless")
chrome_options.add_argument("--incognito")
chrome_options.add_argument("--disable-extensions")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--allow-running-insecure-content")
chrome_options.add_argument("--ignore-certificate-errors")*

PS :  Check the Code nothing Sent to me or a server if you have any doubt . Moreover , Don’t worry. Your password is totally strong enough lol 
# ***Tested On Windows  with an English Linkedin  Only!***
# First Option :
![1](https://user-images.githubusercontent.com/11338137/47062798-001b6c00-d1d0-11e8-94d6-4e27233d0e4b.png)
# Second Option :
![2](https://user-images.githubusercontent.com/11338137/47062796-ff82d580-d1cf-11e8-85c1-446e6e3b4a02.png)
# Third Option :
![3](https://user-images.githubusercontent.com/11338137/47062797-001b6c00-d1d0-11e8-906a-893573a9ab2a.png)
# Todos :
 - *Bezaaaaaaf lol*

##### About me :
* [linkedin] *Endorse me on linkedin*
* [Facebook] 
* [instagram]

# License
**Free Software, Hell Yeah !**

   [here]: <http://chromedriver.chromium.org/downloads>
   [Facebook]:<https://www.facebook.com/MED.E6>
   [instagram]:<https://www.instagram.com/mohamed_el_0mari>
   [linkedin]:<https://www.linkedin.com/in/elomarimohamed/>
   
