# Muninn
A simple Mastodon onboarding bot written in python and suitable for docker deployment. 

## What it does

This bot accepts incoming posts from the built-in Mastodon webhook for newly created and/or approved accounts. It then fires off a welcome message (fully configurable) from an authorized account. 

![welcome_screenshot](https://user-images.githubusercontent.com/83498383/224165328-fac6de68-5f24-4877-b809-425095a2854b.png)



## Installation and configuration
The simplest installation is to run this on docker (docker file included) and create a webhook in the 'Admin' panel on Mastodon that points to the network location of your docker instance. This could easily be adapted to heroku or other services. After that, you need to create an application on an appropriate account on your instance and use the generated api token.

Configuration is done by creating a .env file in the root folder - .env.dist contain all of the required variables and example values.
