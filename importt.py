TOKEN = '5698038766:AAGNe8sBNZKouBQpqFGg1zs5EUiG0PehtpQ'
#TOKEN = '1873466238:AAGU_9hLBiJ7107Ar2AZZEAzRALNFBaZ2Hw'
import random
import sqlite3 as sq
import logging
# from data_words import base
import aiogram.utils.markdown as md
from aiogram import Bot, Dispatcher, types
from aiogram.types import ParseMode, InlineKeyboardMarkup
from aiogram.utils import executor
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from datetime import datetime
import re

from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.contrib.fsm_storage.memory import MemoryStorage



from aiogram.types import InlineKeyboardMarkup

class actions(StatesGroup):                                                             #создаем класс и передаем параметр StatesGroup(хз что это)
    action = State()
    restart_or_continue = State()
    restart = State()
    FIO = State()

import os, time

import httplib2
from google.oauth2.gdch_credentials import ServiceAccountCredentials
from googleapiclient.discovery import build
from google.oauth2 import service_account

v = 5.131
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SERVICE_ACCOUNT_FILE = os.path.join(BASE_DIR, 'credentials.json')
credentials = service_account.Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)

SAMPLE_SPREADSHEET_ID = '13Z5AZKsa-rwt5J01c8yjLn3GzGSbuypnLF3lH5_9sT0'

SAMPLE_RANGE_NAME = 'Лист1'

service = build('sheets', 'v4', credentials=credentials)

sheet = service.spreadsheets()

