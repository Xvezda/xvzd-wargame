#!/bin/bash

mkdir driver
cd driver
curl https://chromedriver.storage.googleapis.com/76.0.3809.68/chromedriver_linux64.zip -o driver.zip
unzip driver.zip
rm driver.zip
cd ..
