import pygame
import random

pygame.init()
clock = pygame.time.Clock()
fps = 60

#game window
screen = pygame.display.set_mode((1200, 750))

#game variables
game_state = "start"
round = 1
new_question = True
question_key = ("","")
question = ()
answers = []
odds = 0
fifty_used = False
call_friend_used = False
call_friend_clicked = False
ask_audience_used = False
ask_audience_clicked = False

# list of money sum per round, used in e.g. round indicator and end screen functions
winnings = [100, 300, 500, 700, 1000, 2000, 3000, 5000, 7000, 10000, 15000, 30000, 60000, 200000, 1000000]

# a dictionary of all the questions from questions-file
with open("questions.txt") as file:
    questions = {}
    for row in file:
        # have to correct letters å, ä and ö
        converted = row.encode('latin-1').decode('utf-8')
        converted = converted.strip().split(", ")
        questions[tuple(converted[0:2])] = list(converted[2:7])

# game screen answer buttons
# have to define outside the function because of the randomization of the order each round
a_button = pygame.Rect(186, 570, 403, 53)
b_button = pygame.Rect(612, 570, 403, 53)
c_button = pygame.Rect(186, 630, 403, 53)
d_button = pygame.Rect(612, 630, 403, 53)
buttons = [a_button, b_button, c_button, d_button]





def draw_text(text, font, color, x, y):
    '''draws given text on screen with given font and location'''
    img = font.render(text, True, color)
    screen.blit(img, (x, y))



def start_screen():
    '''draws the start screen of the game'''
    global round, game_state, running, fifty_used, call_friend_used, ask_audience_used, question_key, new_question, answers

    start_background = pygame.image.load('kuvat/start_screen.png')
    screen.blit(start_background, (0, 0))


    start_font = pygame.font.SysFont('Georgia', 50, bold=True)
    # start screen buttons
    start_button = pygame.Rect(150, 585, 285, 100)
    load_button = pygame.Rect(457, 585, 285, 100)
    quit_button = pygame.Rect(765, 585, 285, 100)

    # mouse position
    a, b = pygame.mouse.get_pos()

    # draw buttons + color change when hovering over it
    if start_button.collidepoint(a, b):
        pygame.draw.rect(screen, (50, 50, 255), start_button)
    else:
        pygame.draw.rect(screen, (100, 160, 255), start_button)
    draw_text("Uusi Peli", start_font,"white", start_button.x + 25, start_button.y + 20)
    if load_button.collidepoint(a, b):
        pygame.draw.rect(screen, (50, 50, 255), load_button)
    else:
        pygame.draw.rect(screen, (100, 160, 255), load_button)
    draw_text("Lataa Peli", start_font,"white", load_button.x + 15, load_button.y + 20)
    if quit_button.collidepoint(a, b):
        pygame.draw.rect(screen, (50, 50, 255), quit_button)
    else:
        pygame.draw.rect(screen, (100, 160, 255), quit_button)
    draw_text("Sulje Peli", start_font, "white", quit_button.x + 20, quit_button.y + 20)

    #clicking buttons change the game state / quits game
    if event.type == pygame.MOUSEBUTTONDOWN:
        if start_button.collidepoint(event.pos):
            game_state = "game"
        # load button reads the needed variables from the save file
        elif load_button.collidepoint(event.pos):
            with open("save_file.txt", "r") as file:
                values = file.readline().split(",")
            round = int(values[0])
            if values[1] == "True":
                fifty_used = True
            elif values[1] == "False":
                fifty_used = False
            if values[2] == "True":
                call_friend_used = True
            elif values[2] == "False":
                call_friend_used = False
            if values[3] == "True":
                ask_audience_used = True
            elif values[3] == "False":
                ask_audience_used = False
            question_key = (values[4], values[5])
            answers = questions[question_key][1:5]
            new_question = False
            game_state = "game"

        elif quit_button.collidepoint(event.pos):
            running = False







