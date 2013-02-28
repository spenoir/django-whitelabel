"""Management utilities."""


from fabric.contrib.console import confirm
from fabric.api import abort, env, local, settings, task


########## GLOBALS
env.run = 'heroku run python manage.py'
env.local = 'python manage.py'

HEROKU_ADDONS = (
    'cloudamqp:lemur',
    'heroku-postgresql:dev',
    'scheduler:standard',
    'memcache:5mb',
    'newrelic:standard',
    'pgbackups:auto-month',
    'sentry:developer',
)
########## END GLOBALS


@task
def install_addons():
    for addon in HEROKU_ADDONS:
        cont('heroku addons:add %s' % addon,
            "Couldn't add %s to your Heroku app, continue anyway?" % addon)


@task
def dumpdata(dev=None):
    if dev:
        env.run = env.local
    local('%(run)s dumpdata pages --indent=4 > whitelabel/apps/pages/fixtures/initial_data.json' % env)
    local('%(run)s dumpdata zinnia --indent=4  > whitelabel/apps/base/fixtures/zinnia.json' % env)
    local('%(run)s dumpdata auth.user --indent=4  > whitelabel/apps/base/fixtures/users.json' % env)
    local('%(run)s dumpdata tagging --indent=4  > whitelabel/apps/base/fixtures/tags.json' % env)
    local('%(run)s dumpdata sites --indent=4  > whitelabel/apps/base/fixtures/sites.json' % env)
    local('git commit -am"latest data dumps from prod"')


@task
def loaddata(dev=None):
    if dev:
        env.run = env.local
    local('%(run)s loaddata pages --indent=4 > whitelabel/apps/pages/fixtures/initial_data.json' % env)
    local('%(run)s loaddata zinnia --indent=4  > whitelabel/apps/base/fixtures/zinnia.json' % env)
    local('%(run)s loaddata auth.user --indent=4  > whitelabel/apps/base/fixtures/users.json' % env)
    local('%(run)s loaddata tagging --indent=4  > whitelabel/apps/base/fixtures/tags.json' % env)
    local('%(run)s dumpdata sites --indent=4  > whitelabel/apps/base/fixtures/sites.json' % env)


@task
def deploystatic():
    """ collects static files from media generator and commits/deploys """
    local('rm -rf _generated_media*')
    local('python manage.py generatemedia')
    local('git add _generated_media*')
    local('git commit -am"adding latest generated media"')
    local('git push heroku master')
    local('%(run)s collectstatic --noinput -iapps -idjango_extensions -idebug_toolbar -imustachejs -itiny_mce -ijquery-ui -isite-packages -ickeditor -izinnia -iadmin -id3' % env)

@task
def collectstatic():
    """ collects static files """
    local('%(run)s collectstatic --noinput -iapps -django_extensions -idebug_toolbar -imustachejs -itiny_mce -ijquery-ui -isite-packages -ickeditor -izinnia -iadmin -id3' % env)


########## HELPERS
def cont(cmd, message):
    """Given a command, ``cmd``, and a message, ``message``, allow a user to
    either continue or break execution if errors occur while executing ``cmd``.

    :param str cmd: The command to execute on the local system.
    :param str message: The message to display to the user on failure.

    .. note::
        ``message`` should be phrased in the form of a question, as if ``cmd``'s
        execution fails, we'll ask the user to press 'y' or 'n' to continue or
        cancel exeuction, respectively.

    Usage::

        cont('heroku run ...', "Couldn't complete %s. Continue anyway?" % cmd)
    """
    with settings(warn_only=True):
        result = local(cmd, capture=True)

    if message and result.failed and not confirm(message):
        abort('Stopped execution per user request.')
########## END HELPERS


########## DATABASE MANAGEMENT
@task
def syncdb():
    """Run a syncdb."""
    local('%(run)s syncdb --noinput' % env)


@task
def migrate(app=None):
    """Apply one (or more) migrations. If no app is specified, fabric will
    attempt to run a site-wide migration.

    :param str app: Django app name to migrate.
    """
    if app:
        local('%s migrate %s --noinput' % (env.run, app))
    else:
        local('%(run)s migrate --noinput' % env)
########## END DATABASE MANAGEMENT


########## HEROKU MANAGEMENT
@task
def bootstrap():
    """Bootstrap your new application with Heroku, preparing it for a production
    deployment. This will:

        - Create a new Heroku application.
        - Install all ``HEROKU_ADDONS``.
        - Sync the database.
        - Apply all database migrations.
        - Initialize New Relic's monitoring add-on.
    """
    cont('heroku create', "Couldn't create the Heroku app, continue anyway?")

    for addon in HEROKU_ADDONS:
        cont('heroku addons:add %s' % addon,
            "Couldn't add %s to your Heroku app, continue anyway?" % addon)

    cont('git push heroku master',
            "Couldn't push your application to Heroku, continue anyway?")

    syncdb()
    migrate()

    cont('%(run)s newrelic-admin validate-config - stdout' % env,
            "Couldn't initialize New Relic, continue anyway?")


@task
def destroy():
    """Destroy this Heroku application. Wipe it from existance.

    .. note::
        This really will completely destroy your application. Think twice.
    """
    local('heroku apps:destroy')
########## END HEROKU MANAGEMENT
