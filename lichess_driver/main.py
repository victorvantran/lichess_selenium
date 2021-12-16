# Lichess.org Testing with Selenium
# Christopher Ta				|   cta002@csu.fullerton.edu
# Brian Tan 				    |   brian388@csu.fullerton.edu
# Victor Tran				    |   victorvantran@csu.fullerton.edu

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys  # Gives access to input keys to interface with the website
from selenium.webdriver.common.by import By  # Allows us to identify the xpath of element
from selenium.webdriver.common.action_chains import \
    ActionChains  # Allows us to perform generic actions on modules such as hovering, clicking, etc.
from selenium.webdriver.support.ui import WebDriverWait # Allows us to stall the driver to wait for a particular element to load
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
import time  # Allows us to sleep for a certain number of seconds



CHROMEDRIVER_PATH = "E:\\chromedriver\\chromedriver.exe"
#CHROMEDRIVER_PATH = "D:\\Software Expert\\chromedriver.exe"
SERVICE = Service(CHROMEDRIVER_PATH)
MAX_WAIT_FOR_SECONDS = 10

class WebTester:
    driver = None
    action = None
    window_size = None

    def __init__(self):
        """ Initiate Selenium webdriver for Chrome """
        self.options = webdriver.ChromeOptions()
        self.options.add_experimental_option('excludeSwitches', ['enable-logging'])
        self.driver = webdriver.Chrome(service=SERVICE, options=self.options)
        self.chrome_window_maximize()
        self.window_size = self.driver.get_window_size()
        self.action = ActionChains(self.driver)


    def __del__(self):
        """ Close the driver """
        self.driver.close()

    def chrome_window_maximize(self):
        """ Maximize the chrome window """
        self.driver.maximize_window()

    def hover(self, xpath):
        """ Hover over an element based on a given xpath """
        element = self.driver.find_element(By.XPATH, xpath)
        self.action.move_to_element(element)
        self.action.perform()

    def hover_offset(self, xpath, x, y):
        """ Hover over an element based on a given xpath """
        element = self.driver.find_element(By.XPATH, xpath)
        self.action.move_to_element_with_offset(element, x, y)
        self.action.perform()

    def click_element(self, element):
        """ Click on an element based on a given element """
        self.action.move_to_element(element)
        self.action.click()
        self.action.perform()

    def click_element_offset(self, element, x, y):
        """ Click on an element based on a given element and offset """
        self.action.move_to_element_with_offset(element, x, y)
        self.action.click()
        self.action.perform()

    def click(self, xpath):
        """ Click on an element based on a given xpath """
        element = self.driver.find_element(By.XPATH, xpath)
        self.click_element(element)

    def click_offset(self, xpath, x, y):
        """ Click on an element based on a given xpath and offset """
        element = self.driver.find_element(By.XPATH, xpath)
        self.click_element_offset(element, x, y)

    def press_key(self, key):
        """ Press a key """
        self.action.send_keys(key)
        self.action.perform()

    def check_exists_by_xpath(self, xpath):
        """ If the xpath exists, return True. Otherwise, return false """
        try:
            self.driver.find_element(By.XPATH, xpath)
        except NoSuchElementException:
            return False
        return True

    def wait_for(self, xpath):
        """ Waits for an element, given by its xpath, to appear on the page before proceeding """
        try:
            element = WebDriverWait(self.driver, MAX_WAIT_FOR_SECONDS).until(
                EC.presence_of_element_located((By.XPATH, xpath))
            )
        except Exception as error:
            print('Error: {}'.format(error))
            self.driver.quit()


