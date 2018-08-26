I. Webium
====================================================
Orginal: http://wgnet.github.io/webium/index.html
Maintained by: jacob@vsee.com


II. vsee.properties
To customize the way the tests are run 

# webdriver.driver
	What browser do you want your tests to run in, for example firefox, chrome, phantomjs or iexplorer. You can also use the driver property as a shortcut.

# webdriver.base.url
	The default starting URL for the application, and base URL for relative paths.

# webdriver.chrome.driver
	Path to the Chrome driver, if it is not on the system path.

# webdriver.firefox.driver
	Path to the Gecko driver, if it is not on the system path.

# webdriver.timeouts.implicitlywait
	How long webdriver waits for elements to appear by default, in seconds.

# chrome.switches
	Arguments to be passed to the Chrome driver, separated by commas. Example: chrome.switches = --incognito;--disable-download-notification

# firefox.activate.firebugs
	Activate the Firebugs and FireFinder plugins for Firefox when running the WebDriver tests. This is useful for debugging, but is not recommended when running the tests on a build server.

# browser.width and browser.height
    Resize the browser to the specified dimensions, in order to take larger screenshots. This should work with Firefox and Chrome, but not with others

# browser.x and browser.y
    Sets the x,y position of the current window.

# vsee.take.screenshots
    FOR_EACH_ACTION : take screenshots for every clicked button and every selected link [Pending]
    BEFORE_AND_AFTER_EACH_STEP
    AFTER_EACH_STEP
    FOR_FAILURES : only store screenshots for failing steps
    DISABLED

# vsee.record.video
    Making a gif. Should use this mode with vsee.take.screenshots = BEFORE_AND_AFTER_EACH_STEP / AFTER_EACH_STEP
    TURN_ON / TURN_OFF

# vsee.clean.log
    YES / NO
    Delete files in the folder that has name is testcaseID before executing the script

