#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import absolute_import

import os
import time
import os.path
from sys import exit
from fabric.api import env, local, run
from fabric.colors import blue, red
import fabric.contrib.project as project
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import yaml


# Remote host and username
env.hosts = []
env.user = ""
env.colorize_errors = True

# Local destination path
env.local_destination = os.path.join(
    os.path.abspath(os.path.dirname(__file__)),
    "destination/")
# Remote path to deploy destination
env.remote_destination = ""

# Other options
env.rsync_delete = False


def update_simiki():
    print(blue("Old Version: "))
    run("simiki -V")
    run("pip install -U simiki")
    print(blue("New Version: "))
    run("simiki -V")


def deploy():
    if not env.remote_destination:
        if env.rsync_delete:
            print(red("You can't enable env.rsync_delete option "
                      "if env.remote_destination is not set!!!"))
            print(blue("Exit"))
            exit()

        print(red("Warning: env.remote_destination directory is not set!\n"
                  "This will cause some problems!!!"))
        ans = raw_input(red("Do you want to continue? (y/N) "))
        if ans != "y":
            print(blue("Exit"))
            exit()

    project.rsync_project(
        local_dir=env.local_destination,
        remote_dir=env.remote_destination.rstrip("/") + "/",
        delete=env.rsync_delete
    )


def g():
    local("simiki generate")


def p():
    local("simiki preview")


def gp():
    g()
    p()


class Handler(FileSystemEventHandler):
    def on_modified(self, event):
        self.config = yaml.load(open("_config.yml", "r"))
        self.config['debug'] = True
        with open("_config.yml", "w") as config_file:
            config_file.write(yaml.dump(self.config, default_flow_style=False))
        g()


def l():
    event_handler = Handler()
    observer = Observer()
    observer.schedule(event_handler, path='content/', recursive=True)
    observer.start()

    try:
        while True:
            time.sleep(1)
    except (KeyboardInterrupt, SystemExit):
        config = yaml.load(open("_config.yml", "r"))
        config['debug'] = False
        with open("_config.yml", "w") as config_file:
            config_file.write(yaml.dump(config, default_flow_style=False))
        observer.stop()
    observer.join()
