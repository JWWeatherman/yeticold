from flask import Flask, render_template, redirect, url_for, request
import os
import subprocess
import json
import cv2
from qrtools.qrtools import QR
from pyzbar.pyzbar import decode
from PIL import Image
import random
import qrcode
from datetime import datetime
import time
import werkzeug
from bitcoinrpc.authproxy import AuthServiceProxy, JSONRPCException
