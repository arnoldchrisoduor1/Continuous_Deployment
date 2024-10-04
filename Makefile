install:
		pip install --upgrade pip &&\
			pip install -r requirements.txt

lint:
		pylint --disable=R,C main.py test_api.py

test:
	python -m pytest -vv --cov=routes test_api.py