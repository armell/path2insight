

TEST_PATHS_WINDOWS = [
    ('C:/Program Files/unittest/docs.pdf'),
    ('C:/Program Files/unittest/docs.pdf'),
    ('/Program Files/unittest/docs.pdf'),
    ('//Program Files/unittest/docs.pdf'),
    ('docs.pdf')
]

# set up some test data
TEST_PATHS_POSIX = [
    ('/Users/unittest/docs.pdf'),
    ('/Users/unittest/docs.pdf'),
    ('/Users/unittest/docs.pdf'),
    ('docs.pdf')
]


TEST_PATHS_MULTI_WINDOWS = [
    ('C:/Program Files/unittest', 'docs.pdf'),
    ('C:/Program Files/unittest', 'docs.pdf'),
    ('/Program Files/unittest', 'docs.pdf'),
    ('//Program Files/unittest', 'docs.pdf'),
    ('', 'docs.pdf')
]

# set up some test data
TEST_PATHS_MULTI_POSIX = [
    ('/Users/unittest', 'docs.pdf'),
    ('/Users/unittest', 'docs.pdf'),
    ('/Users/unittest', 'docs.pdf'),
    ('', 'docs.pdf')
]