def game():
    '''draws the main game screen'''
    global new_question, question_key, round, game_state, fifty_used, call_friend_used, ask_audience_used, question, answers, odds, call_friend_clicked, ask_audience_clicked

    game_background = pygame.image.load('kuvat/game_screen.png')
    screen.blit(game_background, (0, 0))

    question_font = pygame.font.SysFont('arialblack', 19, bold=False)

    # happens on the first game loop iteration of each round
    if new_question == True:
        # getting a random question key from the 10 available for each round
        question_key = (str(round), str(random.randint(1, 10)))
        # randomize the order of the buttons to change correct option
        random.shuffle(buttons)
        answers = list(questions[question_key][1:5])
        new_question = False
        # random number for odds of lifelines
        odds = random.randint(1, 100)

    question = questions[question_key][0]

    draw_text(question, question_font, "white", 210, 505)

    # mouse position
    a, b = pygame.mouse.get_pos()
    # draw all answer buttons + color change when hovering
    if a_button.collidepoint(a, b):
        pygame.draw.rect(screen, (255, 106, 0), a_button)
    else:
        pygame.draw.rect(screen, (18, 100, 180), a_button)
    if b_button.collidepoint(a, b):
        pygame.draw.rect(screen, (255, 106, 0), b_button)
    else:
        pygame.draw.rect(screen, (18, 100, 180), b_button)
    if c_button.collidepoint((a, b)):
        pygame.draw.rect(screen, (255, 106, 0), c_button)
    else:
        pygame.draw.rect(screen, (18, 100, 180), c_button)
    if d_button.collidepoint(a, b):
        pygame.draw.rect(screen, (255, 106, 0), d_button)
    else:
        pygame.draw.rect(screen, (18, 100, 180), d_button)

    # draw the answer alternatives
    draw_text(answers[0], question_font, "white", buttons[0].x + 20, buttons[0].y + 15)
    draw_text(answers[1], question_font, "white", buttons[1].x + 20, buttons[1].y + 15)
    draw_text(answers[2], question_font, "white", buttons[2].x + 20, buttons[2].y + 15)
    draw_text(answers[3], question_font, "white", buttons[3].x + 20, buttons[3].y + 15)


    # lifeline buttons
    fifty_button = pygame.Rect(33, 55, 190, 75)
    call_friend_button = pygame.Rect(33, 160, 190, 75)
    ask_audience_button = pygame.Rect(33, 265, 190, 75)
    # lifeline icons
    fifty_img = pygame.image.load("kuvat/fifty_fifty.png")
    call_friend_img = pygame.image.load("kuvat/phone_friend.png")
    ask_audience_img = pygame.image.load("kuvat/ask_audience.png")
    lifeline_used_img = pygame.image.load("kuvat/lifeline_x.png")

    # draw lifeline buttons
    if fifty_button.collidepoint(a, b):
        pygame.draw.ellipse(screen, (255, 106, 0), fifty_button)
        screen.blit(fifty_img, (33,55))
    else:
        pygame.draw.ellipse(screen, (18, 100, 180), fifty_button)
        screen.blit(fifty_img, (33, 55))
    if call_friend_button.collidepoint(a, b):
        pygame.draw.ellipse(screen, (255, 106, 0), call_friend_button)
        screen.blit(call_friend_img, (33, 160))
    else:
        pygame.draw.ellipse(screen, (18, 100, 180), call_friend_button)
        screen.blit(call_friend_img, (33, 160))
    if ask_audience_button.collidepoint(a, b):
        pygame.draw.ellipse(screen, (255, 106, 0), ask_audience_button)
        screen.blit(ask_audience_img, (33, 265))
    else:
        pygame.draw.ellipse(screen, (18, 100, 180), ask_audience_button)
        screen.blit(ask_audience_img, (33, 265))

    # when used, lifeline gets an "x" over it
    if fifty_used == True:
        screen.blit(lifeline_used_img, (33, 55))
    if call_friend_used == True:
        screen.blit(lifeline_used_img, (33, 160))
    if ask_audience_used == True:
        screen.blit(lifeline_used_img, (33, 265))

    # take money button
    take_money_button = pygame.Rect(480, 15, 240, 90)
    # draw the button
    if take_money_button.collidepoint((a, b)):
        pygame.draw.ellipse(screen, (255, 106, 0), take_money_button)
        draw_text("Ota rahat", question_font, "white", 550, 25)
        draw_text("&", question_font, "white", 590, 45)
        draw_text("JUOKSE", question_font, "white", 560, 65)

    else:
        pygame.draw.ellipse(screen, (18, 100, 255), take_money_button)
        draw_text("Ota rahat", question_font, "white", 550, 25)
        draw_text("&", question_font, "white", 590, 45)
        draw_text("JUOKSE", question_font, "white", 560, 65)

    # if a button is pressed, appropriate action is taken
    if event.type == pygame.MOUSEBUTTONDOWN:
        # lifeline buttons use a lifeline if it hasn't been used before
        if fifty_button.collidepoint(event.pos) and fifty_used == False:
            answers[1] = ""
            answers[2] = ""
            fifty_used = True

        if call_friend_button.collidepoint(event.pos) and call_friend_used == False:
            call_friend_clicked = True

        if ask_audience_button.collidepoint(event.pos) and ask_audience_used == False:
            ask_audience_clicked = True

        if take_money_button.collidepoint(event.pos):
            game_state = "game end"

        # if correct answer is clicked -> next round, else game ends
        if buttons[0].collidepoint(event.pos):
            pygame.draw.rect(screen, (0, 255, 0), buttons[0])
            draw_text(answers[0], question_font, "white", buttons[0].x + 20, buttons[0].y + 15)
            round += 1
            new_question = True
            call_friend_clicked = False
            ask_audience_clicked = False
        elif buttons[1].collidepoint(event.pos):
            pygame.draw.rect(screen, (255, 0, 0), buttons[1])
            draw_text(answers[1], question_font, "white", buttons[1].x + 20, buttons[1].y + 15)
            game_state = "game over"
        elif buttons[2].collidepoint(event.pos):
            pygame.draw.rect(screen, (255, 0, 0), buttons[2])
            draw_text(answers[2], question_font, "white", buttons[2].x + 20, buttons[2].y + 15)
            game_state = "game over"
        elif buttons[3].collidepoint(event.pos):
            pygame.draw.rect(screen, (255, 0, 0), buttons[3])
            draw_text(answers[3], question_font, "white", buttons[3].x + 20, buttons[3].y + 15)
            game_state = "game over"

    if call_friend_clicked:
        # "friend" gives the right answer with 75% chance
        call_screen = pygame.image.load(("kuvat/phone_friend_screen.png"))
        screen.blit(call_screen, (0, 0))
        if odds <= 75:
            draw_text(f"Hmm... Luulen, että vastaus on {answers[0]}", question_font, "black", 340, 400)

        else:
            draw_text(f"Hmm... Luulen, että vastaus on {answers[3]}", question_font, "black", 340, 400)
        call_friend_used = True

    if ask_audience_clicked:
        # "audience" gives the right answer with 90% chance
        audience_screen = pygame.image.load(("kuvat/audience_screen.png"))
        screen.blit(audience_screen, (0, 0))
        if odds <= 90:
            draw_text(f"Hmm... Luulemme, että vastaus on {answers[0]}", question_font, "black", 340, 400)

        else:
            draw_text(f"Hmm... Luulemme, että vastaus on {answers[3]}", question_font, "black", 340, 400)
        ask_audience_used = True


