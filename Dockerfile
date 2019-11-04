# FROM python:3
# ADD flight_search.py /flight_search.py


# CMD [ "python", "./flight_search.py" ]

FROM pypy:3

ADD flight_search.py /flight_search.py

CMD [ "pypy3", "./flight_search.py" ]