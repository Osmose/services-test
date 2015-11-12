import os

if os.getenv('APP_NAME'):
    APP_NAME = os.getenv('APP_NAME')
    BUILD_NUMBER = os.getenv('BUILD_NUMBER')

else:
    APP_NAME = 'Nightly'
    BUILD_NUMBER = '000'

OS = Env.getOS()
OS_VERSION = Settings.getOSVersion()

print Env.getSikuliVersion()
print('OS: %s - %s' % (OS, OS_VERSION))

if Settings.isWindows():
    # IF Windows 10 or Windows 2012 (6.3)
    if OS_VERSION == '10.0' or OS_VERSION == '6.3':
        if APP_NAME == 'Nightly':
            PATH_IMGS = '../images_nightly64/'
            PATH_BIN = 'C:/Program Files'
        else:
            PATH_IMGS = '../images_release32/'
            PATH_BIN = 'C:/Program Files (x86)'
            print "no images found for this OS - ABORTING!"
            exit(1) 
    else:
        print 'Not windows 10 or Windows 2012'
        exit(1)

elif Settings.isLinux():
    print "no images found for this OS - ABORTING!"
    exit(1)

elif Settings.isMac():
    print 'no images found for this OS - ABORTING!'
    exit(1)

else:
    print 'OS not recognized - ABORTING!'
    exit(1)

URL_TEST_PAGE = 'https://pdehaan.github.io/push-notification-test'
PATH_PROFILE = 'C:/Jenkins/workspace/autopush_e2e-test_prod/services-test/autopush/e2e-test/tests/prefs/prefs.js'             
NIGHTLY64 = '%s/%s/firefox.exe -height 768 -width 1024' % (PATH_BIN, APP_NAME)
PATH_FIREFOX = NIGHTLY64
URL_SEARCH = PATH_IMGS + 'url_search.png'
IMG_REFRESH = PATH_IMGS + 'btn_refresh.png'
IMG_ALWAYS_RECEIVE_NOTIFICATIONS = PATH_IMGS + 'btn_always_receive.png'
IMG_BTN_POP_NOTIFICATION = PATH_IMGS + 'btn_pop_notification.png' 
IMG_WIN_POP_NOTIFICATION = PATH_IMGS + 'win_pop_notification.png' 
LINE = '--------------------------'

BIN_MINICAP = 'C:\\Program Files (x86)\\MiniCap\\MiniCap.exe'
PATH_SCREENSHOTS = 'C:\\Jenkins\\workspace\\screenshots'
URL_SCREENSHOTS = 'https://services-qa-jenkins.stage.mozaws.net:8443/job/screenshots/ws'
firefox = App(APP_NAME)

"""
Take a screenshot using MiniCap.exe.
"""
def screenshot(function_name = ''):
    from subprocess import Popen, PIPE
    # global screenshot_counter
    print('taking screenshot')
    suffix = '%s_$uniquenum0$%s' % (BUILD_NUMBER, function_name)
    name_screenshot = '%s\\screenshot_%s.jpg' % (PATH_SCREENSHOTS, suffix)
    cmd = [BIN_MINICAP, '-capturescreen', '-exit', '-closeapp', '-save', name_screenshot] 
    # the MiniCap vars break the following line:
    #print('%s/screenshot_%s.jpg' % (URL_SCREENSHOTS, '%s_$uniquenum0$%s' % (BUILD_NUMBER, function_name)))
    proc = Popen(cmd, stdout=PIPE)
    output = proc.communicate()[0]
    print output
    # screenshot_counter += 1


"""
Log an error, take a screenshot of the current state, and exit with an error code.
"""
def exit_with_screenshot(e, function_name=''):
    print 'ERROR: %s' % e
    screenshot('_error%s' % function_name)
    exit(1)


"""
Print an easy to read header to the log.
"""
def print_header(label):
    print '%s\n%s\n%s' % (LINE, label, LINE)


"""
Shared test setup.
"""
def setup():
    print_header('SETUP')
    try:
        firefox.open(PATH_FIREFOX)
        sleep(3)
        firefox.focus()
    except FindFailed as e:
        exit_with_screenshot(e, '_firefox_open')

    print_header('BEGIN TEST')


"""
Shared test teardown.
"""
def teardown():
    print_header('TEARDOWN')
    print 'closing browser now'
    try:
        type('w', Key.SHIFT + Key.CTRL)
    except FindFailed as e:
        exit_with_screenshot(e, '_teardown')
    
    print('Firefox closed')
    print('TEST COMPLETE!')


"""
Open the specified URL in Firefox.
"""
def enter_url(url = URL_TEST_PAGE):
    print('ENTER URL')
        # Focus on Firefox address bar
    type("l", Key.CTRL)
    try:
        click(URL_SEARCH)
    except FindFailed as e:
        exit_with_screenshot(e, '_url_test_page')
    type(url + Key.ENTER) 


"""
Make sure that Firefox can receive desktop notifications.
"""
def always_receive_notifications():
    print('PERMISSIONS: <Always Receive Notifications?>')
    try:
        if exists(IMG_ALWAYS_RECEIVE_NOTIFICATIONS):
            click(IMG_ALWAYS_RECEIVE_NOTIFICATIONS)
    except FindFailed as e:
        exit_with_screenshot(e, '_always_receive_notifications')


"""
Click the popup notification button in our test app.
"""
def click_button_pop_notification():
    try:
        click(IMG_BTN_POP_NOTIFICATION)
        sleep(2)
    except FindFailed as e:
        exit_with_screenshot(e, '_btn_pop_notification')



"""
Verify the pop notification was displayed (and auto-closed).
"""
def verify_pop_notification():
    print "POP NOTIFICATION: ???"
    try:
        wait(IMG_WIN_POP_NOTIFICATION, 10)
        screenshot('_success')
    except FindFailed as e:
        exit_with_screenshot(e, '_verify_pop_notification')
    
    print('POP NOTIFICATION: COMPLETE!')
    print('POP NOTIFICATION: WAITING FOR VANISH.....')

    try:
        waitVanish(IMG_WIN_POP_NOTIFICATION, 10)
    except FindFailed as e:
        exit_with_screenshot(e, '_verify_vanish_pop_notification')


setup()
enter_url()
click_button_pop_notification()
always_receive_notifications()
verify_pop_notification()
teardown()
