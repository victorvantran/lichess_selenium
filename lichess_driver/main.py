from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys  # Gives access to input keys to interface with the website
from selenium.webdriver.common.by import By  # Allows us to identify the xpath of element
from selenium.webdriver.common.action_chains import \
    ActionChains  # Allows us to perform generic actions on modules such as hovering, clicking, etc.
from selenium.webdriver.support.ui import WebDriverWait # Allows us to stall the driver to wait for a particular element to load
from selenium.webdriver.support import expected_conditions as EC
import time  # Allows us to sleep for a certain number of seconds



CHROMEDRIVER_PATH = "E:\\chromedriver\\chromedriver.exe"
#CHROMEDRIVER_PATH = "D:\\Software Expert\\chromedriver.exe"
SERVICE = Service(CHROMEDRIVER_PATH)
MAX_WAIT_FOR_SECONDS = 10

class WebTester:
    driver = None
    action = None

    def __init__(self):
        options = webdriver.ChromeOptions()
        options.add_experimental_option('excludeSwitches', ['enable-logging'])
        self.driver = webdriver.Chrome(service=SERVICE, options=options)
        self.chrome_window_maximize()
        self.action = ActionChains(self.driver)

    def __del__(self):
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
        """ Click on an element based on a given element and offset """
        element = self.driver.find_element(By.XPATH, xpath)
        self.click_element_offset(element, x, y)

    def press_key(self, key):
        """ Press a key """
        self.action.send_keys(key)
        self.action.perform()

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
    xpath = None
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

    def __init__(self, driver, action, xpath):
        super().__init__()
        self.driver = driver
        self.action = action
        self.xpath = xpath
        self.state = dict()

    def get_board_orientation(self):
        board_properties = self.driver.find_element(By.XPATH, self.xpath.get("orientation")).get_property("classList")
        for property in board_properties:
            if str(property) == "orientation-white" or str(property) == "orientation-black":
                return str(property)

        # throw error here as board does not seem to have a valid orientation
        return "fail"

    def get_cg_board(self):
        return self.driver.find_element(By.XPATH, self.xpath.get("state"))

    def get_board_pixel_size(self):
        """ Return the width x height of the board in pixels """
        board_size_element = self.driver.find_element(By.XPATH, self.xpath.get("container"))
        return [board_size_element.get_property("clientWidth"), board_size_element.get_property("clientHeight")]

    def get_num_ranks(self):
        """ Return the number of ranks of the chess board (rows) """
        ranks_element = self.driver.find_element(By.XPATH, self.xpath.get("ranks"))
        return ranks_element.get_property("childElementCount")

    def get_num_files(self):
        """ Return the number of files of the chess board (columns) """
        files_element = self.driver.find_element(By.XPATH, self.xpath.get("files"))
        return files_element.get_property("childElementCount")

    def get_file_pixel_size(self):
        """ Return the width of an individual file as an integer using floor division """
        return self.get_board_pixel_size()[0]//self.get_num_files()

    def get_rank_pixel_size(self):
        """ Return the height of an individual rank as an integer using floor division """
        return self.get_board_pixel_size()[1]//self.get_num_ranks()

    def get_square_pixel_size(self):
        board_pixel_size = self.get_board_pixel_size()
        return [board_pixel_size[0]/8, board_pixel_size[1]/8]

    def get_last_move(self):
        # Note: A better way would be to use linked-list property of web elements to get the corresponding nodes
        piece = ""
        last_move0 = ""
        last_move1 = ""
        print(self.state)
        for key, val in self.state.items():
            if (str(key) == "last-move0"):
                piece = "" #str(self.state[val.get_property("cgKey")].get_property("cgPiece"))
                last_move0 = (val.get_property("cgKey")[0], int(val.get_property("cgKey")[1:]))
            elif (str(key) == "last-move1"):
                last_move1 = (val.get_property("cgKey")[0], int(val.get_property("cgKey")[1:]))

        return [piece, last_move1, last_move0]

    def get_board_state(self):
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
            #if (cell.get_property("className") == "last-move"):
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
        "puzzles"                   : "//a[@href='/training']",
        "dashboard"                 : "//a[@href='/training/dashboard/30']",
        "streak"                    : "//a[@href='/streak']",
        "storm"                     : "//a[@href='/storm']",
        "racer"                     : "//a[@href='/racer']",
        "search_bar"                : "//header[@id='top']//div[@class='site-buttons']//div[@id='clinput']//a[@class='link']",
        "banner"                    : "//*[@id=\"top\"]/div[1]/h1/a",
        "spotlight1"                : "//*[@id=\"main-wrap\"]/main/div[3]/div[1]/a[1]",
        "spotlight_info"            : "//*[@id=\"main-wrap\"]/main/aside/div/section[1]/div/p/a",
        "watch"                     : "//*[@id=\"topnav\"]/section[4]/a",
        "video_library"             : "//*[@id=\"topnav\"]/section[4]/div/a[5]",
        "video_player"              : "//*[@id=\"ytplayer\"]",
        "beginner"                  : "//*[@id=\"main-wrap\"]/main/aside/div[1]/a[3]/span",
        "beginner_video1"           : "//*[@id=\"main-wrap\"]/main/div/div[2]/a[1]",
        "beginner_video2"           : "//*[@id=\"main-wrap\"]/main/div/div[2]/a[2]",
        "signin"                    : "//*[@id=\"top\"]/div[2]/a",
        "signedin"                  : "//*[@id=\"user_tag\"]",
        "signout"                   : "//*[@id=\"dasher_app\"]/div/div[1]/form/button",
        "username_email_form"       : "//*[@id=\"form3-username\"]",
        "password_form"             : "//*[@id=\"form3-password\"]",   
        "signin_signin"             : "//*[@id=\"main-wrap\"]/main/form/div[1]/button", \
        # specify the element by multiple identifiers, separated by '//'
        "puzzles_moves_table"       : "//*[@id=\"main-wrap\"]/ main/div[2]/div[2]/div",
    }

    puzzles_board_xpath = {
        "container": "//*[@id=\"main-wrap\"]/main/div[1]/div/cg-container",
        "orientation": "//*[@id=\"main-wrap\"]/main/div[1]/div",
        "state": "//*[@id=\"main-wrap\"]/main/div[1]/div/cg-container/cg-board",
        "ranks" : "//*[@id=\"main-wrap\"]/main/div[1]/div/cg-container/coords[1]",
        "files" : "//*[@id=\"main-wrap\"]/main/div[1]/div/cg-container/coords[2]",
        "success" : "//*[@id=\"main-wrap\"]/main/div[2]/div[3]/div[1]"
    }

    board = None

    def __init__(self):
        super().__init__()
        self.board = LichessBoard(self.driver, self.action, self.puzzles_board_xpath)

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
        self.hover(self.xpath.get("spotlight" + str(index)))
        self.click(self.xpath.get("spotlight" + str(index)))

    def click_spotlight_info(self):
        """ Click on the Highlighted Tournament's description """
        self.hover(self.xpath.get("spotlight_info"))
        self.click(self.xpath.get("spotlight_info"))
        time.sleep(2)   # delay so we can see the tournament description
        self.driver.switch_to.window(self.driver.window_handles[1])
        self.driver.close()
        self.driver.switch_to.window(self.driver.window_handles[0])


    # def click_tournament_player(self, index):
    #     """ Click on the tournament participant """
    #     self.hover(self.xpath.get("tournament_player" + str(index)))
    #     self.click(self.xpath.get("tournament_player" + str(index)))

    # def click_close_tournament_player(self):
    #     """ Close the tournament participant's information """
    #     self.hover(self.xpath.get("close_tournament_player"))
    #     self.click(self.xpath.get("close_tournament_player"))

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

    def click_banner(self):
        self.hover(self.xpath.get("banner"))
        self.click(self.xpath.get("banner"))

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
        return len(self.driver.find_elements(By.CLASS_NAME, "complete")) > 0
        """
        return len(self.driver.find_elements(By.XPATH, self.puzzles_board_xpath.get("success"))) > 0 and \
               self.driver.find_element(By.XPATH, self.puzzles_board_xpath.get("success")).get_attribute("className") != None and \
            self.driver.find_element(By.XPATH, self.puzzles_board_xpath.get("success")).get_property("className") == "complete"
        """