def round_indicator(round):
    ''' draws column of all rounds and shows current round in orange'''
    ind_font = pygame.font.SysFont("arialblack", 20)
    # position of first box
    y = 481
    if round < 16:
        # draws boxes for all rounds in blue
        for i in range(15):
            round_box = pygame.Rect(1039, y, 150, 30)
            pygame.draw.rect(screen, (18, 100, 180), round_box)
            draw_text(f"{winnings[i]} €", ind_font, "white", 1045, y + 2)
            y -= 34
        # draws current round box in orange
        pygame.draw.rect(screen, (255, 106, 0), pygame.Rect(1039, 481 - ((round - 1) * 34), 150, 30))
        draw_text(f"{winnings[round - 1]} €", ind_font, "white", 1045, 481 - ((round - 1) * 34))


def pause_screen():
    '''draws the pause screen'''
    global game_state, running
    pause_image = pygame.image.load("kuvat/pause_menu1.png")
    screen.blit(pause_image, (0, 0))

    resume_surprise_font = pygame.font.SysFont('Impact', 72)
    save_quit_font = pygame.font.SysFont('Impact', 45)

    resume_button = pygame.Rect(422, 294, 349, 101)
    save_quit_button = pygame.Rect(422, 554, 349, 101)
    # the menu looks better with 3 buttons than 2 :D
    surprise_button = pygame.Rect(422, 424, 349, 101)

    # mouse position
    a, b = pygame.mouse.get_pos()

    # draw buttons + color change when hovering over it
    if resume_button.collidepoint(a, b):
        pygame.draw.rect(screen, (255, 147, 53), resume_button)
    else:
        pygame.draw.rect(screen, (255, 255, 255), resume_button)
    draw_text("Jatka Peliä", resume_surprise_font, "black", resume_button.x + 18, resume_button.y + 7)
    if surprise_button.collidepoint(a, b):
        pygame.draw.rect(screen, (255, 147, 53), surprise_button)
    else:
        pygame.draw.rect(screen, (255, 255, 255), surprise_button)
    draw_text("Yllätys", resume_surprise_font, "black", surprise_button.x + 75, surprise_button.y + 7)
    if save_quit_button.collidepoint(a, b):
        pygame.draw.rect(screen, (255, 147, 53), save_quit_button)
    else:
        pygame.draw.rect(screen, (255, 255, 255), save_quit_button)
    draw_text("Tallenna & Lopeta", save_quit_font, "black", save_quit_button.x + 13, save_quit_button.y + 25)


    if event.type == pygame.MOUSEBUTTONDOWN:
        if resume_button.collidepoint(event.pos):
            game_state = "game"

        elif save_quit_button.collidepoint(event.pos):
            with open("save_file.txt", "w") as file:
                file.write(f"{round},{fifty_used},{call_friend_used},{ask_audience_used},{question_key[0]},{question_key[1]}")
                running = False

        elif surprise_button.collidepoint(a, b):
            game_state = "surprise"

