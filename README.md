# Betting Website

A betting site simulator for British Premier League where user has the ability to check the match results, league table, place bets and compete against others.
Celery and RabbitMQ were used to handle the delayed simulation of match results based on the match schedule.
This way when a match date comes no bets can be placed anymore and after additional 90 minutes the result is drawn, saved to database and shown on the page.
Signing up and logging in has been implemented using built-in Django functions. 
Dynamic changes to the website like coupon generating is done using vanilla JS.
<br/><br/>

![table](https://user-images.githubusercontent.com/91700001/220476579-644344b6-5d42-433e-911b-8d28cde59c58.PNG)

![bets](https://user-images.githubusercontent.com/91700001/220476595-646e7642-97ef-4f3f-a43f-8ae4ce34cc68.PNG)

![res](https://user-images.githubusercontent.com/91700001/220476616-8e917c9d-8333-4c19-9a5a-adf76d11cc44.png)

![coup](https://user-images.githubusercontent.com/91700001/220476637-dafd2993-b9a0-4715-8b58-23e251ed4483.PNG)

![leaderb](https://user-images.githubusercontent.com/91700001/220476645-a9952f8f-85ba-4840-8d58-9349801683fe.PNG)

Yet to do:
- Strict backend validation
- Deposits and withdrawals
- RWD
