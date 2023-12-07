#!/usr/bin/env bash
# script to set up clean server
sudo apt-get -y update
sudo apt-get -y install nginx
sudo service nginx start
sudo mkdir -p /data/web_static/shared/
sudo mkdir -p /data/web_static/releases/test/
echo "<!DOCTYPE html>
<html>
    <head>
        <title>Home - AirBnB clone</title>
    </head>
    <body>
        <h1>Welcome to AirBnB clone - Deploy static!</h1>
        <h2>I'm Salah Koulal from  Alx Africa</h2>
    </body>
</html>" | sudo tee /data/web_static/releases/test/index.html
sudo ln -fs /data/web_static/releases/test/ /data/web_static/current
sudo chown -R ubuntu:ubuntu /data/
sudo sed -i '39 i\ \tlocation /hbnb_static {\n\t\talias /data/web_static/current;\n\t}\n' /etc/nginx/sites-enabled/default
sudo service nginx restart