def surprise():
    '''draws surprise image on screen :)'''
    global game_state
    surprise_screen = pygame.image.load("kuvat/pontsoo.png")
    screen.blit(surprise_screen, (233, 145))
    surprise_font = pygame.font.SysFont('Impact', 72)
    draw_text("paina ESC palataksesi", surprise_font, "black", 275, 520)
    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_ESCAPE:
            game_state = "paused"



def game_over():
    '''draws the game over screen, with the amount of money won'''
    global round, game_state, running, new_question, fifty_used, call_friend_used, ask_audience_used
    screen.fill((76, 118, 255))

    game_over_font = pygame.font.SysFont("Verdana", 50, bold=True)
    winnings_font = pygame.font.SysFont("Verdana", 50, bold=True)

    button_font = pygame.font.SysFont('Georgia', 50, bold=True)
    new_game_button = pygame.Rect(250, 500, 285, 100)
    quit_button = pygame.Rect(665, 500, 285, 100)

    draw_text("VALITETTAVASTI VASTASIT VÄÄRIN :(", game_over_font, "white", 60, 300)
    if round > 10:
        draw_text("VOITIT 10 000 €", winnings_font, "white", 365, 400)
    elif round > 5:
        draw_text("VOITIT 1 000 €", winnings_font, "white", 383, 400 )
    else:
        draw_text("VOITIT 0 €", winnings_font, "white", 450, 400)



    a, b = pygame.mouse.get_pos()

    # draw buttons + color change when hovering over it
    if new_game_button.collidepoint(a, b):
        pygame.draw.rect(screen, (50, 50, 255), new_game_button)
    else:
        pygame.draw.rect(screen, (100, 160, 255), new_game_button)
    draw_text("Uusi Peli", button_font, "white", new_game_button.x + 25, new_game_button.y + 20)
    if quit_button.collidepoint(a, b):
        pygame.draw.rect(screen, (50, 50, 255), quit_button)
    else:
        pygame.draw.rect(screen, (100, 160, 255), quit_button)
    draw_text("Sulje Peli", button_font, "white", quit_button.x + 20, quit_button.y + 20)

    # clicking buttons change the game state / quits game
    if event.type == pygame.MOUSEBUTTONDOWN:
        if new_game_button.collidepoint(event.pos):
            round = 1
            fifty_used = False
            call_friend_used = False
            ask_audience_used = False
            game_state = "game"
            new_question = True
        elif quit_button.collidepoint(event.pos):
            running = False


