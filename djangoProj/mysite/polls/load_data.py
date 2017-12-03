#loading in yelp data
csv_filepathname="/Users/Erika/Downloads/uttn/yelp_businesses.csv"
dataReader = csv.reader(open(csv_filepathname, errors= 'ignore'), delimiter=',', quotechar='"', )
for row in dataReader:
    print (row)
    if row[0] != 'id':
        # Ignore the header row, import everything else
        biz = business()
        biz.id = row[0]
        biz.name = row[1]
        biz.neighborhood = row[2]
        biz.address = row[3]
        biz.city = row[4]
        biz.state = row[5]
        biz.postal_code = row[6]
        biz.latitude = row[7]
        biz.longitude = row[8]
        biz.stars = row[9]
        biz.review_count = row[10]
        biz.is_open = row[11]
        biz.save()

csv_filepathname="/Users/Erika/Downloads/uttn/yelp_categories.csv"
dataReader = csv.reader(open(csv_filepathname, errors= 'ignore'), delimiter=',', quotechar='"', )
for row in dataReader:
    print (row)
    #if row[0] != 'id':
        # Ignore the header row, import everything else
    cat = category()
    cat.business_id = row[0]
    cat.category = row[1]
    cat.save()



#next time just change the .csv file below and put in the views.py vote function
csv_filepathname="/Users/Erika/Documents/2017-2018 Senior/Databases/dbproject2017/djangoProj/mysite/polls/Airbnb_data/tomslee_airbnb_barcelona_1477_2017-07-23.csv"
dataReader = csv.reader(open(csv_filepathname, errors= 'ignore'), delimiter=',', quotechar='"', )
for row in dataReader:
    print (row)
    if row[0] != 'room_id':
        # Ignore the header row, import everything else
        Alist = Airbnb_listing()
        Alist.room_id = row[0]
        Alist.survey_id = row[1]
        Alist.host_id = row[2]
        Alist.room_type = row[3]
        Alist.country = row[4]
        Alist.city = row[5]
        Alist.borough = row[6]
        Alist.neighborhood = row[7]
        Alist.reviews = row[8]
        Alist.overall_satisfaction = row[9]
        Alist.accommodates = row[10]
        Alist.bedrooms = row[11]
        Alist.bathrooms = row[12]
        Alist.price = row[13]
        Alist.minstay = row[14]
        Alist.name = row[15]
        Alist.last_modified  = row[16]
        Alist.latitude = row[17]
        Alist.longitude = row[18]
        Alist.save()
