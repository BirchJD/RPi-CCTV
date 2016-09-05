# RPiCCTV - CCTV System for Raspberry Pi
# Copyright (C) 2016 Jason Birch
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see &lt;http://www.gnu.org/licenses/>.

/****************************************************************************/
/* V1.00   2016-09-02  Jason Birch                                          */
/*                                                                          */
/* Manual process to install CCTV package on a clean Raspberry OS for       */
/* Raspberry Pi.                                                            */
/****************************************************************************/

/***************************************************/
/* Write a clean Raspberry OS image to an SD card. */
/***************************************************/

  /**********************************************************/
 /* Configure Wifi access directly to SD card file system. */
/**********************************************************/
sudo vi /[SD_MOUNT_PONT]/etc/wpa_supplicant/wpa_supplicant.conf 
   country=GB
   ctrl_interface=DIR=/var/run/wpa_supplicant GROUP=netdev
   update_config=1

   network={
      ssid="[SSID]"
      psk="[PSK]"
      key_mgmt=WPA-PSK
   }

/************************************************/
/* Place SD card into Raspberry Pi and boot up. */
/************************************************/

  /*********************************************/
 /* Start an ssh session to the Raspberry Pi. */
/*********************************************/
ssh pi@[IP_ADDRESS]

  /**************************************/
 /* Install the RPi-CCTV distribution. */
/**************************************/
wget https://github.com/BirchJD/RPi-CCTV/archive/master.zip
unzip master.zip

  /*************************************************************************/
 /* Make sure the default pi and root passwords are changed for security. */
/*************************************************************************/
passwd
sudo passwd

   /*********************************************/
  /* Install an ssh public key to allow access */
 /* without the need to enter a password.     */
/*********************************************/
mkdir ~/.ssh
chmod go= ~/.ssh
chmod u=rwx ~/.ssh
touch ~/.ssh/authorized_keys
chmod go= ~/.ssh/authorized_keys
chmod u=rw ~/.ssh/authorized_keys

ssh-keygen -t rsa -b 4096 -C "x@x.com"
cat ~/CCTV_rsa.pub >  ~/.ssh/authorized_keys

  /*********************************************/
 /* Perform Raspberry Pi configuration steps. */
/*********************************************/
sudo raspi-config
   Wait for network at boot, disable.
   Set hostname.
   Enable ssh.
   Enable camera.
   Autologin.
   Expand file system.

   /**********************************************************/
  /* Set Linux configuration options.                       */
 /* Edit existing lines or add lines if they do not exist. */
/**********************************************************/
sudo vi /boot/config.txt
   disable_camera_led=1
   arm_freq=900
   gpu_mem=256

  /*********************************************************/
 /* Update Raspberry OS and install required OS packages. */
/*********************************************************/
sudo apt-get update
sudo apt-get upgrade
sudo apt-get dist-upgrade
sudo apt-get install libav-tools
sudo apt-get install motion
sudo apt-get install apache2
sudo apt-get install libapache2-mod-php5

  /******************************/
 /* Enable CCTV web interface. */
/******************************/
sudo a2enmod php5
sudo a2ensite 000-default.conf

sudo mkdir /var/www/html/temp/
sudo chmod gu=rwx /var/www/html/temp
sudo chown -R www-data:www-data /var/www/html
sudo rm /var/www/html/index.html
sudo cp RPi-CCTV-master/index.php /var/www/html/
sudo cp RPi-CCTV-master/wwwFrame.sh /usr/lib/cgi-bin/
sudo sudo chown -R www-data:www-data /usr/lib/cgi-bin

  /*******************************************************************/
 /* Configure the required CCTV process to start when system boots. */
/*******************************************************************/
vi .bashrc
   HISTSIZE=0
   HISTFILESIZE=0
   cd /home/pi/RPi-CCTV-master/
   ./Start.sh 2>&1 /home/pi/Start.log
   # ./Start-Photo.sh 2>&1 /home/pi/Start-Photo.log
   # ./Start-Motion.sh 2>&1 /home/pi/Start-Motion.log
   # ./Start-IR-Motion.sh 2>&1 /home/pi/Start-IR-Motion.log


  /************************************************/
 /* Add the pi user to the motion package group. */
/************************************************/
sudo vi /etc/group
   motion:x:114:pi

  /************************************/
 /* Configure cron scheduled events. */
/************************************/
crontab -e
0 * * * * /home/pi/RPi-CCTV-master/PruneData.sh > /home/pi/PruneData.log
0,5,10,15,20,25,30,35,40,45,50,55 * * * * /home/pi/RPi-CCTV-master/CheckWifi.sh >> /home/pi/CheckWifi.log

#/************************************************************************/
#/* NOTE THE FOLLOWING ARE THE CONFIGURATION OPTIONS WHICH HAVE BEEN SET */
#/* IN THE MOTION.CONF FILE COPIED IN THE LINE ABOVE, FOR REFERENCE.     */
#/************************************************************************/
# sudo cp /etc/motion/motion.conf /home/pi/RPi-CCTV-master/
# vi /home/pi/RPi-CCTV-master/motion.conf
#    daemon off
# 
#    threshold_tune off
#    threshold 15000
#    # despeckle_filter EedDl
#    max_movie_time 300
#    event_gap 60
#    auto_brightness on
#    brightness 25
# 
#    target_dir /DATA
#    width 2592
#    height 1944 
#    rotate 0
#    text_double on
# 
#    picture_filename %v-%Y%m%d%H%M%S-%q
#    output_pictures on
#    quality 50
# 
#    movie_filename %v-%Y%m%d%H%M%S
#    ffmpeg_output_movies off
#    ffmpeg_variable_bitrate 15
#    framerate 25
# 
#    stream_auth_method 1
#    stream_authentication CCTV:CCTVpass
#    stream_maxrate 1
#    stream_localhost off
#    stream_port 4000
#    stream_quality 50


  /*****************************/
 /* Restart the Raspberry Pi. */
/*****************************/
sudo reboot

