#!/usr/bin/python3
import sys
import os # For backwards compatibility and other stuff
from subprocess import Popen, PIPE

# default-configuration: Edits default Nginx site to place geth node
# in upstream proxy_pass
# Note that this configuration sets ssh to disabled

# CONSTANTS CONFIGURATION
BACKUP_ON_DESTRUCT = True
SERVER_NAME = "_"
PORT = 8545
PASSWORD_DIRECTORY = "/etc/nginx/"
PASSWORD_FILE = "protected.htpasswd"
AUTH_FILE = "/etc/nginx/protected.htpasswd"
NGINX_CONFIG_FILENAME = "GoLangNode"
NGINX_ROOT_DIRECTORY = "/etc/nginx/"
SITES_DIRECTORY = "/etc/nginx/sites-available"
NGINX_SITE_FILE = "default"

# NGINX Config File

NGINX_CONFIG = """
server {
    listen 80 default_server;
    listen [::]:80 default_server ipv6only=on;
    server_name %s;

    # Geth proxy that password protects the public Internet endpoint
    location / {
        auth_basic \"Restricted\";
        auth_basic_user_file %s;

        # Proxy to geth note that is bind to localhost port
        proxy_pass http://localhost:%s;
    }
}
""" % (SERVER_NAME,
           os.path.join(PASSWORD_DIRECTORY,PASSWORD_FILE),
           PORT)


# Backup old NGINX Default

rewrite_location = os.path.join(SITES_DIRECTORY, NGINX_SITE_FILE)

backup_nginx_command = "sudo cp {dir_and_file} {backup_loc}".format(
                                              dir_and_file = rewrite_location,
                                              backup_loc = NGINX_ROOT_DIRECTORY
                                           )

# Clear old NGINX FILE
file_clear_command = "sudo -S rm {fil_loc}".format(fil_loc = rewrite_location)
file_write_command = 'sudo -S echo "{contents}" >> {target_file}'.format(contents = NGINX_CONFIG, target_file = rewrite_location)

# Run Backup
os.system(backup_nginx_command)

# Run Clear Command
os.system(file_clear_command)

# Run File Write Command
os.system(file_write_command)
