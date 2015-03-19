#!/usr/bin/env bash

INSTALL_DIR=/var/lib/kb_light_stats
CONFIG_DIR=/etc/kb_light_stats

if [ ! -d "$INSTALL_DIR" ]; then
	mkdir -p $INSTALL_DIR
fi
cp -v ./kb_light_stats.conf $INSTALL_DIR/kb_light_stats.conf.template
cp -v ./*.py $INSTALL_DIR/

if [ ! -d "$INSTALL_DIR/stats" ]; then
	mkdir -p $INSTALL_DIR/stats
fi
cp -vR ./stats/*.py $INSTALL_DIR/stats/

if [ ! -d "$INSTALL_DIR/TuxedoWmi" ]; then
	mkdir -p $INSTALL_DIR/TuxedoWmi
fi
cp -vR ./TuxedoWmi/*.py $INSTALL_DIR/TuxedoWmi/

if [ ! -d "$CONFIG_DIR" ]; then
	mkdir -p $CONFIG_DIR
fi
if [ ! -f "$CONFIG_DIR/kb_light_stats.conf" ]; then
	cp -v ./kb_light_stats.conf $CONFIG_DIR/kb_light_stats.conf	
fi
