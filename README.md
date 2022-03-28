# Watcherr Test Task
The test task sources are located in two subdirectories: `server` and `client`. 
- `server` one contains the Python web application (built with the Tornado framework) 
which exposes two GET end points (`/task1` and `/task2`) and also the unit tests
(in the `tests.py` file).
- `client` is a very simple React application which basically has one component (`app.tsx`) 
that implements all required functionality. 

### Running the code
To run the application the simplest way just clone the GitHub repository to some directory
and run 
```shell script
$ docker-compose build
```
and then 
```shell script
$ docker-compose up
```

**Note: the `client/Dockerfile` file uses the React development server - this is *not*
how I deploy the React apps to production. But since my primary purpose was to show how
the app works without making you wait - the React dev server runs faster then building 
the production build.

### Task 1

To test the task 1 (Python endpoint) open this URL in your browser:
[http://localhost:8888/task1](http://localhost:8888/task1). 
The browser will show the HTML table with the stores sorted  in the 
alphabetical order along with their GPS coordinates. The `Coordinates` 
column contains hyperlinks to the Google Maps site that shows the markers
for the coordinates found for the store postcode.

**Note 1: At least one store (Bagshot) shows `None, None` as coordinates since
its postcode (`GU19 5DG`) is obsolete and is not resolved by the `postcodes.io`

**Note 2: There is one extra store (named `Additional Store`) I have added to 
the `stors.json` file to test the "nearby stores" functionality in the second part 
of the task.

### Task 1a
The function which returns a list of stores in a given radius of a given postcode
is in the `server/utils.py` file - the function name is `get_nearby_stores()`. 
The tests for this function are in the `server/tests.py` file (`TestTask1` class). 
The first two tests check the postcode that has one additional store (added by me!) 
with a different postcode in the given radius. The third test is for the "remote" store -
the function returns only one store by the postcode.

The tests can be run by (after you install requirements, of course):

``
$ python3 tests.py
``

### Task 2
To test the task 2 (Python endpoint + React app) open this URL in your browser:
[http://localhost:3000](http://localhost:3000). 
The browser will show the React application with the search field. When you type
in this field the API calls are made (debounced) to return respective stores.
Since only the first 3 stores are returned for every search string the `More` button
is shown if there are some more stores to show. When this button is clicked 
the API is called for the "next page" of the search results.

**Note 1: I decided implement paging with the button rather than on the page scrolling 
to a) simplify my own job and b) to avoid using extra components and doing a lot of
testing of how correctly they work with IntersectionObserver, etc.

**Note 2: The task description asked for adding suggestions to the search field -
I decided to skip this to a) save the time and b) because it was not clear how to 
implement this (there was a description how to find stores for the "main" search results,
but not for the suggestions).

Unit tests for the Task 2 API endpoint `server/tests.py` file (`TestTask2` class).

### Q&A

1. If you had chosen to spend more time on this test, what would you have done differently?
    - No harcoding of URLs, ports, etc. - all this should come from the `.env` files.
    - I will add a more robust error handling to both Python and React apps (React app is very
primitive and lack any kind of error handling). 
    - I will check the backend endpoint params. 
    - I will use a proper React app structure (rather than have one "do it all" component)
    - I will set up Eslint/Prettier plugins to save me from formatting the code manually/
    relying on the default setup.
    - I will add more unit tests (to the back end) to cover border cases.
    - I will work on some "pretty" styling.
    - I will use `react-query`/`axios` instead of using the barebone `fetch()` call -
    they really save the time and enforce the robust architecture.
    
2. Make sure you indicate the time you have spent in the README.md file among other metadata.
    - The approximate breakdown looks like:
        - 2h studying the task and checking postcode.io (which ndpoint to use, etc.)
        - 1h checking the Tornado framework (I mostly used Flask/FastAPI before)
        - 2h buiding the Task 1 end-point
        - 3h building and creating tests for the Task 1a endpoint
        - 2h building Task2 endpoint
        - 2h creating React app, using endpoint, solving CORS problems
        - 1h creating Docker files
        - 2h writing this readme.md file
    
3. What part did you find the hardest?
    - There was nothing really hard to do - save for the making myself to use the
    frameworks (like Tornado/requests) instead of reinventing ll the wheels as you asked.
    
 4. What part are you most proud of? In both cases, why?
    - There is nothing to write home about, really...
    
 5. What is one thing we could do to improve this test?
    - With all due respect I did not get the "reinvent the wheel" part of the test.
    Do you guys avoid using the available libs and frameworks in the real life and
    build the web servers from scratch? I do agree Django (or even Flask) is overkill
    for such task but why not to say "use Tornado and whatever else you need and concentrate
    on the business logic"? 
    
 6. Code your own constructs and 2 very general reusable methods you use over and over again.
    - There is a reusable function named `extend_dict_list()` in the `server\utis.py` file - it 
    implements something like the "left join" (or rather a `lookup()` from MongoDB)
    - There is a reusable function named `check_response()` in the `server\postcode_lookup.py`
    file - it checks if the call to the external API returned with the "good" status code
    and raises an exception with the detailed error description otherwise.