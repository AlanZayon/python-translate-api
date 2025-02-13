#!/bin/bash
gunicorn --workers 4 --timeout 120 -b 0.0.0.0:10000 app:app