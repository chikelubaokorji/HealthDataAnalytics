virtualenv --python=/usr/bin/python3.7 python
source python/bin/activate
pip install -r requirements.txt -t python/lib/python3.7/site-packages
zip -r9 python.zip python