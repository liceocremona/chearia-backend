#!/bin/bash
systemctl stop chearia-backend.service
git pull
cp chearia-backend.service /etc/systemd/system/chearia-backend.service
cp http.conf /etc/nginx/conf.d/
systemctl start chearia-backend.service
systemctl restart nginx