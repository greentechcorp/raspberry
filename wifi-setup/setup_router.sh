#!/bin/bash

sudo systemctl stop dnsmasq
sudo systemctl stop hostapd

sudo cp /etc/dhcpcd_router.conf /etc/dhcpcd.conf
sudo cp /etc/default/hostapd_router /etc/default/hostapd

sudo service dhcpcd restart

sudo systemctl start dnsmasq
sudo systemctl unmask hostapd
sudo systemctl enable hostapd
sudo systemctl start hostapd
