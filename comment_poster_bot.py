from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import undetected_chromedriver as UC
import time, random, os, string
import pywin

''' Comment Poster Bot class'''
class CommentBot:
    ''' Constructor accepts the following keyword args: \n
         -> bool static_page \n
         -> str video_link   \n
         -> bool comment_on_video \n
         -> str video_link        \n
         -> bool comment_on_channel \n
         -> str channel_link        \n
         -> bool comment_on_playlist \n
         -> str playlist_link \n
         -> bool comment_on_term \n
         -> str search_term'''
    def __init__(self, **kwargs):
        self.page_src = None

        #Set options and chdr pth
        self.PATH = 'REQS/chromedriver.exe'
        self.options = Options()
        self.options.add_argument("user-data-dir=path_to_store_user_data")
        # self.options.add_experimental_option("useAutomationExtension", False)
        self.options.add_experimental_option("excludeSwitches", ["enable-automation", "disable-popup-blocking"])
        self.options.add_argument("--log-level-3")
        # self.options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64)")
        self.options.add_argument("--disable-notifications")

        # Kwargs args validation
        if kwargs.get('static_page') is True:
            self.page_src = kwargs['video_link']

        elif kwargs.get('comment_on_video') is True:
            # if 'youtube.com' not in kwargs['video_link']:
            #     raise ValueError("Link must be a youtube link. If the link is compressed, uncompress it")

            self.page_src = kwargs['video_link']

        elif kwargs.get('comment_on_channel') is True:
            self.page_src = kwargs['channel_link']

        elif kwargs.get('comment_on_playlist') is True:
            self.page_src = kwargs['playlist_link']

        elif kwargs.get('comment_on_term') is True:
            link = f'https://www.youtube.com/results?search_query={kwargs["search_term"]}&sp=EgIQAQ%253D%253D'
            self.page_src = link

        elif kwargs.get('setup_account') is True:
            self.page_src = "https://google.com"

        else:
            raise ValueError("Invalid argument")

        # Instantiate driver
        self.driver = webdriver.Chrome(self.PATH, options=self.options)
        self.driver.get(self.page_src)
        self.driver.maximize_window()

    # Quit driver
    def driver_quit(self):
        ''' Ends driver session '''
        self.driver.quit()

    # Bot methods
    def is_shorts(self, url):
        if 'shorts' in url:
            return True

        else:
            return False

    def scroll(self, len_):
        ''' Scrolls down page to specific length
        :argument len_ Length to scroll'''
        time.sleep(0.5)

        page_handle = WebDriverWait(self.driver, 3).until(
            EC.presence_of_element_located((By.TAG_NAME, "html"))
        )

        for _ in range(len_):
            page_handle.send_keys(Keys.DOWN)

    def post_single_comment(self, comments):
        ''' Posts a single comment to a video '''
        self.scroll(random.randint(15, 18))
        time.sleep(0.7)

        # Select comment from list
        random_comment = comments[random.randint(0, len(comments) - 1)]

        # Render the comment box
        try:
            comment_box_unrendered = WebDriverWait(self.driver, 8).until(
                EC.presence_of_element_located((By.ID, 'placeholder-area'))
            ).click()

        except Exception as E:
            self.driver.quit()
            print("Comments disabled on video")

        time.sleep(1.2)

        input_box = WebDriverWait(self.driver, 5).until(
            EC.presence_of_element_located((By.ID, 'contenteditable-root'))
        )

        # Send comment to input box (simulate human typing)
        for _ in random_comment:
            time.sleep(random.uniform(0.001, 0.018))
            input_box.send_keys(_)

            if random.randint(1, 9) % 3 == 0:
                input_box.send_keys(random.choices(string.ascii_lowercase, k=1))
                input_box.send_keys(Keys.BACK_SPACE)

        input_box.send_keys(random.randint(0, 9))
        input_box.send_keys(Keys.BACK_SPACE)

        time.sleep(0.9)
        input_box.send_keys(Keys.CONTROL, Keys.ENTER)

    def reply_to_commment(self, comments, comment_count):
        self.scroll(random.randint(20,
                                   21))
        time.sleep(0.3)

        comment_pos = 1
        cc_count = 0
        for _ in range(comment_count):
            try:
                reply_button = WebDriverWait(self.driver, 5).until(
                    EC.presence_of_element_located((By.XPATH, f"/html/body/ytd-app/div[1]/ytd-page-manager/ytd-watch-flexy/div[5]/div[1]/div/div[2]/ytd-comments/ytd-item-section-renderer/div[3]/ytd-comment-thread-renderer[{comment_pos}]/ytd-comment-renderer/div[3]/div[2]/ytd-comment-action-buttons-renderer/div[1]/div[4]/ytd-button-renderer/a/tp-yt-paper-button/yt-formatted-string"))
                ).click()

                time.sleep(0.4)

                comment_box = WebDriverWait(self.driver, 5).until(
                    EC.presence_of_element_located((By.XPATH, f"/html/body/ytd-app/div[1]/ytd-page-manager/ytd-watch-flexy/div[5]/div[1]/div/div[2]/ytd-comments/ytd-item-section-renderer/div[3]/ytd-comment-thread-renderer[{comment_pos}]/ytd-comment-renderer/div[3]/div[2]/ytd-comment-action-buttons-renderer/div[2]/ytd-comment-reply-dialog-renderer/ytd-commentbox/div[2]/div/div[2]/tp-yt-paper-input-container/div[2]/div/div[1]/ytd-emoji-input/yt-user-mention-autosuggest-input/yt-formatted-string/div"))
                )

                random_comment = comments[random.randint(0, len(comments) - 1)]

                for char in random_comment:
                    time.sleep(random.uniform(0.003, 0.02))
                    comment_box.send_keys(char)

                    if random.randint(1, 14) % 4 == 0:
                        comment_box.send_keys(random.choices(string.ascii_lowercase, k=1))
                        comment_box.send_keys(Keys.BACK_SPACE)

                cc_count = cc_count + 1

                time.sleep(0.5)
                comment_box.send_keys(Keys.CONTROL, Keys.ENTER)

                if cc_count >= 2:
                    self.scroll(8)

                comment_pos = comment_pos + 1
                time.sleep(1)

            except Exception as E:
                self.driver.quit()
                print("No comments left")
                break

    def comment_on_channel(self, comments, video_count, reply=(False, 0)):
        ''' Posts videos to specified count of videos on a channel'''
        video_pos = 1
        for _ in range(video_count):
            try:
                video = WebDriverWait(self.driver, 5).until(
                    EC.presence_of_element_located((By.XPATH, f'/html/body/ytd-app/div[1]/ytd-page-manager/ytd-browse/ytd-two-column-browse-results-renderer/div[1]/ytd-section-list-renderer/div[2]/ytd-item-section-renderer/div[3]/ytd-grid-renderer/div[1]/ytd-grid-video-renderer[{video_pos}]/div[1]'))
                ).click()

                if self.is_shorts(self.driver.current_url):
                    self.driver.refresh()

                time.sleep(0.8)

                if reply[0] is True:
                    self.reply_to_commment(comments, comment_count=reply[1])

                else:
                    self.post_single_comment(comments)

                time.sleep(2)
                self.driver.back()

            except Exception as E:
                self.driver.quit()
                print("No videos left")
                break

            video_pos = video_pos + 1

    def comment_on_search_term(self, comments, video_count, reply=(False, 0)):
        video_pos = 1

        for _ in range(video_count):
            try:
                video = WebDriverWait(self.driver, 5).until(
                    EC.presence_of_element_located((By.XPATH, f'/html/body/ytd-app/div[1]/ytd-page-manager/ytd-search/div[1]/ytd-two-column-search-results-renderer/div[2]/div/ytd-section-list-renderer/div[2]/ytd-item-section-renderer/div[3]/ytd-video-renderer[{video_pos}]/div[1]/div/div[1]/div'))
                ).click()

                if self.is_shorts(self.driver.current_url):
                    self.driver.refresh()

                if reply[0] is True:
                    self.reply_to_commment(comments, reply[1])

                else:
                    self.post_single_comment(comments)

                time.sleep(2)
                self.driver.back()

            except Exception as E:
                print("No videos left")
                self.driver.quit()
                break

            video_pos = video_pos + 1