class LichessEngine(WebTester):
    url = "https://lichess.org/analysis"
    xpath = {
        "suggested_moves"   : "//*[@id=\"main-wrap\"]/main/div[3]/div[2]/div",
        "pgn_bar"           : "//*[@id=\"main-wrap\"]/main/div[5]/div/div[2]",
        "pgn_button"        : "//*[@id=\"main-wrap\"]/main/div[5]/div/div[2]/div/button",
        "pgn_text"          : "//*[@id=\"main-wrap\"]/main/div[5]/div/div[2]/div/textarea",
        "state"             : "//*[@id=\"main-wrap\"]/main/div[1]/div[3]/cg-container/cg-board",
        "board_orientation" : "//*[@id=\"main-wrap\"]/main/div[1]/div[3]"
    }

    analysis_board_xpath = {
        "container": "//*[@id=\"main-wrap\"]/main/div[1]/div/cg-container",
        "orientation": "//*[@id=\"main-wrap\"]/main/div[1]/div[3]",
        "state": "//*[@id=\"main-wrap\"]/main/div[1]/div[3]/cg-container/cg-board",
        "ranks" : "//*[@id=\"main-wrap\"]/main/div[1]/div[3]/cg-container/coords[1]",
        "files" : "//*[@id=\"main-wrap\"]/main/div[1]/div[3]/cg-container/coords[2]"
    }

    board = None

    def __init__(self):
        super().__init__()
        self.board = LichessBoard(self.driver, self.action, self.analysis_board_xpath)

    def open_website(self):
        """ Open a website given a URL """
        self.driver.get(self.url)

    def enable_engine(self):
        self.press_key(Keys.SPACE)

    def import_pgn(self, pgn):
        """ Import pgn to update analysis board """
        pgn_bar = self.driver.find_element(By.XPATH, self.xpath.get("pgn_bar"))
        self.action.move_to_element(pgn_bar)
        self.action.click()
        self.action.send_keys(pgn)
        self.action.perform()

    def update_pgn(self, next_move):
        pgn_text = self.driver.find_element(By.XPATH, self.xpath.get("pgn_text"))
        pgn_text.send_keys(" " + next_move)
        self.action.perform()

    def get_pgn(self):
        """ Returns the current pgn in string """
        pgn_text = self.driver.find_element(By.XPATH, self.xpath.get("pgn_text"))
        return pgn_text.get_property("value")


    def enter_pgn(self):
        self.click(self.xpath.get("pgn_button"))

    def get_best_move(self):
        """ Return the best move in string format """
        suggested_moves = self.driver.find_element(By.XPATH, self.xpath.get("suggested_moves"))
        # [!] ASSUME THERE IS AT LEAST 1 MOVE ALWAYS SUGGESTED BY ENGINE (NEED AN ASSERTION TO CHECK)
        # NEED TO DELAY 2 SECONDS FOR ENGINE TO CALCULATE
        # else error selenium.common.exceptions.NoSuchElementException: Message: no such element: Unable to locate element: {"method":"xpath","selector":"//*[@id="main-wrap"]/main/div[3]/div[2]/div"}

        num_elements = suggested_moves.get_property("childElementCount")
        best_move_element = suggested_moves.get_property("childNodes")[2]
        best_move_string = best_move_element.get_property("innerText")
        return best_move_string

    def make_best_move(self):
        best_move = self.get_best_move()
        lichess_engine.update_pgn(best_move)
        lichess_engine.enter_pgn()
        time.sleep(1)

    def get_board(self):
        return self.board

    def test(self):
        #print(list(self.get_board().get_board_state().values())[-1])
        cell = list(self.get_board().get_board_state().values())[-1]
        self.click_element(cell)

