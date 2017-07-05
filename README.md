# Challenge:

Create a command line program that will take an internet domain name (i.e. "www.jana.com") and print out a list of the email addresses that were found on the website at that host name only.

## Example:

The following is _expected_ output from www.jana.com and web.mit.edu, but it should also run on other websites. In the example of www.jana.com, the program should not crawl other subdomains (blog.jana.com, technology.jana.com).

```
# These are expected output from www.jana.com
> python find_email_addresses.py www.jana.com
Found these email addresses:
sales@jana.com
press@jana.com
info@jana.com

(**Note:** there is one broken link: mailto:%20press@jana.com that wasn't
mentioned in the initial challenge that isn't stripped from the results)

# Here are some examples from web.mit.edu (subject to change)
> python find_email_addresses.py web.mit.edu
Found these email addresses:
campus-map@mit.edu
mitgrad@mit.edu
sfs@mit.edu
llwebmaster@ll.mit.edu
webmaster@ll.mit.edu
whatsonyourmind@mit.edu
fac-officers@mit.edu
```

## More information:

- You can use any modern programming language you like. We work in Python and Java, so one of those is preferred but not required.
- Create a new github repository for this project. The repository should be public but please give it some kind of codename that doesn't have the word `jana` in it. The master branch should be empty, and then create a branch with your code in it.
- Push your branch up to github, and create a pull request. Send me the link to the pull request, and I can comment directly on it. All our code goes through this code review process, so it's a little glimpse into how we work.
- In your repo, please include a readme that has any instructions we might need to setup and install your solution.
- Your program must work on another computer, so be sure to include any required libraries (using libraries is OK). You do not need to check in the source for those libraries. Build scripts and/or a requirements.txt file would be preferred.

## Hints:

- Make sure to find email addresses on any discoverable page of the website, not just the home page.

## Style:

- At Jana we follow the Google Style Guides for Python and Java. However, it is not critical for this challenge.

## Installing and Running

### Prerequisites

- The following software is required to run:

  - Python
  - Java
  - Selenium standalone server
  - Optional:
    - Chrome and ChromeDriver, required for JavaScript execution

    - Note that in some cases Chrome is more stable than the HTMLUNIT driver

### Installation

- First make sure that Java is installed _didn't have time to write up install instructions_
- Download [Selenium standalone server](https://selenium-release.storage.googleapis.com/3.4/selenium-server-standalone-3.4.0.jar)
- Install Selenium bindings for Python with:

  `$ pip install selenium`
- To scrape more complex pages, it is suggested to use Chrome and ChromeDriver
  - Download and install Chrome from [Google](http://google.com/chrome)
  - Download and install [ChromeDriver](https://sites.google.com/a/chromium.org/chromedriver/downloads) to somewhere in your PATH

- Start Selenium server if Chrome isn't being used:

    `$ java -jar ./selenium-server-standalone-3.4.0.jar`

  - **NOTE:** this server is buggy and may hang, so it may require restarts

### Running

- This script uses [Selenium WebDriver](http://www.seleniumhq.org/projects/webdriver/)'s [Python bindings](http://selenium-python.readthedocs.io/index.html)

  - By default, it will use the HTMLUNIT driver, which is somewhat unstable, use --chrome flag if it isn't working

- Execute:

  `$ python find_email_addresses.py <host name>`
- For additional debugging output, add '--verbose'

### Caveats

- This has only been tested under Linux, though it should run on any other systems that support the required dependencies
- I ran low on time, so this isn't fully debugged and several items I wanted to fix weren't done:
  - timing out if we haven't heard back from WebDriver in a few seconds
  - automatically launch/kill the Selenium server (there might even be builtin functionality in the Python bindings to do this, didn't get a chance to look)
  - put Browser-MobProxy between Selenium and the Internet to allow for:

    - more insight into HTTP, so Content-Type can be checked before attempting to inject JavaScript or search the DOM

  - URLs with fragment identifiers are not de-duped if the rest of the URL has already been loaded, e.g. <http://w3.org/#foo> will still load, even if <http://w3.org> has been visited already
  - documentation and test cases are desperately needed

- There's very little error handling! --verbose will help to see if it's currently running
- See [sample output](sample-output.txt) and [verbose sample output](sample-output-verbose.txt) for example results
- This is my first Python program in years, so I'm a little rusty and I'm not familiar with all of the latest bells and whistles introduced in the latest versions of the language
