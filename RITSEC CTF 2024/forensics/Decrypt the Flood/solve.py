#!/usr/bin/env python3
import os

os.system('strings evidence.pcap | grep -E "RS{.+}"')