def game_end():
    '''draws game end screen, with the amount of money won'''
    global round, game_state, running, new_question, fifty_used, call_friend_used, ask_audience_used

    background = pygame.image.load("kuvat/blurred.png")
    screen.blit(background, (0, 0))
    game_over_font = pygame.font.SysFont("Verdana", 80, bold=True)
    winnings_font = pygame.font.SysFont("Verdana", 65, bold=True)
    draw_text("ONNEKSI OLKOON!", game_over_font, "white", 170, 260)


    if round > 15:
        draw_text("VOITIT 1 000 000 €", winnings_font, "white", 240, 380)
    elif round == 1:
        draw_text("VOITIT 0 €", winnings_font, "white", 400, 380)
    else:
        draw_text(f"Voitit {winnings[round - 2]} €", winnings_font, "white", 350, 380)
    button_font = pygame.font.SysFont('Georgia', 50, bold=True)

    new_game_button = pygame.Rect(150, 500, 285, 100)
    quit_button = pygame.Rect(765, 500, 285, 100)

    a, b = pygame.mouse.get_pos()

    # draw buttons + color change when hovering over it
    if new_game_button.collidepoint(a, b):
        pygame.draw.rect(screen, (50, 50, 255), new_game_button)
    else:
        pygame.draw.rect(screen, (100, 160, 255), new_game_button)
    draw_text("Uusi Peli", button_font, "white", new_game_button.x + 25, new_game_button.y + 20)
    if quit_button.collidepoint(a, b):
        pygame.draw.rect(screen, (50, 50, 255), quit_button)
    else:
        pygame.draw.rect(screen, (100, 160, 255), quit_button)
    draw_text("Sulje Peli", button_font, "white", quit_button.x + 20, quit_button.y + 20)

    # clicking buttons change the game state and variable values / quits game
    if event.type == pygame.MOUSEBUTTONDOWN:
        if new_game_button.collidepoint(event.pos):
            round = 1
            fifty_used = False
            call_friend_used = False
            ask_audience_used = False
            game_state = "game"
            new_question = True
        elif quit_button.collidepoint(event.pos):
            running = False




#game loop

running = True
while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if game_state == "game over":
            game_over()

        if game_state == "game":
            game()
            if round > 15:
                game_state = "game end"
            round_indicator(round)
            # pressing ESC changes the game state -> pauses the game
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    game_state = "paused"

        if game_state == "start":
            start_screen()

        if game_state == "game end":
            game_end()

        if game_state == "paused":
            pause_screen()

        if game_state == "surprise":
            surprise()


    clock.tick(fps)
    pygame.display.update()