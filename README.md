# NTUST_TGBOT
NTUST Course Assist Bot

This Telegram Bot can help the students of NTUST search the available course efficiently

This repository contains:

1. The usage of this Telegram Bot
2. A Django program of this project
3. The guide of create the Bot service

## Table of Contents:
- [Background](#background)
- [Install](#install)
- [Usage](#usage)
- [Maintainer](#maintainer)

## Background
Because of the Course Searching system provided by NTUST does not have the quota inquire function,
So we devoloped this Line bot to provide a platform that can inquire the course quota.

The goals for this repository are:

1. To provide the NTUST student have a convient way to check the quota fo course.
2. To make a platform can combine the all of lecture informations
3. To provide the notice of NTUST

## Install
To establish this Telegram bot service, please use the [Dockerfile](./Dockerfile) to build the image.

You can use this command to build the image:

`$ docker build -t tgbot . --no-cache`

Then use this command to run the service:

`$ docker run -p 8000:8000 -v /path/to/your/token.txt:/usr/src/app/courseQuery/token.txt -d --restart always tgbot`

## Usage
You can use the telegram bot we establish:

[@Brandon_NTUST_Bot](https://t.me/Brandon_NTUST_Bot)

## Maintainer
[@Aiden_Lai](https://github.com/AidenLai)
