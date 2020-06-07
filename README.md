# EasyWork :money_with_wings:
## Full-Stack Python, Flask, HTML, CSS, Bootstrap project created by [Nikola](https://github.com/nikolata) and [Tanya](https://github.com/tanyabudinova)
A website that helps people find work in a very easy way

Requirements
----------------------------
Before you can use the website, you need to install some packages.
```bash
pip install -r requirements.txt
```

How it works
---------------------------
#### To start the website, you need to run in the terminal ```python3 main.py```.
This will run the flask server on [localhost](http://127.0.0.1:5000/) and will create your empty database.
#### Sign up as candidate/company
In this project we have 2 types of users - candidates and companies.
Companies can create new jobs, see all candidates ordered by categories, see all candidates that liked their job and they can like and write to candidates. Fully working CRUD for the company's profile and all jobs created by them.
Candidates can see all new jobs, like or pass them and if they have messages from company, they can respond to them. This way we ensure that there is no spam, because only companies can text first. Fully working CRUD for the candidate's profile.
#### Log in
When you have an account, you can log in at any time and see new jobs or messages.

Demo
------------------------
![](demo.gif)

TODO
-----------------------
- Complete the front-end
- Integrate email notification when you receive a new message
- Write some tests
- Add CI
- Better UI

### The elephant team wishes you a nice day! :elephant: :four_leaf_clover: