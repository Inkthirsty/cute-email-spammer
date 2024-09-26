# cute-email-spammer

summary: this is a script that signs up the entered email for random services. this wasnt a serious project so its not very fast or well presented but if you for some reason need to use this then enjoy...

if you want to make a better version feel free to use anything from here (you know who you are, i live in your head rent free)

![image](https://github.com/user-attachments/assets/df0e2d68-5838-4937-9469-d5cc9c490e06)

![image](https://github.com/user-attachments/assets/6e21cb55-8133-45c6-b3c6-60e3356d6a6d)

tw// good music

https://github.com/user-attachments/assets/c98d32ed-8b36-4cc9-a234-8df8f17f8020

if you want some throwaway emails to test this with here
- https://mail.tm/en/
- https://mail.gw/en/
- https://temp-mail.io/en
- https://tempmailo.com/

## how to use
1. pip install aiohttp
2. run the script
3. paste any email
4. let it do its magic
5. enjoy ^_^

alternatively you can paste main.py into this site and it might work https://trinket.io/python3

## info
- intentionally slow because python is shit and i dont know any other programming languages
- u can flood inboxes of people u don't like
- i didn't bother with optimisation
- around 70% success rate (some apis might have changed how they work because of me lol)
- i live in the uk so some apis may not work for you
- sometimes you get an "assertion error" and I have no idea how to prevent it (possibly occurs due to excessive async usage) but you can lower the thread limit if it happens
- i don't plan to update this often but if i find sites i may expand it

## extra info
- if you want to "debug" which sites do and do not work, set threads to 1
- a file named "results.txt" will record all responses
- let me know if any websites no longer work
- you can give me site recommendations using [discussions](https://github.com/Inkthirsty/cute-email-spammer/discussions) or something
- i found half of these random sites by googling "... shop" or using a vpn to search for sites in different countries

## people i want to thank for making this slightly better
- gacekkosmatek - didn't directly contribute to this but caused my async addiction
- wv8 - helping me optimise this + giving me motivation to work on it + telling me to add a timeout
- chelpus - making a faster generate function

