#next time just change the .csv file below and put in the views.py vote function
csv_filepathname="/Users/Erika/Documents/2017-2018 Senior/Databases/dbproject2017/djangoProj/mysite/polls/tomslee_airbnb_boston_1429_2017-07-10.csv"
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
