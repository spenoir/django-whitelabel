MEDIA_BUNDLES = (
    # base utli js libs
    ('jquery.js',
        'js/jquery-1.7.2.js',
        'js/jquery-ui-1.8.16.custom.min.js',
    ),

    ('application.js',
#        {'filter': 'mediagenerator.filters.concat.Concat',
#         'dev_output_name': 'app-dev.js',
#         'concat_dev_output': True,
#         'input': (

            # libs and base classes
            'js/json2.js',
            'js/underscore.js',
            'js/mustache.js',
            'mustache/js/django.mustache.js',
            'js/backbone.js',
            'js/backbone-tastypie.js',
            'js/jquery.url.js',
            'js/uidev.js',
            'js/router.js',
            'js/models.js',
            'js/collections.js',

            # apps
            'js/models_pages.js',
            'js/collections_pages.js',
            'js/views/base.js',
            'js/views/page.js',
            'js/views/gallery.js',
            'js/views/home.js',
#            )
#        }
    ),

    ('styles.css',
        'css/jquery-ui/ui-darkness/jquery-ui-1.8.16.custom.css',
        'sass/pages.sass',
    ),
)