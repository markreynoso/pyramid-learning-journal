# pyramid-learning-journal

https://marksthoughtfulspot.herokuapp.com/

A simple Pyramid app for listing and displaying expenses.

**Authors**:

- Mark Reynoso
- 401 Python Course Project

## Routes:

- `/` - the home page and a listing of all blogs
- `/expense/1` - the page for an individual blog post
- `/journal/new-entry` - to create a new blog post
- `/expense/{id:\d+}/edit=entry` - for editing existing blog post

## Set Up and Installation:

- Clone this repository to your local machine.

- Once downloaded, `cd` into the `pyramid-learning-journal` directory.

- Begin a new virtual environment with Python 3 and activate it.

- `cd` into the `learning-journal` directory. It should be at the same level of `setup.py`

- `pip install` this package as well as the `testing` set of extras into your virtual environment.

- `$ initialize_db development.ini` to initialize the database, populating with random models.

- `$ pserve development.ini --reload` to serve the application on `http://localhost:6543`

## To Test

- If you have the `testing` extras installed, testing is simple. If you're in the same directory as `setup.py` type the following:

```
$ py.test learing_journal
```

## Test Coverage

```
---------- coverage: platform darwin, python 2.7.14-final-0 ----------
Name                                    Stmts   Miss  Cover   Missing
---------------------------------------------------------------------
learning_journal/data/__init__.py           0      0   100%
learning_journal/data/journal_data.py       2      0   100%
learning_journal/routes.py                  6      0   100%
learning_journal/views/__init__.py          0      0   100%
learning_journal/views/default.py          21      0   100%
learning_journal/views/notfound.py          4      2    50%   6-7
---------------------------------------------------------------------
TOTAL                                      33      2    94%

---------- coverage: platform darwin, python 3.6.3-final-0 -----------
Name                                    Stmts   Miss  Cover   Missing
---------------------------------------------------------------------
learning_journal/data/__init__.py           0      0   100%
learning_journal/data/journal_data.py       2      0   100%
learning_journal/routes.py                  6      0   100%
learning_journal/views/__init__.py          0      0   100%
learning_journal/views/default.py          21      0   100%
learning_journal/views/notfound.py          4      2    50%   6-7
---------------------------------------------------------------------
TOTAL                                      33      2    94%
```