import os
import shutil
from datetime import datetime
from invoke import task, run

try:
    import urllib2 as urequest
    import urllib as uparse
except ImportError:
    import urllib.request as urequest
    import urllib.parse as uparse


# === Settings ===

# Project directories
_site_dest = "./_site/"       # Dir where Jekyll will generate site
_posts_dest = "./_posts/"     # Dir with posts
_drafts_dest = "./_drafts/"   # Dir with drafts

# Global options
_hostname = '127.0.0.1'       # Listen given hostname
_port = '4000'                # Listen given port
_bundle_exec = False          # Run commands with Bundler
_fpolling = False             # Force watch to use polling
_incremental = False          # Enable incremental build (Jekyll 3 and higher!)

# Post settings
_post_ext = '.md'             # Post files extension

# Notification settings (your sitemap location)
_sitemap_url = 'http://www.example.com/sitemap.xml'


# == Helpers ===

build_help = {
    'drafts': "Build site including draft posts.",
    'bundle-exec': "Build site via Bundler.",
    'incremental-build': "Rebuild only posts and pages that have changed."
}

serve_help = {
    'drafts': "Process and render draft posts.",
    'bundle-exec': "Run Jekyll development server via Bundler.",
    'force-polling': "Force watch to use polling.",
    'incremental-build': "Rebuild only posts and pages that have changed."
    }

doctor_help = {
    'bundle-exec': "Run doctor via Bundler."
}

list_help = {
    'drafts': "Include draft posts."
}

post_help = {
    'title': "Post title.",
    'drafts': "Create draft post."
}

notify_help = {
    'google': "Notify Google about sitemap updates.",
    'bing': "Notify Bing about sitemap updates."
}


# === Tasks ===

@task(help=build_help)
def build(drafts=False, bundle_exec=_bundle_exec,
          incremental_build=_incremental):
    """Build the site.

    jekyll build [options]
    """
    core_command = 'jekyll build'
    exec_lst = [core_command]

    # Icluding _site_dest
    exec_lst.append('-d ' + _site_dest)

    # Parsing options
    if bundle_exec:
        exec_lst.insert(0, 'bundle exec')
    if incremental_build:
        exec_lst.append('-I')
    if drafts:
        exec_lst.append('--drafts')

    # Print options and execute resulted command
    printer(exec_lst)
    # run(' '.join(exec_lst))


@task(help=serve_help)
def serve(drafts=False, bundle_exec=_bundle_exec,
          force_polling=_fpolling, incremental_build=_incremental):
    """Serve the site locally.

    jekyll serve [options]
    """
    core_command = 'jekyll serve'
    exec_lst = [core_command]

    # Icluding _site_dest
    exec_lst.append('-d ' + _site_dest)

    # Listening given port and hostname
    exec_lst.append('--host ' + _hostname)
    exec_lst.append('--port ' + _port)

    # Parsing options
    if bundle_exec:
        exec_lst.insert(0, 'bundle exec')
    if incremental_build:
        exec_lst.append('-I')
    if drafts:
        exec_lst.append('--drafts')
    if force_polling:
        exec_lst.append('--force_polling')

    # Print options and execute resulted command
    printer(exec_lst)
    # run(' '.join(exec_lst))


@task
def clean():
    """Clean the site.

    Removes site output and metadata file without building.
    """
    print("\nCleaning the site from {}\n".format(_site_dest))
    rm(_site_dest)


@task(help=doctor_help)
def doctor(bundle_exec=_bundle_exec):
    """Search site and print specific deprecation warnings.

    jekyll doctor
    """
    core_command = 'jekyll doctor'
    exec_lst = [core_command]

    # Parsing options
    if bundle_exec:
        exec_lst.insert(0, 'bundle exec')

    # Print options and execute resulted command
    printer(exec_lst)
    # run(' '.join(exec_lst))