# https://lichess.org/analysis

if __name__ == '__main__':
    #initiate puzzle board
    lichess_website_tester = LichessTester()
    lichess_website_tester.open_website()
    time.sleep(1)
    lichess_website_tester.click_puzzles()
    time.sleep(1.5)
    pgn = lichess_website_tester.get_puzzle_pgn()
    time.sleep(1)
    lichess_website_tester.get_board().update_board_state()
    time.sleep(1)

    #initiate analysis board
    lichess_engine = LichessEngine()
    lichess_engine.open_website()
    lichess_engine.enable_engine()
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
        time.sleep(1)
        lichess_website_tester.get_board().make_move(analysis_last_move[1], analysis_last_move[2])
        time.sleep(1)
        lichess_website_tester.get_board().update_board_state()
        puzzle_last_move = lichess_website_tester.get_board().get_last_move()

        # analysis board's moves
        lichess_engine.get_board().make_move(puzzle_last_move[1], puzzle_last_move[2])
        time.sleep(5)
        lichess_engine.make_best_move()
        time.sleep(1)
        lichess_engine.get_board().update_board_state()
        analysis_last_move = lichess_engine.get_board().get_last_move()





    print("Puzzle completed!") #https://lichess.org/training#Insert=puzzle%number #b6wRh







    time.sleep(1000)


    """ Spotlighted Tournaments Test """
    """
    lichess_website_tester = LichessTester()
    lichess_website_tester.open_website()
    time.sleep(2)
    lichess_website_tester.click_spotlight(1)
    time.sleep(2)
    lichess_website_tester.click_spotlight_info()
    time.sleep(2)
    lichess_website_tester.click_banner()
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
    lichess_website_tester.click_banner()
    time.sleep(2)
    """


    """
    lichess_website_tester = LichessTester()
    lichess_website_tester.open_website()
    time.sleep(0.2)
    lichess_website_tester.click_puzzles()
    time.sleep(0.2)
    lichess_website_tester.get_puzzle_moves_table()
    time.sleep(1000)
    """



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
    lichess_website_tester.click_signout()
    time.sleep(1)
    lichess_website_tester.click_banner()
    time.sleep(4)
    """


"""
SUBMENU CLICK
# https://www.tutorialspoint.com/how-can-i-perform-mouse-hover-action-in-selenium-python
action = ActionChains(self.driver)
# identify element
element = self.driver.find_element(By.XPATH, "//a[@href='/training']")
# hover over element
action.move_to_element(element).perform()
# identify sub menu element
sub_element = self.driver.find_element(By.XPATH, "//a[@href='/racer']")
# hover over element and click
action.move_to_element(sub_element).click().perform()
"""


# /html/body/div[1]/main/div[1]/div[3]/cg-container/cg-board

#iterate till find 'black' or 'white'

#https://lichess.org/forum/lichess-feedback/play-by-typing-san-moves-like-e4-nf3-or-qxd6


# To translate pieces to position need to consider:
# board flip position   | # //*[@id="main-wrap"]/main/div[1]/div .get_property("innerText") == black/white
# board size            |
# piece position        |



#1) Every time a higher ranking pieces moves, a capital prefix is apparent
#2) Pawns have no capital prefix
#3) If multiple pieces can enter a square, the piece to enter the square is specified by the file and x


# Just use last move information


# After getting best move, make it. Then record the previous move to get c1n1c2n2
# After making the best move, wait for computer response. Then record c1n1c2n2