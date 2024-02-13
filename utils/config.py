import os
import logging
from dotenv import load_dotenv

# URL Template: https://auto.ria.com/uk/car/used/?page={}

LOG_PATH = os.path.join(os.getcwd(), "utils", "log.txt")


logging.basicConfig(format='%(asctime)s %(message)s',
                    filename=LOG_PATH,
                    level=logging.DEBUG,
                    datefmt='%Y-%m-%d %H:%M:%S')

logger = logging.getLogger(__name__)

load_dotenv()

URL_TEMPLATE = os.getenv('URL_TEMPLATE')
DUMP_TIME = int(os.getenv('DUMP_TIME'))
SCRAPPER_TIME = int(os.getenv('SCRAPPER_TIME'))
DB_NAME = os.getenv('DB_NAME')
DB_USER = os.getenv('DB_USER')
DB_PASSWORD = os.getenv('DB_PASSWORD')
DB_HOST = os.getenv('DB_HOST')
DB_PORT = int(os.getenv('DB_PORT'))