class LichessBoard:
    css = None
    driver = None
    state = None
    action = None

    piece_abbreviation = {
        'pawn': '',
        'knight': 'N',
        'bishop': 'B',
        'rook': 'R',
        'queen': 'Q',
        'king': 'K'
    }

    def __init__(self, driver, action, css):
        super().__init__()
        self.driver = driver
        self.action = action
        self.css = css
        self.state = dict()

    def get_board_orientation(self):
        board_properties = self.driver.find_element(By.CSS_SELECTOR, self.css.get("orientation")).get_property("classList")
        for property in board_properties:
            if str(property) == "orientation-white" or str(property) == "orientation-black":
                return str(property)

        # throw error here as board does not seem to have a valid orientation
        return "fail"

    def get_cg_board(self):
        return self.driver.find_element(By.CSS_SELECTOR, self.css.get("state"))

    def get_board_pixel_size(self):
        """ Return the width x height of the board in pixels """
        board_size_element = self.driver.find_element(By.CSS_SELECTOR, self.css.get("container"))
        return [board_size_element.get_property("clientWidth"), board_size_element.get_property("clientHeight")]

    def get_num_ranks(self):
        """ Return the number of ranks of the chess board (rows) """
        ranks_element = self.driver.find_element(By.CSS_SELECTOR, self.css.get("ranks"))
        return ranks_element.get_property("childElementCount")

    def get_num_files(self):
        """ Return the number of files of the chess board (columns) """
        files_element = self.driver.find_element(By.CSS_SELECTOR, self.css.get("files"))
        return files_element.get_property("childElementCount")

    def get_file_pixel_size(self):
        """ Return the width of an individual file as an integer using floor division """
        return self.get_board_pixel_size()[0]//self.get_num_files()

    def get_rank_pixel_size(self):
        """ Return the height of an individual rank as an integer using floor division """
        return self.get_board_pixel_size()[1]//self.get_num_ranks()

    def get_square_pixel_size(self):
        """ """
        board_pixel_size = self.get_board_pixel_size()
        return [board_pixel_size[0]/self.get_num_files(), board_pixel_size[1]/self.get_num_ranks()]

    def get_last_move(self):
        # Note: A better way would be to use linked-list property of web elements to get the corresponding nodes
        piece = ""
        last_move0 = ""
        last_move1 = ""
        print(self.state)
        for key, val in self.state.items():
            if (str(key) == "last-move0"):
                piece = ""  # str(self.state[val.get_property("cgKey")].get_property("cgPiece"))
                last_move0 = (val.get_property("cgKey")[0], int(val.get_property("cgKey")[1:]))
            elif (str(key) == "last-move1"):
                last_move1 = (val.get_property("cgKey")[0], int(val.get_property("cgKey")[1:]))

        return [piece, last_move1, last_move0]

    def get_board_state(self):
        """ Return the state of the board (dictionary) """
        return self.state

    def update_board_state(self):
        """ The board state is a dictionary mapping position to web element (square/piece)"""
        print(id(self.state))
        self.state.clear()
        cg_board = self.get_cg_board()
        cg_board_properties = cg_board.get_property("childNodes")
        last_move = ""
        last_move_found = 0
        for cell in cg_board_properties:
            # if (cell.get_property("className") == "last-move"):
            if (cell.get_attribute("class") == "last-move"):
                self.state["last-move" + str(last_move_found)] = cell
                last_move_found += 1
            elif (cell.get_property("localName") == "piece"):
                self.state[str(cell.get_property("cgKey"))] = cell

    def print_board_state(self):
        for key, value in self.state.items():
            print(key, " : ", value)


    def make_move(self, start_move, end_move):
        """
        :param start_move, end_move: [file, rank]
        :return: None
        """
        orientation = self.get_board_orientation()
        board_element = self.get_cg_board()

        file_pixel_size = self.get_file_pixel_size()
        rank_pixel_size = self.get_rank_pixel_size()

        num_files = self.get_num_files()
        num_ranks = self.get_num_ranks()

        start_file_index = ord(start_move[0]) - ord('a')
        start_rank_index = start_move[1] - 1
        end_file_index = ord(end_move[0]) - ord('a')
        end_rank_index = end_move[1] - 1

        if orientation == "orientation-white":
            start_file_pixel_offset = file_pixel_size//2 + start_file_index*file_pixel_size
            start_rank_pixel_offset = rank_pixel_size//2 + (num_ranks - start_rank_index - 1)*rank_pixel_size
            self.action.move_to_element_with_offset(board_element, start_file_pixel_offset, start_rank_pixel_offset)
            self.action.click()
            self.action.perform()

            end_file_pixel_offset = file_pixel_size//2 + end_file_index*file_pixel_size
            end_rank_pixel_offset = rank_pixel_size//2 + (num_ranks - end_rank_index - 1)*rank_pixel_size
            self.action.move_to_element_with_offset(board_element, end_file_pixel_offset, end_rank_pixel_offset)
            self.action.click()
            self.action.perform()
            pass
        elif orientation == "orientation-black":
            start_file_pixel_offset = file_pixel_size//2 + (num_files - start_file_index - 1)*file_pixel_size
            start_rank_pixel_offset = rank_pixel_size//2 + start_rank_index*rank_pixel_size
            self.action.move_to_element_with_offset(board_element, start_file_pixel_offset, start_rank_pixel_offset)
            self.action.click()
            self.action.perform()

            end_file_pixel_offset = file_pixel_size//2 + (num_files - end_file_index - 1)*file_pixel_size
            end_rank_pixel_offset = rank_pixel_size//2 + end_rank_index*rank_pixel_size
            self.action.move_to_element_with_offset(board_element, end_file_pixel_offset, end_rank_pixel_offset)
            self.action.click()
            self.action.perform()


