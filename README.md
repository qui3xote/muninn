# Muninn
A simple Mastodon onboarding bot written in python and suitable for docker deployment. 

## What it does

This bot accepts incoming posts from the built-in Mastodon webhook for newly created and/or approved accounts. It then fires off a welcome message (fully configurable) from an authorized account. 

![Screenshot 2023-03-09 at 3 52 40 PM](https://user-images.githubusercontent.com/83498383/224162109-605fdc58-010c-47a7-8a62-4b34b7523062.png)


## Installation and configuration
The simplest installation is to run this on docker (docker file included) and create a webhook in the 'Admin' panel on Mastodon that points to the network location of your docker instance. This could easily be adapted to heroku or other services. After that, you need to create an application on an appropriate account on your instance and use the generated api token.

Configuration is done by creating a .env file in the root folder - .env.dist contain all of the required variables and example values.
