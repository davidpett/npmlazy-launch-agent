#!/usr/bin/env python

# Creates a LaunchAgent for npm_lazy, or does nothing
# if it's already installed.

import os, sys, getpass, commands

def command(cmd):
  print cmd
  os.system(cmd)

def finished():
  print "\nIf you want to switch back to normal npm, run:\n\n    npmrc default\n"
  print "If you want to see replication progress, run:\n\n    pm2 logs all\n"
  print "If you want to uninstall, run:\n\n    launchctl unload ~/Library/LaunchAgents/com.davidpett.npmlazy.plist\n"

install_dir = os.path.expanduser('~/.npm_lazy')
if not os.path.exists(install_dir):
  os.mkdir(install_dir)

done_file = os.path.join(install_dir, 'done')
if os.path.exists(done_file):
  print "\nLooks like npm_lazy is already installed! Exiting."
  finished()
  sys.exit(1)

command('npm install -g npm_lazy pm2 npmrc')

plist = '''<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple Computer//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
  <dict>
    <key>Label</key>
    <string>com.davidpett.npmlazy</string>
    <key>ProgramArguments</key>
    <array>
      <string>%s</string>
      <string>%s</string>
      <string>start</string>
      <string>%s</string>
      <string>--</string>
      <string>%s</string>
    </array>
    <key>RunAtLoad</key>
    <true/>
    <key>KeepAlive</key>
    <false/>
    <key>StandardErrorPath</key>
    <string>/tmp/npmlazy.err</string>
    <key>StandardOutPath</key>
    <string>/tmp/npmlazy.out</string>
    <key>UserName</key>
    <string>%s</string>
    <key>WorkingDirectory</key>
    <string>%s</string>
  </dict>
</plist>'''

plist = plist % (\
  commands.getoutput('which node'), \
  commands.getoutput('which pm2'), \
  commands.getoutput('which node'), \
  commands.getoutput('which npm_lazy'), \
  getpass.getuser(), \
  install_dir)

out_file = open(os.path.expanduser('~/Library/LaunchAgents/com.davidpett.npmlazy.plist'), 'w')
out_file.write(plist)
out_file.close()

command('launchctl load -w ~/Library/LaunchAgents/com.davidpett.npmlazy.plist')

command('npmrc -c local')
os.system('npm config set registry http://localhost:8080/')

open(done_file, 'a').close()

print "\nDone! You now have npm_lazy running at 127.0.0.1:8080"
print "You also have an npmrc called \"local\" configured to point to it."
print "All offline data is stored in ~/db/"
finished()
