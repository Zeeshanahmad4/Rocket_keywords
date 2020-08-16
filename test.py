import os
import settings
import zipfile
from selenium import webdriver
import time
CHROME_EXT_MANIFEST = """
{
    "version": "1.0.0",
    "manifest_version": 2,
    "name": "%(name)s",
    "permissions": [
        "proxy",
        "tabs",
        "unlimitedStorage",
        "storage",
        "<all_urls>",
        "webRequest",
        "webRequestBlocking"
    ],
    "background": {
        "scripts": ["background.js"]
    },
    "minimum_chrome_version":"22.0.0"
}
"""
CHROME_PROXY_EXT = """
var config = {
    mode: "fixed_servers",
    rules: {
        singleProxy: {
            scheme: "http",
            host: "%(host)s",
            port: parseInt(%(port)s)
        },
        bypassList: ["localhost"]
    }
};
chrome.proxy.settings.set({value: config, scope: "regular"}, function() {});
function callbackFn(details) {
    return {
        authCredentials: {
            username: "%(username)s",
            password: "%(password)s"
        }
    };
}
chrome.webRequest.onAuthRequired.addListener(
    callbackFn,
    {urls: ["<all_urls>"]},
    ['blocking']
);
"""

def browser_factory(proxy_username, proxy_password, proxy_port, proxy_ip, account_username='', account_password='', account_user_agent=''):
    
    directory = os.path.join(settings.BASE_DIR, 'linkedln_testing')

    os.makedirs(directory, exist_ok=True)
    extension = os.path.join(settings.BASE_DIR, 'linkedln_testing', 'chrome_proxy.zip')

    manifest_json = CHROME_EXT_MANIFEST % {'name': os.path.splitext('chrome_proxy.zip')[0]}

    background_js = CHROME_PROXY_EXT % { 'username': proxy_username, 
                                            'password': proxy_password, 
                                            'port': proxy_port, 'host': proxy_ip}
                                            
    with zipfile.ZipFile(extension, 'w') as zp:
        zp.writestr("manifest.json", manifest_json)
        zp.writestr("background.js", background_js)

    options = webdriver.ChromeOptions()
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-web-security')
    options.add_argument('--disable-notifications')
    options.add_argument('--disable-gpu')
    options.add_argument('--disable-setuid-sendbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--disable-accelerated-2d-canvas')
    options.add_extension(extension)
    
    if account_username:
        temp_dir = settings.BROWSER_PROFILES
        user_dir_path = os.path.join(temp_dir, f'fli_scrapper_{account_username}')
        options.add_argument(f'--user-data-dir={user_dir_path}')

    prefs = {
        'profile.default_content_setting_values.notifications': 2,
        "profile.managed_default_content_settings.images": 1,
        "profile.default_content_settings.cookies": 1
    }
    
    options.add_experimental_option("prefs", prefs)
    caps = webdriver.DesiredCapabilities.CHROME.copy()
    for key, value in caps.items():
        options.set_capability(key, value)
    options.set_capability('pageLoadStrategy', 'none')
    
    if account_user_agent:
        user_agent = account_user_agent
    # else:
    #     user_agent = UserAgent.objects.all().order_by('?')[0]
    
    options.add_argument(f'user-agent={account_user_agent}')
        
    browser = webdriver.Chrome(
        desired_capabilities=caps,
        options=options
    )
    
    time.sleep(1)

    browser.set_window_size(1920, 768)
    
    
    return browser


browser = browser_factory("dev_leadme_ca","0e5a74d083","30001","2.56.114.194","Profile_2","Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.84 Safari/537.36")
browser.get("https://www.linkedin.com/")



