<!-- dbproject2017 -->

How to run the server: 

  step 1. cd into djangoProj/mysite
  step 2. unzip db.sqlite3.zip, export to . [djangoProj/mysite]
  step 3. make sure you have pip and django installed
    pip: https://pip.pypa.io/en/latest/installing/#installing-with-get-pip-py
    django: https://docs.djangoproject.com/en/2.0/topics/install/
  step 4. install geopy
    run: python -m pip install geopy
  step 5. run: python manage.py runserver
    (Starting development server at http://127.0.0.1:8000/)
  step 6. in browser, go to http://127.0.0.1:8000/polls/

Notes:
  1. Because of the incompleteness of the Yelp data set, the only cities for which the Airbnb listing search will return meaningful results are Las Vegas and Pittsburgh.  However, feel free to use the secondary search section to query fun facts about the Airbnb's in each city.
  2. At this point, we have limited interests selection to two cuisines, activities, and entertainments, each.
  3. We have extraneous Django models (relations) because we based them off the original data sets but didn't end up needing them.  Then, we chose not to delete them so as not to invoke further migrations.  The only relevant models are Airbnb_listing, business, attribute, and category.
  