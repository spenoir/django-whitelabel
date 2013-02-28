Deployment
----------

1. python manage.py importsassframeworks
2. python manage.py generatemedia
3. python manage.py collectstatic
4. python manage.py runserver 8003 --nothreading

This is process for deploying latest static files if styles need updating on live.

1. rm _generated_media/*.css _generated_media/*.js _generated_media_names.py
2. python manage.py generatemedia
3. git add _generated_media/*
4. git commit -am'adding latest generated media'
5. git push heroku master
6. heroku run python manage.py collectstatic --noinput -i ckeditor/* -i zinnia/* -i admin/* -i d3/examples/*