class LichessTester(WebTester):
    url = "https://lichess.org"
    xpath = {
        "puzzles"                   : "//a[@href='/training']", \
        # specify the element by multiple identifiers, separated by '//'
        "dashboard"                 : "//a[@href='/training/dashboard/30']",
        "streak"                    : "//a[@href='/streak']",
        "storm"                     : "//a[@href='/storm']",
        "racer"                     : "//a[@href='/racer']",
        "search_bar"                : "//header[@id='top']//div[@class='site-buttons']//div[@id='clinput']//a[@class='link']",
        "spotlight1"                : "//*[@id=\"main-wrap\"]/main/div[3]/div[1]/a[1]",
        "spotlight2"                : "//*[@id=\"main-wrap\"]/main/div[3]/div[1]/a[2]",
        "spotlight3"                : "//*[@id=\"main-wrap\"]/main/div[3]/div[1]/a[3]",
        "spotlight4"                : "//*[@id=\"main-wrap\"]/main/div[3]/div[1]/a[4]",
        "spotlight_info"            : "//*[@id=\"main-wrap\"]/main/aside/div/section[1]/div/p/a",
        "watch"                     : "//*[@id=\"topnav\"]/section[4]/a",
        "video_library"             : "//*[@id=\"topnav\"]/section[4]/div/a[5]",
        "video_player"              : "//*[@id=\"ytplayer\"]",
        "beginner"                  : "//*[@id=\"main-wrap\"]/main/aside/div[1]/a[3]/span",
        "beginner_video1"           : "//*[@id=\"main-wrap\"]/main/div/div[2]/a[1]",
        "beginner_video2"           : "//*[@id=\"main-wrap\"]/main/div/div[2]/a[2]",
        "signin"                    : "//*[@id=\"top\"]/div[2]/a",
        "signedin"                  : "//*[@id=\"user_tag\"]",
        "home"                      :"//a[@href='/']",
        "community"                 :"//a[@href='/player']",
        "forum"                     :"//a[@href='/forum']",
        "blog"                      :"//a[@href='/blog/community']",
        "swag"                      :"//a[@href='https://shop.spreadshirt.com/lichess-org']",
        "preferences"               : "//*[@id=\"dasher_app\"]/div/div[1]/a[3]",
        "kid_mode"                  : "//*[@id=\"main-wrap\"]/main/nav/a[5]",
        "kid_mode_pwform"           : "//*[@id=\"form3-passwd\"]",
        "kid_mode_submit"           : "//*[@id=\"main-wrap\"]/main/div/div/form/button",
        "signout"                   : "//*[@id=\"dasher_app\"]/div/div[1]/form/button",
        "username_email_form"       : "//*[@id=\"form3-username\"]",
        "password_form"             : "//*[@id=\"form3-password\"]",   
        "signin_signin"             : "//*[@id=\"main-wrap\"]/main/form/div[1]/button",
        "puzzles_moves_table"       : "//*[@id=\"main-wrap\"]/ main/div[2]/div[2]/div",
    }


    puzzles_board_css = {
        "container" : "cg-container",
        #"orientation": "div[class*=\"cg-wrap orientation-\"]",
        "orientation": "div[class*=\"cg-wrap\"]",
        "state": "cg-board",
        "ranks" : "coords[class*=\"ranks\"]",
        "files" : "coords[class*=\"files\"]",
        "complete" : "div[class=\"complete\"]",
        "continue" : "a[class=\"continue\"]"
    }

    board = None

    def __init__(self):
        """ Initiate LichessTester and setup the board """
        super().__init__()
        self.board = LichessBoard(self.driver, self.action, self.puzzles_board_css)

    def open_website(self):
        """ Open a website given a URL """
        self.driver.get(self.url)

    def hover_puzzles(self):
        """ Hover over the Puzzles tab on the top bar menu """
        self.hover(self.xpath.get("puzzles"))

    def hover_watch(self):
        """ Hover over the Watch tab on the top bar menu """
        self.hover(self.xpath.get("watch"))

    def click_puzzles(self):
        """ Click on the Puzzles tab on the top bar menu """
        self.click(self.xpath.get("puzzles"))

    def click_puzzles_dashboard(self):
        """ Click on the Puzzles Dashboard button under the Puzzles tab """
        self.hover_puzzles()
        self.click(self.xpath.get("streak"))

    def click_puzzles_streak(self):
        """ Click on the Puzzles Streak button under the Puzzles tab """
        self.hover_puzzles()
        self.click(self.xpath.get("streak"))

    def click_puzzles_storm(self):
        """ Click on the Puzzles Storm button under the Puzzles tab """
        self.hover_puzzles()
        self.click(self.xpath.get("storm"))

    def click_puzzles_racer(self):
        """ Click on the Puzzles Racer button under the Puzzles tab """
        self.hover_puzzles()
        self.click(self.xpath.get("racer"))

    def click_spotlight(self, index):
        """ Click on the Highlighted Tournaments on the left of the webpage """
        tournaments = (1, 2, 3, 4)
        if index not in tournaments:
            return "ERROR: Invalid Highlighted tournament ID input"
        else:
            self.hover(self.xpath.get("spotlight" + str(index)))
            self.click(self.xpath.get("spotlight" + str(index)))
            time.sleep(2)   # delay so we can see the tournament page
            self.click_spotlight_info()

    def click_spotlight_info(self):
        """ Click on the Highlighted Tournament's description """
        if (self.check_exists_by_xpath(self.xpath.get("spotlight_info"))):
            self.hover(self.xpath.get("spotlight_info"))
            self.click(self.xpath.get("spotlight_info"))
            time.sleep(3)   # delay so we can see the tournament description
            self.driver.switch_to.window(self.driver.window_handles[1])
            self.driver.close()
            self.driver.switch_to.window(self.driver.window_handles[0])
        else:
            pass

    def click_watch_video_library(self):
        """ Click on the Video library button under the Watch tab """
        self.hover_watch()
        self.click(self.xpath.get("video_library"))

    def click_beginner(self):
        """ Hover and click on the Beginner button """
        self.hover(self.xpath.get("beginner"))
        self.click(self.xpath.get("beginner"))

    def click_beginner_video(self, vid):
        """ Hover and click on the video """
        self.hover(self.xpath.get("beginner_video" + str(vid)))
        self.click(self.xpath.get("beginner_video" + str(vid)))

    def click_video_player(self):
        """ Click the video player to play video"""
        self.click(self.xpath.get("video_player"))

    def click_signin_button(self):
        """ Hover and click on the Sign in button """
        self.hover(self.xpath.get("signin"))
        self.click(self.xpath.get("signin"))

    def click_signout(self):
        """ Signout from lichess account """
        self.hover(self.xpath.get("signedin"))
        self.click(self.xpath.get("signedin"))
        time.sleep(0.75) # delay so we can see cascaded menu
        self.hover(self.xpath.get("signout"))
        self.click(self.xpath.get("signout"))

    def fill_signin_form(self, string_input1, string_input2):
        """ Fill out the signin information """
        id_form = self.driver.find_element(By.XPATH, self.xpath.get("username_email_form"))
        self.action.move_to_element(id_form)
        self.action.click()
        self.action.send_keys(string_input1)
        self.action.perform()
        time.sleep(1)   # delay so we can see the input on the id form
        self.action.send_keys(Keys.TAB)
        self.action.send_keys(string_input2)
        self.action.perform()
        #signin_button = self.driver.find_element(By.XPATH, self.xpath.get("signin_signin"))
        #self.action.move_to_element(signin_button)
        self.action.move_to_element(self.driver.find_element(By.XPATH, self.xpath.get("signin_signin")))
        self.action.click()
        self.action.perform()

    def click_home(self):
        """ Click home page link """
        self.click(self.xpath.get("home"))

    def hover_community(self):
        """ Hover over the Community tab on the top bar menu """
        self.hover(self.xpath.get("community"))

    def click_forum(self):
        """ Hover and click on the forum button """
        self.hover_community()
        self.hover(self.xpath.get("forum"))
        self.click(self.xpath.get("forum"))

    def click_blog(self):
        """ Hover and click on the blog button """
        self.hover_community()
        self.hover(self.xpath.get("blog"))
        self.click(self.xpath.get("blog"))

    def click_swag(self):
        """ Click on the swag link """
        self.click(self.xpath.get("swag"))

    def click_preferences(self):
        """ Click on preferences on the cascaded menu after clicking the user """
        self.hover(self.xpath.get("signedin"))
        self.click(self.xpath.get("signedin"))
        self.hover(self.xpath.get("preferences"))
        self.click(self.xpath.get("preferences"))

    def click_kid_mode(self):
        """ Click Kid mode in preferences """
        self.hover(self.xpath.get("kid_mode"))
        self.click(self.xpath.get("kid_mode"))

    def switch_kid_mode(self, string_input):
        """ Enable or disable kid mode for the account """
        self.action.move_to_element(self.driver.find_element(By.XPATH, self.xpath.get("kid_mode_pwform")))
        self.action.click()
        self.action.send_keys(string_input)
        self.action.perform()
        time.sleep(1)
        self.hover(self.xpath.get("kid_mode_submit"))
        self.click(self.xpath.get("kid_mode_submit"))

    def search(self, string_input):
        """ Search given an input """
        search_bar = self.driver.find_element(By.XPATH, self.xpath.get("search_bar"))
        self.action.move_to_element(search_bar)
        self.action.click()
        self.action.send_keys(string_input)
        self.action.perform()
        time.sleep(1)   # delay so we can see the input on the search bar
        self.action.send_keys(Keys.RETURN)
        self.action.perform()
        # self.action.move_to_element(element).click().send_keys(input).send_keys(Keys.RETURN).perform() # one liner

    def get_board(self):
        return self.board

    def get_puzzle_pgn(self):
        """ Returns the pgn of a puzzle in string format """
        moves_table = self.driver.find_element(By.XPATH, self.xpath.get("puzzles_moves_table"))

        pgn = ""
        num_elements = moves_table.get_property("childElementCount")
        # [!] ASSUME THERE IS AT LEAST 1 MOVE MADE IN THE PUZZLE POSITION (NEED AN ASSERTION TO CHECK)

        for i in range(0, num_elements, 3):
            pgn += str(((i//3) + 1)) + ". "

            white_move = moves_table.get_property("childNodes")[i + 1]
            pgn += white_move.get_property("innerText") + " "

            if (white_move.get_attribute("class") != "hist"):
                break

            black_move = moves_table.get_property("childNodes")[i + 2]
            pgn += black_move.get_property("innerText") + " "

        return pgn


    def puzzle_success(self):
        """ Returns true if the success element of the puzzle page is found,
         indicating a successful puzzle completion """
        #return len(self.driver.find_elements(By.CLASS_NAME, "complete")) > 0
        return len(self.driver.find_elements(By.CSS_SELECTOR, self.puzzles_board_css["complete"])) > 0

    def click_puzzle_continue(self):
        """ Click on the continue puzzle to continue to the next puzzle """
        self.click_element(self.driver.find_element(By.CSS_SELECTOR, self.puzzles_board_css["continue"]))


class LichessEngine(WebTester):
    url = "https://lichess.org/analysis"

    css = {
        "suggested_moves": "div[class=\"pv pv--nowrap\"]",
        "pgn": "div[class=\"pgn\"]",
        "pgn_button": "button[class='button button-thin action text']",
        "pgn_text": "textarea[class=\"copyable autoselect\"]"
        #"state" : "cg-board",
    }

    analysis_board_ccs = {
        "container": "cg-container",
        "orientation": "div[class*=\"cg-wrap\"]",
        "state": "cg-board",
        "ranks": "coords[class*=\"ranks\"]",
        "files": "coords[class*=\"files\"]"
    }

    board = None

    def __init__(self):
        super().__init__()
        self.board = LichessBoard(self.driver, self.action, self.analysis_board_ccs)

    def open_website(self):
        """ Open a website given a URL """
        self.driver.get(self.url)

    def enable_engine(self):
        """ Enable the engine with the hotkey SPACE """
        self.press_key(Keys.SPACE)

    def import_pgn(self, pgn_string):
        """ Import pgn to update analysis board """
        pgn = self.driver.find_element(By.CSS_SELECTOR, self.css.get("pgn"))
        self.action.move_to_element(pgn)
        self.action.click()
        self.action.send_keys(pgn_string)
        self.action.perform()

    def update_pgn(self, next_move):
        """ Concatenate to the pgn """
        pgn_text = self.driver.find_element(By.CSS_SELECTOR, self.css.get("pgn_text"))
        pgn_text.send_keys(" " + next_move)
        self.action.perform()

    def get_pgn(self):
        """ Returns the current pgn in string """
        pgn_text = self.driver.find_element(By.CSS_SELECTOR, self.css.get("pgn_text"))
        return pgn_text.get_property("value")

    def enter_pgn(self):
        """ Click the blue import button when new text is added to the pgn form """
        pgn_button = self.driver.find_element(By.CSS_SELECTOR, self.css.get("pgn_button"))
        self.click_element(pgn_button)

    def get_best_move(self):
        """ Return the best move in string format """
        suggested_moves = self.driver.find_element(By.CSS_SELECTOR, self.css.get("suggested_moves"))
        # [!] ASSUME THERE IS AT LEAST 1 MOVE ALWAYS SUGGESTED BY ENGINE (NEED AN ASSERTION TO CHECK)
        # NEED TO DELAY 2 SECONDS FOR ENGINE TO CALCULATE
        # else error selenium.common.exceptions.NoSuchElementException: Message: no such element: Unable to locate element: {"method":"xpath","selector":"//*[@id="main-wrap"]/main/div[3]/div[2]/div"}

        num_elements = suggested_moves.get_property("childElementCount")
        best_move_element = suggested_moves.get_property("childNodes")[2]
        best_move_string = best_move_element.get_property("innerText")
        return best_move_string

    def make_best_move(self):
        """ Analysis board determines what the best move is """
        best_move = self.get_best_move()
        lichess_engine.update_pgn(best_move)
        lichess_engine.enter_pgn()

    def get_board(self):
        """ Get the current board """
        return self.board

# https://lichess.org/analysis


def play(lichess_website_tester, lichess_engine):
    time.sleep(1.5)
    pgn = lichess_website_tester.get_puzzle_pgn()
    time.sleep(1)
    lichess_website_tester.get_board().update_board_state()
    time.sleep(1)
    lichess_engine.import_pgn(pgn)
    time.sleep(1)
    lichess_engine.enter_pgn()

    # initial analysis board's moves
    time.sleep(5)
    lichess_engine.make_best_move()
    time.sleep(1)
    lichess_engine.get_board().update_board_state()
    analysis_last_move = lichess_engine.get_board().get_last_move()
    print("Analysis last move: ", analysis_last_move)


    while (not lichess_website_tester.puzzle_success()):
        # puzzle board's moves
        time.sleep(0.1)
        lichess_website_tester.get_board().make_move(analysis_last_move[1], analysis_last_move[2]) # analysis_last_move[1] is source position & analysis_last_move[2] is terminal position
        time.sleep(1) # puzzle makes response move
        lichess_website_tester.get_board().update_board_state() # update the board
        puzzle_last_move = lichess_website_tester.get_board().get_last_move() # get the puzzle's last move

        if (lichess_website_tester.puzzle_success()):
            break

        # analysis board's moves
        lichess_engine.get_board().make_move(puzzle_last_move[1], puzzle_last_move[2])
        time.sleep(1) # wait for engine to find the best move
        lichess_engine.make_best_move() # engine makes best move
        time.sleep(1) # wait for pieces to move
        lichess_engine.get_board().update_board_state() # update the engine board
        analysis_last_move = lichess_engine.get_board().get_last_move() # get the engine's last move

    lichess_website_tester.click_puzzle_continue()



if __name__ == '__main__':

    # Only able to run single test case.
    # Comment out other tests.
    # Super Puzzles Test: Lines 652-672
    # Spotlight Tournaments Test: Lines 671-684
    # Watch Library Test: Lines 688-706
    # Puzzles Test: Lines 710-726
    # Signin & Signout Test: Lines 730-748
    # Community, Forum, Blog, Swag Test: Lines 752-764



    """ Super Puzzles Test """

    #initiate puzzle webpage
    lichess_website_tester = LichessTester()
    lichess_website_tester.open_website()
    time.sleep(1)
    lichess_website_tester.click_puzzles()
    lichess_website_tester.driver.set_window_size(lichess_website_tester.window_size['width']/2, lichess_website_tester.window_size['height'])
    lichess_website_tester.driver.set_window_position(0, 0)

    #initiate analysis webpage
    lichess_engine = LichessEngine()
    lichess_engine.open_website()
    lichess_engine.driver.set_window_size(lichess_engine.window_size['width']/2, lichess_engine.window_size['height'])
    lichess_engine.driver.set_window_position(lichess_engine.window_size['width']/2, 0)
    lichess_engine.enable_engine()

    for _ in range(0, 1000):
        play(lichess_website_tester, lichess_engine)

    time.sleep(1000)



    """ Spotlighted Tournaments Test """
    """
    lichess_website_tester = LichessTester()
    lichess_website_tester.open_website()
    time.sleep(2)
    lichess_website_tester.click_spotlight(1)
    time.sleep(2)
    lichess_website_tester.click_home()
    time.sleep(2)
    """


    """ Watch Library Test """
    """
    lichess_website_tester = LichessTester()
    lichess_website_tester.open_website()
    time.sleep(2)
    lichess_website_tester.hover_watch()
    time.sleep(2)
    lichess_website_tester.click_watch_video_library()
    time.sleep(2)
    lichess_website_tester.click_beginner()
    time.sleep(2)
    lichess_website_tester.click_beginner_video(1)
    time.sleep(2)
    lichess_website_tester.click_video_player()
    time.sleep(5)
    lichess_website_tester.click_video_player()
    time.sleep(1)
    lichess_website_tester.click_home()
    time.sleep(2)
    """


    """ Puzzles Test """
    """
    lichess_tester = LichessTester()
    lichess_tester.open_website()
    time.sleep(2)
    lichess_tester.click_puzzles()
    time.sleep(2)
    lichess_tester.click_puzzles_dashboard()
    time.sleep(2)
    lichess_tester.click_puzzles_streak()
    time.sleep(2)
    lichess_tester.click_puzzles_storm()
    time.sleep(2)
    lichess_tester.click_puzzles_racer()
    time.sleep(2)
    lichess_tester.search("Hello, world!")
    time.sleep(10)
    """


    """ Signin & Signout Test """
    """
    lichess_website_tester = LichessTester()
    lichess_website_tester.open_website()
    time.sleep(0.2)
    lichess_website_tester.click_signin_button()
    time.sleep(0.2)
    lichess_website_tester.fill_signin_form("Throwawayy123", "123456")
    time.sleep(3)
    lichess_website_tester.click_preferences()
    time.sleep(1)
    lichess_website_tester.click_kid_mode()
    time.sleep(1)
    lichess_website_tester.switch_kid_mode("123456")
    time.sleep(1)
    lichess_website_tester.click_signout()
    time.sleep(1)
    lichess_website_tester.click_home()
    time.sleep(4)
    """


    """ Community, Forum, Blog, Swag Test """
    """
    lichess_website_tester = LichessTester()
    lichess_website_tester.open_website()
    time.sleep(2)
    lichess_website_tester.click_forum()
    time.sleep(2)
    lichess_website_tester.click_blog()
    time.sleep(2)
    lichess_website_tester.click_home()
    time.sleep(2)
    lichess_website_tester.click_swag()
    time.sleep(4)
    """