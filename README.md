This is an API project that allows the uploading and display of images in PNG or JPG format.

To set up this project you need to:
- type: "docker-compose up"
- make and push migrations
- type "python manage.py loaddata initial_data.json" to create 3 types of tiers (Basic, Premium, and Enterprise) in the database. (If this doesn't work you must make them manually according to the JSON file via the admin panel, validation should prevent you from doing this wrong!)
- create a user and set an account type for him!


There are two endpoints:
- localhost/upload
- localhost/images

You can add photos via curl command like: "curl -X POST -H "Authorization: Basic $(echo -n '<username>:<password>' | base64)" -H "Content-Disposition: attachment; filename=<filename>" --data-binary "@<path to photo>" http://localhost:8000/upload/"

Once you upload the photo there will be made a few folders for the user that uploaded the photo and there will be created multiple folders and pictures in it, for all tiers and all thumbnail types per tier. They are filtered in serializer to display user data according to his account type.