@task(help=list_help)
def list(drafts=False):
    """List all posts."""
    print("\nListing posts...\n")
    ls(_posts_dest)
    print("")

    if drafts:
        print("Listing drafts...\n")
        ls(_drafts_dest)
        print("")


@task(help=post_help)
def post(title, drafts=False):
    """Create a new post."""
    # Parsing options
    if drafts:
        dest = _drafts_dest
    else:
        dest = _posts_dest

    # File name
    date = get_date()
    name = sanitize(title)
    fname = "{}-{}{}".format(date, name, _post_ext)

    # Front Matter
    front_matter = []
    front_matter.append('---')
    front_matter.append('layout: post')
    front_matter.append('title: {}'.format(title))
    front_matter.append('---')

    # Create post file and write Front Matter
    print("\nCreating new post '{}' in {}\n".format(fname, dest))
    try:
        f = open(dest + fname, 'w')
    except FileNotFoundError:
        print("* [Error]: directory '{}' does not exist!\n".format(dest))
    else:
        f.write('\n'.join(front_matter))
        f.close()
        print("* Done.\n")


@task(help=notify_help)
def notify(google=False, bing=False):
    """Notify various services about sitemap update."""
    if google:
        base_url = 'http://www.google.com/webmasters/sitemaps/ping'
        params = {'sitemap': _sitemap_url}
        ping_sitemap(base_url, params)
    if bing:
        base_url = 'http://www.bing.com/webmaster/ping.aspx'
        params = {'siteMap': _sitemap_url}
        ping_sitemap(base_url, params)

    if not (google or bing):
        print("\n* Specify service(s) to ping.")
        print("* type: 'invoke --help notify'")
        print("* for the list of available options.\n")


# === Helper functions ===

def sanitize(str):
    """Align post title to the Jekyll post name requirements."""
    res = str.lower()
    return res.replace(' ', '-')


def get_date():
    """Get current date in YEAR-MONTH-DAY format."""
    dt = datetime.now()
    return dt.strftime("%Y-%m-%d")


def ping_sitemap(base_url, params):
    """Submit sitemap."""
    url_values = uparse.urlencode(params)
    full_url = base_url + '?' + url_values
    req = urequest.Request(full_url)

    print("\nSubmitting sitemap to {}\n".format(base_url))
    try:
        urequest.urlopen(req)
        print("* Done.\n")
    except Exception as e:
        print("* [Error] occured: {}\n".format(e))


def ls(path):
    """Print dir contents."""
    try:
        item_lst = os.listdir(path)
    except Exception as e:
        print("* [Error] occured: {}\n".format(e))
    else:
        for item in item_lst:
            print(item)


def rm(path):
    """Recursively delete a directory tree."""
    try:
        shutil.rmtree(path)
    except Exception as e:
        print("* [Error] occured: {}\n".format(e))
    else:
        print("* Done.\n")


def printer(exec_lst):
    # Core commands
    if 'jekyll build' in exec_lst:
        print("\nBuilding the site in {}\n".format(_site_dest))
    if 'jekyll serve' in exec_lst:
        print("\nServing the site in {}\n".format(_site_dest))
    if 'jekyll doctor' in exec_lst:
        print(
            "\nChecking site for compatibility problems and URL conflicts...\n"
            )

    # Options
    if '--host ' + _hostname in exec_lst:
        print(
            "* Starting Jekyll development server at {}:{}".
            format(_hostname, _port)
            )
    if 'bundle exec' in exec_lst:
        print("* Running via Bundler...")
    if '-I' in exec_lst:
        print("* Enabling incremental build (Jekyll 3 and higher only)...")
    if ('--drafts' in exec_lst) or (_drafts_dest in exec_lst):
        print("* Including drafts...")
    if '--force_polling' in exec_lst:
        print("* Forcing watch to use polling...")

    # Printing resulted command
    print("\n>>> " + ' '.join(exec_lst) + "\n")
