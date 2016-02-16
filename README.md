jtasks: a swiss knife for Jekyll projects
=========================================

**_jtasks_ (Jekyll tasks) is a collection of configurable [Invoke](http://www.pyinvoke.org/) tasks that provide simple, but powerful, interface to run both common and _advanced_ routines in your Jekyll projects.**

For example, let's run development server via [Bundler](http://bundler.io/), at host `0.0.0.0` (like in Jekyll 2), port `5000` (because I have multiple Jekyll projects served simultaneously), generate output into `dist` folder, including *drafts* and enabling *incremental build*:

```
# using jtasks:
$ invoke serve -bdi

# common way:
$ bundle exec jekyll serve --destination ./dist/ --host 0.0.0.0 --port 5000 --incremental --drafts
```

`--destination`, `--host` and `--port` are configured as global variables at the *settings* part of the script. This allows flexible setup of **jtasks** on per-project basis.


How to Use
----------

```
inv[oke] task1 [--task1-opts] ... taskN [--taskN-opts]
```

### Examples:

Build the site with Bundler:
```
$ inv build -b
```

Serve site with Bundler including draft posts:
```
$ inv serve -bd
```

Notify Google and Bing about your sitemap updates:
```
$ inv notify -gb
```

Create a new post with the given title:
```
$ inv post "My awesome post"
```

Start development server and fire up default browser to preview resulted site:
```
$ inv serve preview
```

List all posts and drafts:
```
$ inv list -d
```

Remove generated site:
```
$ inv clean
```

Check site for compatibility problems and URL conflicts:
```
$ inv doctor
```


Installation
------------

Copy *tasks.py* file into the base folder of your Jekyll site.

You also need *Python (2.7+ or 3.3+)* with [Invoke](http://www.pyinvoke.org/index.html) package:

* [Install Python](https://www.python.org/downloads/)
* [Install Invoke](http://www.pyinvoke.org/installing.html)


Configuration
-------------

All settings are available at the top of the *tasks.py* file:

```python
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
```

From the box, **jtasks** uses [Jekyll 3 default configuration settings](http://jekyllrb.com/docs/configuration/). They can be easily modified for your project-specific needs. E.g. if we always need to run all tasks via Bundler, it is possible to set `_bundle_exec = True` and now all tasks (where applicable) will be executed using `bundle exec`:

```
$ inv build

# Same as:
$ bundle exec jekyll build --destination ./_site/
```


Available tasks
---------------

Currently, following tasks are supported:

```
$ inv --list
Available tasks:

  build     Build the site.
  clean     Clean the site.
  doctor    Search site and print specific deprecation warnings.
  list      List all posts.
  notify    Notify various services about sitemap update.
  post      Create a new post.
  preview   Launches default browser for previewing generated site.
  serve     Serve the site locally.
```

### build

```
$ inv --help build
Docstring:
  Build the site.

  jekyll build [options]

Options:
  -b, --bundle-exec         Build site via Bundler.
  -d, --drafts              Build site including draft posts.
  -i, --incremental-build   Rebuild only posts and pages that have changed.
```

### serve

```
$ inv --help serve
Docstring:
  Serve the site locally.

  jekyll serve [options]

Options:
  -b, --bundle-exec         Run Jekyll development server via Bundler.
  -d, --drafts              Process and render draft posts.
  -f, --force-polling       Force watch to use polling.
  -i, --incremental-build   Rebuild only posts and pages that have changed.
```

### clean

```
$ inv --help clean
Docstring:
  Clean the site.

  Removes site output and metadata file without building.

Options:
  none
```

### doctor

```
$ inv --help doctor
Docstring:
  Search site and print specific deprecation warnings.

  jekyll doctor

Options:
  -b, --bundle-exec   Run doctor via Bundler.
```

### post

```
$ inv --help post
Docstring:
  Create a new post.

Options:
  -d, --drafts                Create draft post.
  -t STRING, --title=STRING   Post title.
```

### list

```
$ inv --help list
Docstring:
  List all posts.

Options:
  -d, --drafts   Include draft posts.
```

### notify

```
$ inv --help notify
Docstring:
  Notify various services about sitemap update.

Options:
  -b, --bing     Notify Bing about sitemap updates.
  -g, --google   Notify Google about sitemap updates.
```


### preview

```
$ inv --help preview
Docstring:
  Launches default browser for previewing generated site.

  `build` and/or `serve` tasks should be launched manually in advance,
  depending on desired options.

Options:
  none
```


License
-------

Distributed under the terms of the [MIT License](https://opensource.org/licenses/MIT).
