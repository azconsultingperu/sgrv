import os
import sys

BASE = os.path.dirname(os.path.abspath(__file__))
if BASE not in sys.path:
    sys.path.insert(0, BASE)

from dotenv import load_dotenv
load_dotenv(os.path.join(BASE, '.env'))

from app import create_app

application = create_app()
