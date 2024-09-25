# cute-email-spammer

summary: this is a script that signs up the entered email for random services. this wasnt a serious project so its not very fast or well presented but if you for some reason need to use this then enjoy...

if you want to make a better version feel free to use anything from here (you know who you are, i live in your head rent free)

![image](https://github.com/user-attachments/assets/851d8fda-7888-4d3e-a429-bb55a3c87e93)

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

## examples
### here's the aftermath of 1 thread
![image](https://github.com/user-attachments/assets/03d0e1b6-2827-432e-a452-c0f1cfaa6504)
![image](https://github.com/user-attachments/assets/ea83f063-3fbf-453d-a9f2-d26e1cf402dc)

### here's the instant aftermath of 1000 threads
![image](https://github.com/user-attachments/assets/dc260e03-2b79-4ac6-99ff-ae86642ae487)
![image](https://github.com/user-attachments/assets/c97b3396-09bb-4e89-a8d9-98e9e42efba4)

### here's the aftermath of 1000 threads after 24 hours
![image](https://github.com/user-attachments/assets/cd3b0917-91db-4838-b9b4-9415f78d9234)

