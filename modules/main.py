from flask import Flask, render_template, request, send_from_directory
import logging
from logbase import setup_logger, call_logger


def main():
    address = request.remote_addr
    return render_template('main.html', ipaddress = "")