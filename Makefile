install:
		pip install --upgrade pip &&\
			pip install -r requirements.txt

lint:
		pylint --disable=R,C app.py test_api.py test_unit.py

test:
	python -m pytest -vv --cov=routes test_unit.py test_api.py