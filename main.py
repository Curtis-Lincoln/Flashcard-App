import kivy, kivymd, re, hashlib, random, ssl, smtplib, sqlite3, time, datetime
from kivy.uix.boxlayout import BoxLayout 
from kivy.lang import Builder 
from kivymd.app import MDApp
from kivymd.uix.boxlayout import MDBoxLayout
from kivy.uix.widget import Widget
from kivy.properties import ObjectProperty
from kivy.uix.spinner import Spinner
from kivymd.uix.list import OneLineListItem
from kivy.uix.screenmanager import ScreenManager, Screen, NoTransition, SlideTransition, CardTransition, SwapTransition, FadeTransition, WipeTransition, FallOutTransition, RiseInTransition
from kivy.uix.floatlayout import FloatLayout
from kivy_garden.matplotlib.backend_kivyagg import FigureCanvasKivyAgg
import matplotlib.pyplot as plt
from kivy.clock import Clock
from email.message import EmailMessage
from kivy.factory import Factory

def OpenDatabase():
        conn = sqlite3.connect("Flashcard_App.db", timeout=10)
        return conn, conn.cursor()

def CloseDatabase(conn):
        conn.commit()
        conn.close()

def PreMadeFlashcards(ID):
    conn, c = OpenDatabase()

    c.execute(f"INSERT INTO FlashcardSet (SetName, NumCards, UserID, Premade) VALUES ('Premade Set: Addition', 3, {ID}, 1)")
    c.execute(f"SELECT SetID FROM FlashcardSet ORDER BY SetID DESC")
    SetID = c.fetchall()[0][0]
    AdditionFront1 = "What is 3+4"
    AdditionFront2 = "What is 34+73"
    AdditionFront3 = "What is 458+621"
    AdditionBack1 = "7"
    AdditionBack2 = "107"
    AdditionBack3 = "1079"
    c.execute(f"INSERT INTO Flashcard (SetID, Title, FrontCard, BackCard, Format, Difficulty) VALUES ({SetID}, 'Addition Question 1', '{AdditionFront1}', '{AdditionBack1}', 0, 'Easy')")
    c.execute(f"INSERT INTO Flashcard (SetID, Title, FrontCard, BackCard, Format, Difficulty) VALUES ({SetID}, 'Addition Question 2', '{AdditionFront2}', '{AdditionBack2}', 0, 'Medium')")
    c.execute(f"INSERT INTO Flashcard (SetID, Title, FrontCard, BackCard, Format, Difficulty) VALUES ({SetID}, 'Addition Question 3', '{AdditionFront3}', '{AdditionBack3}', 0, 'Hard')")
    c.execute(f"INSERT INTO MainProgress (SetID) VALUES ({SetID})")

    c.execute(f"INSERT INTO FlashcardSet (SetName, NumCards, UserID, Premade) VALUES ('Premade Set: Subtraction', 3, {ID}, 1)")
    c.execute(f"SELECT SetID FROM FlashcardSet ORDER BY SetID DESC")
    SetID = c.fetchall()[0][0]
    SubtractionFront1 = "What is 12-6"
    SubtractionFront2 = "What is 98-32"
    SubtractionFront3 = "What is 983-359"
    SubtractionBack1 = "6"
    SubtractionBack2 = "66"
    SubtractionBack3 = "624"
    c.execute(f"INSERT INTO Flashcard (SetID, Title, FrontCard, BackCard, Format, Difficulty) VALUES ({SetID}, 'Subtraction Question 1', '{SubtractionFront1}', '{SubtractionBack1}', 0, 'Easy')")
    c.execute(f"INSERT INTO Flashcard (SetID, Title, FrontCard, BackCard, Format, Difficulty) VALUES ({SetID}, 'Subtraction Question 2', '{SubtractionFront2}', '{SubtractionBack2}', 0, 'Medium')")
    c.execute(f"INSERT INTO Flashcard (SetID, Title, FrontCard, BackCard, Format, Difficulty) VALUES ({SetID}, 'Subtraction Question 3', '{SubtractionFront3}', '{SubtractionBack3}', 0, 'Hard')")
    c.execute(f"INSERT INTO MainProgress (SetID) VALUES ({SetID})")



    c.execute(f"INSERT INTO FlashcardSet (SetName, NumCards, UserID, Premade) VALUES ('Premade Set: Multiplication', 3, {ID}, 1)")
    c.execute(f"SELECT SetID FROM FlashcardSet ORDER BY SetID DESC")
    SetID = c.fetchall()[0][0]
    MultiplicationFront1 = "What is 7*4"
    MultiplicationFront2 = "What is 32*11"
    MultiplicationFront3 = "What is 324*65"
    MultiplicationBack1 = "28"
    MultiplicationBack2 = "352"
    MultiplicationBack3 = "21060"
    c.execute(f"INSERT INTO Flashcard (SetID, Title, FrontCard, BackCard, Format, Difficulty) VALUES ({SetID}, 'Multiplication Question 1', '{MultiplicationFront1}', '{MultiplicationBack1}', 0, 'Easy')")
    c.execute(f"INSERT INTO Flashcard (SetID, Title, FrontCard, BackCard, Format, Difficulty) VALUES ({SetID}, 'Multiplication Question 2', '{MultiplicationFront2}', '{MultiplicationBack2}', 0, 'Medium')")
    c.execute(f"INSERT INTO Flashcard (SetID, Title, FrontCard, BackCard, Format, Difficulty) VALUES ({SetID}, 'Multiplication Question 3', '{MultiplicationFront3}', '{MultiplicationBack3}', 0, 'Hard')")
    c.execute(f"INSERT INTO MainProgress (SetID) VALUES ({SetID})")

    CloseDatabase(conn)


def HashPassword(Password):
    sha256 = hashlib.sha256()
    Passwd = bytes(Password.encode())
    sha256.update(Passwd)
    HashedPwd = sha256.hexdigest()
    return HashedPwd

def ValidEmail(Email):
    regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'

    if(re.fullmatch(regex, Email)):
        return True
    return False 

def ValidUsername(User):
    conn, c = OpenDatabase()

    regex = bool(re.search(r"\s", User))
    if len(User) >= 1 and len(User) <= 30 and not regex:
        Usernames = c.execute("SELECT Username From UserAccount")
        Usernames = c.fetchall()
    
        for row in range(len(Usernames)):
            if User == Usernames[row][0]:
                CloseDatabase(conn)
                return False
        
        CloseDatabase(conn)
        return True
    else:
        CloseDatabase(conn)
        return False 
    

def ValidPassword(Password):
    regex = "^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9])(?=.*?[#?!@$%^&*-]).{12,30}$"
    if re.match(regex, Password) != None:
        return True
    else:
        return False

def Flip(Side):
    if Side == "Front":
        Side = "Back"
    else:
        Side = "Front"
    return Side

def MergeSort(Data):
    if len(Data) > 1:
        Mid = len(Data) // 2
        Left = Data[:Mid]
        Right = Data[Mid:]

        MergeSort(Left)
        MergeSort(Right)

        Left_Pointer = 0
        Right_Pointer = 0
        Main_Pointer = 0
        
        while Left_Pointer < len(Left) and Right_Pointer < len(Right):
            if Left[Left_Pointer] <= Right[Right_Pointer]:
                Data[Main_Pointer] = Left[Left_Pointer]
                Left_Pointer += 1
            else:
                Data[Main_Pointer] = Right[Right_Pointer]
                Right_Pointer += 1
            Main_Pointer += 1

        while Left_Pointer < len(Left):
            Data[Main_Pointer] = Left[Left_Pointer]
            Left_Pointer += 1
            Main_Pointer += 1

        while Right_Pointer < len(Right):
            Data[Main_Pointer]= Right[Right_Pointer]
            Right_Pointer += 1
            Main_Pointer += 1

    return Data

class Login(Screen):
    def on_pre_enter(self, *args):
        self.ids.user_field.text = ""
        self.ids.password_field.text = ""
        return super().on_pre_enter(*args)
    
    def displayerror(self, dt):
        self.ids.Error.text = ""
    
    def login(self):
        global UserID

        conn, c = OpenDatabase()

        c.execute(f"SELECT Password FROM UserAccount WHERE Username = '{self.ids.user_field.text}'")
        Password = c.fetchone()
        HashedPwd = HashPassword(self.ids.password_field.text)
        if Password != None:
            if HashedPwd == Password[0]:
                c.execute(f"SELECT UserID FROM UserAccount WHERE Username = '{self.ids.user_field.text}'")
                UserID = c.fetchone()[0]
                sm.current = "Home"
            else:
                self.ids.Error.text = "The password does not match the username you have entered"
                Clock.schedule_once(self.displayerror, 2)
        else:
            self.ids.Error.text = "One or more of the fields are not filled in correctly"
            Clock.schedule_once(self.displayerror, 2)
        
        CloseDatabase(conn)

    def show_password(self, checkbox, value):
        if value:
            self.ids.password_field.password = False
            self.ids.password_text.text = "Hide Password"
            self.ids.password_field.icon_right = "eye"
        
        else:
            self.ids.password_field.password = True
            self.ids.password_text.text = "Show Password"
            self.ids.password_field.icon_right = "eye-off"

class SignUp(Screen):
    def on_pre_enter(self, *args):
        self.ids.Email_textfield.text = ""
        self.ids.user_textfield.text = ""
        self.ids.password_textfield.text = ""
        self.ids.confirm_password.text = ""
        return super().on_pre_enter(*args)

    def signup(self):
        conn, c = OpenDatabase()

        if ValidEmail(self.ids.Email_textfield.text):
            if ValidUsername(self.ids.user_textfield.text):
                if ValidPassword(self.ids.password_textfield.text):
                    if self.ids.password_textfield.text == self.ids.confirm_password.text:
                        Password = HashPassword(self.ids.password_textfield.text)
                        c.execute(f"INSERT INTO UserAccount (Username, Password, Email) VALUES ('{self.ids.user_textfield.text}', '{Password}', '{self.ids.Email_textfield.text}')")
                        sm.current = "Login"

                        c.execute(f"SELECT UserID FROM UserAccount ORDER BY UserID DESC")
                        ID = c.fetchall()[0][0]
                        CloseDatabase(conn)
                        PreMadeFlashcards(ID)
                    else:
                        self.ids.Error.text = "Passwords do not match"
                        Clock.schedule_once(self.displayerror, 2)
                        CloseDatabase(conn)
                else:
                    self.ids.Error.text = "Password does not meet the requirements"
                    Clock.schedule_once(self.displayerror, 2)
                    CloseDatabase(conn)
            else:
                self.ids.Error.text = "Username is already taken or does not meet the requiremnts"
                Clock.schedule_once(self.displayerror, 2)
                CloseDatabase(conn)
        else:
            self.ids.Error.text = "Email is not valid"
            Clock.schedule_once(self.displayerror, 2)
            CloseDatabase(conn)


    def show_password(self, checkbox, value):
        if value:
            self.ids.password_textfield.password = False
            self.ids.checkbox.text = "Hide Password"
            self.ids.password_textfield.icon_right = "eye"
            self.ids.confirm_password.password = False
            self.ids.confirm_password.icon_right = "eye"
        
        else:
            self.ids.password_textfield.password = True
            self.ids.checkbox.text = "Show Password"
            self.ids.password_textfield.icon_right = "eye-off"
            self.ids.confirm_password.password = True
            self.ids.confirm_password.icon_right = "eye-off"
    
    def displayerror(self, dt):
        self.ids.Error.text = ""

class Account(Screen):
    def on_pre_enter(self, *args):
        conn, c = OpenDatabase()
        
        self.ids.topbar.ids.searchbar.text = ""
        self.ids.topbar.ids.spinner_id.text = "Select"
        self.ids.NewUsername.text = ""
        self.ids.NewPassword.text = ""
        self.ids.NewEmail.text = ""
        self.ids.topbar.ids.Account.disabled = True

        c.execute(f"SELECT Email FROM UserAccount WHERE UserID = '{UserID}'")
        Email = c.fetchone()[0]
        self.ids.Email.text = f"Current Email: {Email}"

        c.execute(f"SELECT Username FROM UserAccount WHERE UserID = '{UserID}'")
        Username = c.fetchone()[0]
        self.ids.User.text = f"Current Username: {Username}"

        CloseDatabase(conn)
        return super().on_pre_enter(*args)
    
    def UpdateUsername(self):

        conn, c = OpenDatabase()

        if ValidUsername(self.ids.NewUsername.text):
            c.execute(f"UPDATE UserAccount SET Username = '{self.ids.NewUsername.text}' \
                      WHERE UserID = '{UserID}'")
            self.ids.User.text = f"Current Username: {self.ids.NewUsername.text}"
            self.ids.NewUsername.text = ""
            self.ids.Error.text = "Username has been changed"
            Clock.schedule_once(self.displayerror, 2)
        else:
            self.ids.Error.text = "\n The username you typed in was not valid. \n Usernames must be between 1 and 30 characters containing no spaces." 
            Clock.schedule_once(self.displayerror, 2)

        CloseDatabase(conn)

    def UpdatePassword(self):
        conn, c = OpenDatabase()

        if ValidPassword(self.ids.NewPassword.text):
            c.execute(f"UPDATE UserAccount SET Password = '{HashPassword(self.ids.NewPassword.text)}' \
                      WHERE UserID = '{UserID}'")
            self.ids.NewPassword.text = ""
            self.ids.Error.text = "Password has been changed"
            Clock.schedule_once(self.displayerror, 2)
        else:
            self.ids.Error.text = "\n \nThe password that was typed was not valid. \n Password must contain at least 1 capital letter, special character \n and number, being between 12 and 30 characters in length"
            Clock.schedule_once(self.displayerror, 2)

        CloseDatabase(conn) 

    def UpdateEmail(self):
        conn, c = OpenDatabase()

        if ValidEmail(self.ids.NewEmail.text):
            c.execute(f"UPDATE UserAccount SET Email = '{self.ids.NewEmail.text}' \
                      WHERE UserID = '{UserID}'")
            self.ids.Email.text = f"Current Username: {self.ids.NewEmail.text}"
            self.ids.NewEmail.text = ""
            self.ids.Error.text = "Email has been changed"
            Clock.schedule_once(self.displayerror, 2)
        else: 
            self.ids.Error.text = "\n The email that was typed in was not valid"
            Clock.schedule_once(self.displayerror, 2)

        CloseDatabase(conn)

    def displayerror(self, dt):
        self.ids.Error.text = ""

    def searcherror(dt):
        sm.get_screen("Account").ids.searchbar.text = ""

class CreateNotes(Screen):
    def on_pre_enter(self, *args):
        self.ids.topbar.ids.searchbar.text = ""
        self.ids.topbar.ids.spinner_id.text = "Select"
        self.ids.Title.text = ""
        self.ids.Notes.text = ""
        self.ids.topbar.ids.spinner_id.disabled = True
        self.ids.topbar.ids.searchbar.disabled = True
        self.ids.topbar.ids.Search.disabled = True
        self.ids.topbar.ids.Clear.disabled = True
        self.ids.topbar.ids.HelpButton.disabled = True
        self.ids.topbar.ids.Account.disabled = True
        self.ids.NavBar.ids.HomeButton.disabled  = True
        self.ids.NavBar.ids.LearnFlashcard.disabled  = True
        self.ids.NavBar.ids.CreateFlashcard.disabled  = True
        self.ids.NavBar.ids.ProgressButton.disabled  = True

        return super().on_pre_enter(*args)

    def FlipCard(self):
        global Side

        conn, c = OpenDatabase()

        if  PrevScreen == "Edit":
            Side = Flip(Side)

            if Side == "Back":
                    c.execute(f"UPDATE Flashcard SET FrontCard = '{self.ids.Notes.text}' \
                            WHERE FlashID = '{Flashcards[Index][0]}'")
                
                    c.execute(f"SELECT BackCard FROM Flashcard WHERE FlashID = '{Flashcards[Index][0]}'")
                    BackCard = c.fetchone()[0]
                    if BackCard == None:
                        self.ids.Notes.text = ""
                    else:
                        self.ids.Notes.text = BackCard
                

            else:
                c.execute(f"UPDATE Flashcard SET BackCard = '{self.ids.Notes.text}' \
                        WHERE FlashID = '{Flashcards[Index][0]}'")
                
                c.execute(f"SELECT FrontCard FROM Flashcard WHERE FlashID = '{Flashcards[Index][0]}'")
                FrontCard = c.fetchone()[0]
                if FrontCard == None:
                    self.ids.Notes.text = ""
                else:
                    self.ids.Notes.text = FrontCard
        
        else:
            c.execute(f"SELECT FlashID FROM Flashcard WHERE SetID = '{Set}'")
            Flash = c.fetchall()[-1][0]
            Side = Flip(Side)
            if Side == "Back":
                c.execute(f"UPDATE Flashcard SET FrontCard = '{self.ids.Notes.text}' \
                        WHERE FlashID = '{Flash}'")
            
                c.execute(f"SELECT BackCard FROM Flashcard WHERE FlashID = '{Flash}'")
                BackCard = c.fetchone()[0]
                if BackCard == None:
                    self.ids.Notes.text = ""
                else:
                    self.ids.Notes.text = BackCard
            

            else:
                c.execute(f"UPDATE Flashcard SET BackCard = '{self.ids.Notes.text}' \
                        WHERE FlashID = '{Flash}'")
                
                c.execute(f"SELECT FrontCard FROM Flashcard WHERE FlashID = '{Flash}'")
                FrontCard = c.fetchone()[0]
                if FrontCard == None:
                    self.ids.Notes.text = ""
                else:
                    self.ids.Notes.text = FrontCard

        CloseDatabase(conn)

    def save(self):
        global Side

        conn, c = OpenDatabase()

        if PrevScreen == "Edit":
            c.execute(f"UPDATE Flashcard SET Title = '{self.ids.Title.text}' \
                    WHERE FlashID = '{Flashcards[Index][0]}'")
            if Side == "Front":
                c.execute(f"UPDATE Flashcard SET FrontCard = '{self.ids.Notes.text}' \
                        WHERE FlashID = '{Flashcards[Index][0]}'")
            else:
                c.execute(f"UPDATE Flashcard SET BackCard = '{self.ids.Notes.text}' \
                        WHERE FlashID = '{Flashcards[Index][0]}'")
        else:
            c.execute(f"SELECT FlashID FROM Flashcard WHERE SetID = '{Set}'")
            Flashcard = c.fetchall()[-1][0]
            c.execute(f"UPDATE Flashcard SET Title = '{self.ids.Title.text}' \
                    WHERE FlashID = '{Flashcard}'")
            if Side == "Front":
                c.execute(f"UPDATE Flashcard SET FrontCard = '{self.ids.Notes.text}' \
                        WHERE FlashID = '{Flashcard}'")
            else:
                c.execute(f"UPDATE Flashcard SET BackCard = '{self.ids.Notes.text}' \
                        WHERE FlashID = '{Flashcard}'")
                
        CloseDatabase(conn)
    
    def displayerror(self, dt):
        conn, c = OpenDatabase()

        c.execute(f"SELECT Title FROM Flashcard WHERE SetID = '{Set}' ORDER BY FlashID DESC")
        Title = c.fetchone()[0]
        if Title == None:
            self.ids.Title.text = ""
        else:
            self.ids.Title.text = Title

        CloseDatabase(conn)

    def check(self, button):
        conn, c = OpenDatabase()

        c.execute(f"SELECT * FROM Flashcard WHERE SetID = '{Set}' ORDER BY FlashID DESC")
        Flashcard = c.fetchall()[0]

        if Flashcard[5] == 0:
            if Flashcard[2] == "" or Flashcard[3] == "" or Flashcard[4] == "" \
                or Flashcard[2] == None or Flashcard[3] == None or Flashcard[4] == None:
                self.ids.Title.text = "You have not filled in all of the required fields"
                Clock.schedule_once(self.displayerror, 2)
                CloseDatabase(conn)
                return False
        else:
            if Flashcard[2] == "" or Flashcard[3] == "" \
                or Flashcard[2] == None or Flashcard[3] == None:
                self.ids.Title.text = "You have not filled in all of the required fields"
                Clock.schedule_once(self.displayerror, 2)
                CloseDatabase(conn)
                return False
       
        if button == "Finish":
            sm.current = "Home"
        else:
            sm.current = "CreateSelection"

        c.execute(f"SELECT NumCards FROM FlashcardSet WHERE SetID = '{Set}'")
        Num = c.fetchone()[0]
        c.execute(f"UPDATE FlashcardSet SET NumCards = {Num+1} WHERE SetID = '{Set}'")

        CloseDatabase(conn)

    def back(self):
        conn, c = OpenDatabase()

        if PrevScreen == "CreateSelection":
            c.execute(f"SELECT FlashID FROM Flashcard WHERE SetID = '{Set}'")
            Flash = c.fetchall()[-1][0]
            c.execute(f"DELETE FROM Flashcard WHERE FlashID = '{Flash}'")
            sm.current = "CreateSelection"
        else:
            sm.current = "Edit"

        CloseDatabase(conn)   


    def searcherror(dt):
        sm.get_screen("CreateNotes").ids.searchbar.text = ""

class CreateSelection(Screen):
    def on_pre_enter(self, *args):
        self.ids.topbar.ids.searchbar.text = ""
        self.ids.topbar.ids.spinner_id.text = "Select"
        self.ids.NavBar.ids.CreateFlashcard.disabled = True
        self.ids.spinner_id.text = "Flashcard Set"
        self.ids.click_label.text = "Pick the flashcard set below"
        self.ids.Easy.icon = "close"
        self.ids.Medium.icon = "close"
        self.ids.Hard.icon = "close"

        self.ids.SetTitle.clear_widgets()
        self.ids.Create.disabled = False

        return super().on_pre_enter(*args)
    
    def spinner_clicked(self, value):
        self.ids.click_label.text = f'You selected set: {value}'
        self.ids.spinner_id.text = value

    def addtextinput(self):
        self.ids.Create.disabled = True
        self.ids.SetTitle.add_widget(InputAndButton())

    def Format(self, Format):
        global Set, Side, PrevScreen

        conn, c = OpenDatabase()

        PrevScreen = "CreateSelection"

        if self.ids.spinner_id.text == "Flashcard Set":
            self.ids.Error.text = "You have not selected a set"
            Clock.schedule_once(self.displayerror, 2)
            return False
        c.execute(f"SELECT SetID FROM FlashcardSet WHERE SetName = '{self.ids.spinner_id.text}' \
            and UserID = '{UserID}'")
        Set = c.fetchone()[0]
        if self.ids.Easy.icon == "close" and self.ids.Medium.icon == "close" and self.ids.Hard.icon == "close":
            self.ids.Error.text = "You have not selected a difficulty"
            Clock.schedule_once(self.displayerror, 2)
            return False
        elif self.ids.Easy.icon == "check":
            Difficulty = "Easy"
        elif self.ids.Medium.icon == "check":
            Difficulty = "Medium"
        elif self.ids.Hard.icon == "check":
            Difficulty = "Hard"
        c.execute(f"INSERT INTO Flashcard (SetID, Format, Learnt, Flagged, Viewed, Difficulty) VALUES ({Set}, {Format}, 0, 0, 0, '{Difficulty}')")
        

        c.execute(f"INSERT INTO MainProgress (SetID) VALUES ('{Set}')")

        sm.current = "CreateNotes"
        if Format == 1:
            sm.get_screen("CreateNotes").ids.FlipCard.disabled = True
        else:
            sm.get_screen("CreateNotes").ids.FlipCard.disabled = False

        Side = "Front"
        CloseDatabase(conn)
    
    def displayerror(self, dt):
        self.ids.Error.text = ""

    def searcherror(dt):
        sm.get_screen("CreateSelection").ids.searchbar.text = ""

class Help(Screen):
    def on_pre_enter(self, *args):
        self.ids.topbar.ids.searchbar.text = ""
        self.ids.topbar.ids.spinner_id.text = "Select"
        self.ids.helpbox.text = ""
        self.ids.topbar.ids.HelpButton.disabled = True
        self.ids.Iconitem1.icon = "minus" 
        self.ids.Iconitem2.icon = "minus"
        self.ids.Iconitem3.icon = "minus"
        self.ids.Iconitem4.icon = "minus"
        self.ids.Iconitem5.icon = "minus"
        self.ids.Iconitem6.icon = "minus"
        self.ids.Iconitem7.icon = "minus"

        
        return super().on_pre_enter(*args)
    
    def press(self, pressed, list_id):
        if list_id == "item1":
            self.ids.helpbox.text = "To change your username, you will first have to access the account page, which can be done by pressing the account button at the top of the screen. Then you can view what your current username and have the ability to change it as long it is between 1 and 30 characters and is unique."
            self.ids.Iconitem1.icon = "check" 
            self.ids.Iconitem2.icon = "minus"
            self.ids.Iconitem3.icon = "minus"
            self.ids.Iconitem4.icon = "minus"
            self.ids.Iconitem5.icon = "minus"
            self.ids.Iconitem6.icon = "minus"
            self.ids.Iconitem7.icon = "minus"
        elif list_id == "item2":
            self.ids.helpbox.text = "To change your password, you will first have to access the account page, which can be done by pressing the account button at the top of the screen. Then you can change your password as long as it is between 12 and 30 characters, containing at least 1 capital letter, lowercase letter, number and special character"
            self.ids.Iconitem1.icon = "minus" 
            self.ids.Iconitem2.icon = "check"
            self.ids.Iconitem3.icon = "minus"
            self.ids.Iconitem4.icon = "minus"
            self.ids.Iconitem5.icon = "minus"
            self.ids.Iconitem6.icon = "minus"
            self.ids.Iconitem7.icon = "minus"
        elif list_id == "item3":
            self.ids.helpbox.text = "To change your email, you will first have to access the account page, which can be done by pressing the account button at the top of the screen. Then you can view what your current email and have the ability to change it as long it is a valid email."
            self.ids.Iconitem1.icon = "minus" 
            self.ids.Iconitem2.icon = "minus"
            self.ids.Iconitem3.icon = "check"
            self.ids.Iconitem4.icon = "minus"
            self.ids.Iconitem5.icon = "minus"
            self.ids.Iconitem6.icon = "minus"
            self.ids.Iconitem7.icon = "minus"
        elif list_id == "item4":
            self.ids.helpbox.text = "To create a flashcard, go to the create flashcard section. Then you will need to select a flashcard set, which if there is not one, then you must create one. From there you can select which format of flashcard you want."
            self.ids.Iconitem1.icon = "minus" 
            self.ids.Iconitem2.icon = "minus"
            self.ids.Iconitem3.icon = "minus"
            self.ids.Iconitem4.icon = "check"
            self.ids.Iconitem5.icon = "minus"
            self.ids.Iconitem6.icon = "minus"
            self.ids.Iconitem7.icon = "minus"
        elif list_id == "item5":
            self.ids.helpbox.text = "To learn a flashcard set, go to the learn flashcard section. Then you will need to select which set you want to learn and which type of flashcards (e.g flagged flashcards etc)."
            self.ids.Iconitem1.icon = "minus" 
            self.ids.Iconitem2.icon = "minus"
            self.ids.Iconitem3.icon = "minus"
            self.ids.Iconitem4.icon = "minus"
            self.ids.Iconitem5.icon = "check"
            self.ids.Iconitem6.icon = "minus"
            self.ids.Iconitem7.icon = "minus"
        elif list_id == "item6":
            self.ids.helpbox.text = "To edit a flashcard set, go to the learn flashcard section. Then you will need to select which flashcard set you would like to edit. Then you can scroll through the card using the next and previous buttons to either delete the card or edit the contents of the card"
            self.ids.Iconitem1.icon = "minus" 
            self.ids.Iconitem2.icon = "minus"
            self.ids.Iconitem3.icon = "minus"
            self.ids.Iconitem4.icon = "minus"
            self.ids.Iconitem5.icon = "minus"
            self.ids.Iconitem6.icon = "check"
            self.ids.Iconitem7.icon = "minus"
        elif list_id == "item7":
            self.ids.helpbox.text = "To look at your progress of the set go to the progress section. From there, select which set you would like to see your progress and which graph you would like to see from the available options: The percentage of flashcards viewed, percentage of flashcards learnt and the percenatge of flashcards flagged. This is trcaked over the last 10 sessions."
            self.ids.Iconitem1.icon = "minus" 
            self.ids.Iconitem2.icon = "minus"
            self.ids.Iconitem3.icon = "minus"
            self.ids.Iconitem4.icon = "minus"
            self.ids.Iconitem5.icon = "minus"
            self.ids.Iconitem6.icon = "minus"
            self.ids.Iconitem7.icon = "check"
        
    def searcherror(dt):
        sm.get_screen("Help").ids.searchbar.text = ""
class Home(Screen):
    def on_pre_enter(self,*args):
        self.ids.topbar.ids.searchbar.text = ""
        self.ids.topbar.ids.spinner_id.text = "Select"
        self.ids.NavBar.ids.HomeButton.disabled = True
    
        conn, c = OpenDatabase()

        c.execute(f"SELECT SetName FROM FlashcardSet WHERE UserID = '{UserID}' ORDER BY LastOpened DESC")
        RecentActivity = c.fetchall()
        if len(RecentActivity) == 0:
            self.ids.Recent1.disabled = True
            self.ids.Recent2.disabled = True
            self.ids.Recent3.disabled = True
        elif len(RecentActivity) == 1:
            self.ids.Recent1.text = f"Learn: {RecentActivity[0][0]}"
            self.ids.Recent1.disabled = False
            self.ids.Recent2.disabled = True
            self.ids.Recent3.disabled = True
        elif len(RecentActivity) == 2:
            self.ids.Recent1.text = f"Learn: {RecentActivity[0][0]}"
            self.ids.Recent2.text = f"Learn: {RecentActivity[1][0]}"
            self.ids.Recent1.disabled = False
            self.ids.Recent2.disabled = False
            self.ids.Recent3.disabled = True
        else:
            self.ids.Recent1.text = f"Learn: {RecentActivity[0][0]}"
            self.ids.Recent2.text = f"Learn: {RecentActivity[1][0]}"
            self.ids.Recent3.text = f"Learn: {RecentActivity[2][0]}"
            self.ids.Recent1.disabled = False
            self.ids.Recent2.disabled = False
            self.ids.Recent3.disabled = False

        CloseDatabase(conn)

        return super().on_pre_enter(*args)

    def GoToSet(self, Index):
        conn, c = OpenDatabase()

        c.execute(f"SELECT SetName FROM FlashcardSet WHERE UserID = '{UserID}' ORDER BY LastOpened DESC")
        RecentActivity = c.fetchall()
        sm.get_screen("LearnSelection").ids.spinner_id.text = RecentActivity[Index][0]

        c.execute(f"SELECT NumCards FROM FlashcardSet WHERE UserID = '{UserID}' AND SetName = '{RecentActivity[Index][0]}'")
        NumCards = c.fetchone()[0]
        if NumCards == 0:
            self.ids.Error.text = "The set that you have selected contains no cards"
        else:
            LearnNotes.loadnotes(LearnNotes(), "Learn")
            sm.current = "LearnNotes"


        CloseDatabase(conn)
        
    
    def searcherror(dt):
        sm.get_screen("Home").ids.searchbar.text = ""

class LearnNotes(Screen):
    def on_pre_enter(self, *args):
        self.ids.topbar.ids.searchbar.text = ""
        self.ids.topbar.ids.spinner_id.text = "Select"
        return super().on_pre_enter(*args)
        
    def loadnotes(self, Condition):
        global Flashcards, Index, SideCard
        print(self)

        conn, c = OpenDatabase()

        if sm.get_screen('LearnSelection').ids.spinner_id.text == "Flashcard Set":
            sm.get_screen('LearnSelection').ids.spinner_id.text = "You have not selected a set"
            Clock.schedule_once(LearnSelection.LoadError, 2)

            CloseDatabase(conn)
            return False

        Index = 0
        c.execute(f"SELECT SetID FROM FlashcardSet WHERE SetName = '{sm.get_screen('LearnSelection').ids.spinner_id.text}' \
                  and UserID = '{UserID}'")
        S_ID = c.fetchone()
        
        if Condition == "Learn":
            Screen = "LearnNotes"
            c.execute(f"UPDATE Flashcard SET Viewed = 0 WHERE SetID = '{S_ID[0]}'")
            c.execute(f"UPDATE Flashcard SET Flagged = 0 WHERE SetID = '{S_ID[0]}'")
            c.execute(f"UPDATE Flashcard SET Learnt = 0 WHERE SetID = '{S_ID[0]}'")
            c.execute(f"SELECT * FROM Flashcard WHERE SetID = '{S_ID[0]}'")
            sm.get_screen("LearnNotes").ids.FlagButton.disabled = False
            sm.get_screen("LearnNotes").ids.LearntButton.disbaled  = False
            Flashcards = c.fetchall()
        
        elif Condition == "Edit":
            Screen = "Edit"
            c.execute(f"SELECT * FROM Flashcard WHERE SetID = '{S_ID[0]}'")
            Flashcards = c.fetchall()

        elif Condition == "Learnt":
            Screen = "LearnNotes"
            c.execute(f"SELECT * FROM Flashcard WHERE SetID = '{S_ID[0]}' AND Learnt = 1")
            Flashcards = c.fetchall()
            sm.get_screen("LearnNotes").ids.FlagButton.disabled = True
            sm.get_screen("LearnNotes").ids.LearntButton.disbaled  = True

        elif Condition == "Flagged":
            Screen = "LearnNotes"
            c.execute(f"SELECT * FROM Flashcard WHERE SetID = '{S_ID[0]}' AND Flagged = 1")
            Flashcards = c.fetchall()
            sm.get_screen("LearnNotes").ids.FlagButton.disabled = True
            sm.get_screen("LearnNotes").ids.LearntButton.disbaled  = True

        elif Condition == "Easy":
            Screen = "LearnNotes"
            c.execute(f"SELECT * FROM Flashcard WHERE SetID = '{S_ID[0]}' AND Difficulty = 'Easy'")
            Flashcards = c.fetchall()
            sm.get_screen("LearnNotes").ids.FlagButton.disabled = True
            sm.get_screen("LearnNotes").ids.LearntButton.disbaled  = True

        elif Condition == "Medium":
            Screen = "LearnNotes"
            c.execute(f"SELECT * FROM Flashcard WHERE SetID = '{S_ID[0]}' AND Difficulty = 'Medium'")
            Flashcards = c.fetchall()
            sm.get_screen("LearnNotes").ids.FlagButton.disabled = True
            sm.get_screen("LearnNotes").ids.LearntButton.disbaled  = True

        elif Condition == "Hard":
            Screen = "LearnNotes"
            c.execute(f"SELECT * FROM Flashcard WHERE SetID = '{S_ID[0]}' AND Difficulty = 'Hard'")
            Flashcards = c.fetchall()
            sm.get_screen("LearnNotes").ids.FlagButton.disabled = True
            sm.get_screen("LearnNotes").ids.LearntButton.disbaled  = True

        if len(Flashcards) == 0:
            sm.get_screen('LearnSelection').ids.spinner_id.text = "This set contains no flashcards"
            Clock.schedule_once(LearnSelection.LoadError, 2)
            CloseDatabase(conn)
            return False
        
        elif len(Flashcards) == 1: 
            sm.get_screen(Screen).ids.Next.disabled = True
            sm.get_screen(Screen).ids.Previous.disabled = True
        
        else:
            sm.get_screen(Screen).ids.Next.disabled = False
            sm.get_screen(Screen).ids.Previous.disabled = False

        c.execute(f"SELECT Format FROM Flashcard WHERE FlashID = '{Flashcards[Index][0]}'")
        Format = c.fetchone()[0]
        if Format == 1:
            sm.get_screen(Screen).ids.Flip.disabled = True
        else:
            sm.get_screen(Screen).ids.Flip.disabled = False
            
        c.execute(f"SELECT FrontCard FROM Flashcard WHERE FlashID = '{Flashcards[Index][0]}'")
        FrontCard = c.fetchone()[0]
        sm.get_screen(Screen).ids.Notes.text = FrontCard

        c.execute(f"SELECT Title FROM Flashcard WHERE FlashID = '{Flashcards[Index][0]}'")
        Title = c.fetchone()[0]
        sm.get_screen(Screen).ids.Title.text = Title

        if Screen == "LearnNotes":
            c.execute(f"SELECT Learnt FROM Flashcard WHERE FlashID = '{Flashcards[Index][0]}'")
            Learnt = c.fetchone()[0]
            if Learnt == 1:
                sm.get_screen(Screen).ids.LearntButton.icon = "check"
            else:
                sm.get_screen(Screen).ids.LearntButton.icon = "close"

            c.execute(f"SELECT Flagged FROM Flashcard WHERE FlashID = '{Flashcards[Index][0]}'")
            flag = c.fetchone()[0]
            if flag == 1:
                sm.get_screen(Screen).ids.FlagButton.icon = "check"
            else:
                sm.get_screen(Screen).ids.FlagButton.icon = "close"

            c.execute(f"UPDATE Flashcard SET Viewed = 1 WHERE FlashID = '{Flashcards[Index][0]}'")
            timestamp = int(time.time())
            c.execute(f"UPDATE FlashcardSet SET LastOpened = '{timestamp}' WHERE SetID = '{S_ID}'")

        SideCard = "Front"
        
        if Screen == "LearnNotes":
            sm.current = "LearnNotes"
        elif Screen == "Edit":
            c.execute(f"SELECT Difficulty FROM Flashcard WHERE FlashID = {Flashcards[Index][0]}")
            Difficulty = c.fetchone()[0]
            sm.get_screen("Edit").ids.ChangeDifficulty.text = f"Difficulty: {Difficulty}"
            sm.current = "Edit"

        CloseDatabase(conn)

    def Previous(self):
        global Index, SideCard

        conn, c = OpenDatabase()

        Index -= 1
        if Index < 0:
            Index = len(Flashcards) - 1

        c.execute(f"SELECT Title FROM Flashcard WHERE FlashID = '{Flashcards[Index][0]}'")
        Title = c.fetchone()[0]
        self.ids.Title.text = Title

        c.execute(f"SELECT FrontCard FROM Flashcard WHERE FlashID = '{Flashcards[Index][0]}'")
        FrontCard = c.fetchone()[0]
        self.ids.Notes.text = FrontCard

        c.execute(f"SELECT Format FROM Flashcard WHERE FlashID = '{Flashcards[Index][0]}'")
        Format = c.fetchone()[0]
        if Format == 1:
            self.ids.Flip.disabled = True
        else:
            self.ids.Flip.disabled = False

    
        c.execute(f"SELECT Learnt FROM Flashcard WHERE FlashID = '{Flashcards[Index][0]}'")
        Learnt = c.fetchone()[0]
        if Learnt == 1:
            self.ids.LearntButton.icon = "check"
        else:
            self.ids.LearntButton.icon = "close"

        c.execute(f"SELECT Flagged FROM Flashcard WHERE FlashID = '{Flashcards[Index][0]}'")
        flag = c.fetchone()[0]
        if flag == 1:
            self.ids.FlagButton.icon = "check"
        else:
            self.ids.FlagButton.icon = "close"

        c.execute(f"UPDATE Flashcard SET Viewed = 1 WHERE FlashID = '{Flashcards[Index][0]}'")

        SideCard = "Front"

        CloseDatabase(conn)

    def Flag(self):
        conn, c = OpenDatabase()

        c.execute(f"SELECT Flagged FROM Flashcard WHERE FlashID = '{Flashcards[Index][0]}'")
        flag = c.fetchone()[0]

        if flag == 0:
            c.execute(f"UPDATE Flashcard SET Flagged = 1 WHERE FlashID = '{Flashcards[Index][0]}'")
            self.ids.FlagButton.icon = "check"
        else:
            c.execute(f"UPDATE Flashcard SET Flagged = 0 WHERE FlashID = '{Flashcards[Index][0]}'")
            self.ids.FlagButton.icon = "close"

        CloseDatabase(conn)

    def Learnt(self):
        conn, c = OpenDatabase()
        c.execute(f"SELECT Learnt FROM Flashcard WHERE FlashID = '{Flashcards[Index][0]}'")
        Learnt = c.fetchone()[0]

        if Learnt == 0:
            c.execute(f"UPDATE Flashcard SET Learnt = 1 WHERE FlashID = '{Flashcards[Index][0]}'")
            self.ids.LearntButton.icon = "check"
        else:
            c.execute(f"UPDATE Flashcard SET Learnt = 0 WHERE FlashID = '{Flashcards[Index][0]}'")
            self.ids.LearntButton.icon = "close"

        CloseDatabase(conn)

    def FlipCard(self):
        global SideCard
        
        conn, c = OpenDatabase()

        SideCard = Flip(SideCard)
        if SideCard == "Back":
            c.execute(f"SELECT BackCard FROM Flashcard WHERE FlashID = '{Flashcards[Index][0]}'")
            BackCard = c.fetchone()[0]
            self.ids.Notes.text = BackCard
        else:
            c.execute(f"SELECT FrontCard FROM Flashcard WHERE FlashID = '{Flashcards[Index][0]}'")
            FrontCard = c.fetchone()[0]
            self.ids.Notes.text = FrontCard

        CloseDatabase(conn)

    def Next(self):
        global Index, SideCard, Flashcards

        conn, c = OpenDatabase()
            
        Index += 1
        if Index == len(Flashcards):
            Index = 0

        c.execute(f"SELECT Title FROM Flashcard WHERE FlashID = '{Flashcards[Index][0]}'")
        Title = c.fetchone()[0]
        self.ids.Title.text = Title

        c.execute(f"SELECT FrontCard FROM Flashcard WHERE FlashID = '{Flashcards[Index][0]}'")
        FrontCard = c.fetchone()[0]
        self.ids.Notes.text = FrontCard

        c.execute(f"SELECT Format FROM Flashcard WHERE FlashID = '{Flashcards[Index][0]}'")
        Format = c.fetchone()[0]
        if Format == 1:
            self.ids.Flip.disabled = True
        else:
            self.ids.Flip.disabled = False

        c.execute(f"SELECT Learnt FROM Flashcard WHERE FlashID = '{Flashcards[Index][0]}'")
        Learnt = c.fetchone()[0]
        if Learnt == 1:
            self.ids.LearntButton.icon = "check"
        else:
            self.ids.LearntButton.icon = "close"

        c.execute(f"SELECT Flagged FROM Flashcard WHERE FlashID = '{Flashcards[Index][0]}'")
        flag = c.fetchone()[0]
        if flag == 1:
            self.ids.FlagButton.icon = "check"
        else:
            self.ids.FlagButton.icon = "close"

        c.execute(f"UPDATE Flashcard SET Viewed = 1 WHERE FlashID = '{Flashcards[Index][0]}'")

        SideCard = "Front"

        CloseDatabase(conn)

    def close(self):
        conn, c = OpenDatabase()

        NumCards = len(Flashcards)
        c.execute(f"SELECT * FROM Flashcard WHERE SetID = '{Flashcards[0][1]}' AND Viewed = 1")
        Viewed = c.fetchall()
        c.execute(f"SELECT * FROM Flashcard WHERE SetID = '{Flashcards[0][1]}' AND Flagged = 1")
        Flagged = c.fetchall()
        c.execute(f"SELECT * FROM Flashcard WHERE SetID = '{Flashcards[0][1]}' AND Learnt = 1")
        Learnt = c.fetchall()


        ProgressV = (len(Viewed)/NumCards)*100
        ProgressF = (len(Flagged)/NumCards)*100
        ProgressL = (len(Learnt)/NumCards)*100

        c.execute(f"SELECT ProgressID FROM MainProgress WHERE SetID = '{Flashcards[0][1]}'")
        P_ID = c.fetchone()[0]

        c.execute(f"SELECT ViewedID FROM ProgressViewed WHERE ProgressID = '{P_ID}' ORDER BY ViewedID ASC")
        NumViewed = c.fetchall()
        if len(NumViewed) == 10: 
            c.execute(f"DELETE FROM ProgressViewed WHERE ViewedID = '{NumViewed[0][0]}")

        c.execute(f"SELECT FlaggedID FROM ProgressFlagged WHERE ProgressID = '{P_ID}' ORDER BY FlaggedID ASC")
        NumFlagged = c.fetchall()
        if len(NumFlagged) == 10: 
            c.execute(f"DELETE FROM ProgressFlagged WHERE FlaggedID = '{NumFlagged[0][0]}")

        c.execute(f"SELECT LearntID FROM ProgressLearnt WHERE ProgressID = '{P_ID}' ORDER BY LearntID ASC")
        NumLearnt = c.fetchall()
        if len(NumLearnt) == 10: 
            c.execute(f"DELETE FROM ProgressLearnt WHERE LearntID = '{NumLearnt[0][0]}")

        timestamp = int(time.time())

        c.execute(f"INSERT INTO ProgressViewed (ProgressID, ProgressV, ViewedDate) VALUES ({P_ID}, {ProgressV}, {timestamp})")
        c.execute(f"INSERT INTO ProgressFlagged (ProgressID, ProgressF, FlaggedDate) VALUES ({P_ID}, {ProgressF}, {timestamp})")
        c.execute(f"INSERT INTO ProgressLearnt (ProgressID, ProgressL, LearntDate) VALUES ({P_ID}, {ProgressL}, {timestamp})")

        CloseDatabase(conn)

    def searcherror(dt):
        sm.get_screen("LearnNotes").ids.searchbar.text = ""
class LearnSelection(Screen):
    def on_pre_enter(self, *args):
        self.ids.topbar.ids.searchbar.text = ""
        self.ids.topbar.ids.spinner_id.text = "Select"
        self.ids.spinner_id.text = "Flashcard Set"
        self.ids.click_label.text = "Pick the flashcard set below"

        return super().on_pre_enter(*args)
    
    def spinner_clicked(self, value):
        if self.ids.spinner_id.text == "You have not selected a set" \
            or self.ids.spinner_id.text == "This set contains no flashcards" \
                or self.ids.spinner_id.text == "Flashcard Set":
            self.ids.click_label.text = "Pick the flashcard set below"
        else:
            self.ids.click_label.text = f'You selected set: {value}'
            self.ids.spinner_id.text = value

    def Delete(self):
        conn, c = OpenDatabase()

        if self.ids.spinner_id.text == "Flashcard Set":
            self.ids.spinner_id.text = "No set was selected"
            Clock.schedule_once(self.LoadError, 2)
            CloseDatabase(conn)
            return False
        
        c.execute(f"SELECT SetID FROM FlashcardSet WHERE SetName = '{self.ids.spinner_id.text}' \
                  and UserID = '{UserID}'")
        S_ID = c.fetchone()[0]

        c.execute(f"SELECT ProgressID FROM MainProgress WHERE SetID = {S_ID}")
        ProgressID = c.fetchone()

        c.execute(f"DELETE FROM FlashcardSet WHERE SetID = '{S_ID}' AND UserID = '{UserID}'")
        c.execute(f"DELETE FROM Flashcard WHERE SetID = '{S_ID}'")

        if ProgressID != None:
            c.execute(f"DELETE FROM MainProgress WHERE ProgressID = '{ProgressID[0]}'")
            c.execute(f"DELETE FROM ProgressViewed WHERE ProgressID = '{ProgressID[0]}'")
            c.execute(f"DELETE FROM ProgressLearnt WHERE ProgressID = '{ProgressID[0]}'")
            c.execute(f"DELETE FROM ProgressFlagged WHERE ProgressID = '{ProgressID[0]}'")
        
        self.ids.spinner_id.text = "Flashcard Set"
        self.ids.click_label.text = "Pick the flashcard set below"

        CloseDatabase(conn)
        
    def LoadError(dt):
        sm.get_screen("LearnSelection").ids.spinner_id.text = "Flashcard Set"

    def searcherror(dt):
        sm.get_screen("LearnSelection").ids.searchbar.text = ""
class Progress(Screen):
    def on_pre_enter(self, *args):
        self.ids.topbar.ids.searchbar.text = ""
        self.ids.topbar.ids.spinner_id.text = "Select"
        self.ids.NavBar.ids.ProgressButton.disabled = True
        self.ids.spinner_id.text = "Flashcard Set"
        self.ids.click_label.text = "Pick the flashcard set below"
        conn, c = OpenDatabase()

        self.ids.spinner_id.values = []
        c.execute(f"SELECT SetName FROM FlashcardSet WHERE UserID = '{UserID}'")
        Sets = c.fetchall()
        Sets = MergeSort(Sets)
        for row in range(len(Sets)):
            self.ids.spinner_id.values.append(Sets[row][0])

        CloseDatabase(conn)
        return super().on_pre_enter(*args)
    
    def spinner_clicked(self, value):
        if self.ids.spinner_id.text == "No set was selected" \
            or self.ids.spinner_id.text == "You have not learnt this set yet" \
                or self.ids.spinner_id.text == "Flashcard Set":
            self.ids.click_label.text = "Pick the flashcard set below"
        else:
            self.ids.click_label.text = f'You selected set: {value}'
            self.ids.spinner_id.text = value

    def PlotViewed(self):
        conn, c = OpenDatabase()

        if self.ids.spinner_id.text == "Flashcard Set":
            self.ids.spinner_id.text = "No set was selected"
            Clock.schedule_once(self.LoadError, 2)
            CloseDatabase(conn)
            return False

        plt.clf()
        sm.get_screen("Graph").ids.box.clear_widgets() 
        sm.get_screen("Graph").ids.box.add_widget(FigureCanvasKivyAgg(plt.gcf()))

        c.execute(f"SELECT SetID FROM FlashcardSet WHERE SetName = '{self.ids.spinner_id.text}' \
                   AND UserID = '{UserID}'")
        SetId = c.fetchone()[0]
        c.execute(f"SELECT ProgressID FROM MainProgress WHERE SetID = '{SetId}'")
        P_ID = c.fetchone()

        if P_ID == None: 
            self.ids.spinner_id.text = "You have not learnt this set yet"
            Clock.schedule_once(self.LoadError, 2)
            CloseDatabase(conn)
            return False


        c.execute(f"SELECT ProgressV FROM ProgressViewed WHERE ProgressID = '{P_ID[0]}' ORDER BY ViewedID ASC")
        Viewed = c.fetchall()

        c.execute(f"SELECT ViewedDate FROM ProgressViewed WHERE ProgressID = '{P_ID[0]}' ORDER BY ViewedID ASC")
        Times = c.fetchall()
        Dates = []
        for Time in range(len(Times)):
            Dates.append(datetime.datetime.fromtimestamp(int(f"{Times[Time][0]}")).strftime('%d-%m-%Y %H:%M:%S'))
        
        x = [1,2,3,4,5,6,7,8,9,10]
        y = []

        for Card in range(len(Viewed)):
            y.append(Viewed[Card][0])

        
        c.execute(f"SELECT MIN(ProgressV) FROM ProgressViewed WHERE ProgressID = '{P_ID[0]}'")
        Min = c.fetchone()[0] 
        c.execute(f"SELECT MAX(ProgressV) FROM ProgressViewed WHERE ProgressID = '{P_ID[0]}'")
        Max = c.fetchone()[0]
        c.execute(f"SELECT AVG(ProgressV) FROM ProgressViewed WHERE ProgressID = '{P_ID[0]}'")
        Avg = c.fetchone()[0]
        
        while len(y) != 10:
            y.append(0)

        while len(Dates) != 10:
            Dates.append("None")


        plt.plot(x,y)
        plt.ylabel("Percentage Viewed")
        plt.xlabel("Sessions")
        plt.title("Percentage of flashcards viewed in the set")

        sm.get_screen("Graph").ids.Highest.text = f"The highest percentage is {Max}%"
        sm.get_screen("Graph").ids.Lowest.text = f"The lowest percentage is {Min}%"
        sm.get_screen("Graph").ids.Average.text = f"The average percentage is {Avg}%"

        sm.get_screen("Graph").ids.Session1.text = f"Session 1: {Dates[0]}"
        sm.get_screen("Graph").ids.Session2.text = f"Session 2: {Dates[1]}"
        sm.get_screen("Graph").ids.Session3.text = f"Session 3: {Dates[2]}"
        sm.get_screen("Graph").ids.Session4.text = f"Session 4: {Dates[3]}"
        sm.get_screen("Graph").ids.Session5.text = f"Session 5: {Dates[4]}"
        sm.get_screen("Graph").ids.Session6.text = f"Session 6: {Dates[5]}"
        sm.get_screen("Graph").ids.Session7.text = f"Session 7: {Dates[6]}"
        sm.get_screen("Graph").ids.Session8.text = f"Session 8: {Dates[7]}"
        sm.get_screen("Graph").ids.Session9.text = f"Session 9: {Dates[8]}"
        sm.get_screen("Graph").ids.Session10.text = f"Session 10: {Dates[9]}"

        sm.current = "Graph"

        CloseDatabase(conn)

    def PlotFlagged(self):
        conn, c = OpenDatabase()

        if self.ids.spinner_id.text == "Flashcard Set":
            self.ids.spinner_id.text = "No set was selected"
            Clock.schedule_once(self.LoadError, 2)
            CloseDatabase(conn)
            return False

        plt.clf()
        sm.get_screen("Graph").ids.box.clear_widgets() 
        sm.get_screen("Graph").ids.box.add_widget(FigureCanvasKivyAgg(plt.gcf()))

        sm.current = "Graph"
         
        c.execute(f"SELECT SetID FROM FlashcardSet WHERE SetName = '{self.ids.spinner_id.text}' \
                   AND UserID = '{UserID}'")
        SetId = c.fetchone()[0]
        c.execute(f"SELECT ProgressID FROM MainProgress WHERE SetID = '{SetId}'")
        P_ID = c.fetchone()[0]

        c.execute(f"SELECT ProgressF FROM ProgressFlagged WHERE ProgressID = '{P_ID}' ORDER BY FlaggedID ASC")
        Flagged = c.fetchall()

        c.execute(f"SELECT FlaggedDate FROM ProgressFlagged WHERE ProgressID = '{P_ID}' ORDER BY FlaggedID ASC")
        Times = c.fetchall()
        Dates = []
        for Time in range(len(Times)):
            Dates.append(datetime.datetime.fromtimestamp(int(f"{Times[Time][0]}")).strftime('%d-%m-%Y %H:%M:%S'))

        x = [1,2,3,4,5,6,7,8,9,10]
        y = []

        for Card in range(len(Flagged)):
            y.append(Flagged[Card][0])

        c.execute(f"SELECT MIN(ProgressF) FROM ProgressFlagged WHERE ProgressID = '{P_ID}'")
        Min = c.fetchone()[0] 
        c.execute(f"SELECT MAX(ProgressF) FROM ProgressFlagged WHERE ProgressID = '{P_ID}'")
        Max = c.fetchone()[0]
        c.execute(f"SELECT AVG(ProgressF) FROM ProgressFlagged WHERE ProgressID = '{P_ID}'")
        Avg = c.fetchone()[0]

        while len(y) != 10:
            y.append(0)

        while len(Dates) != 10:
            Dates.append("None")
                    
        plt.plot(x,y)
        plt.ylabel("Percentage Flagged")
        plt.xlabel("Sessions")
        plt.title("Percentage of flashcards flagged in the set")

        sm.get_screen("Graph").ids.Highest.text = f"The highest percentage is {Max}%"
        sm.get_screen("Graph").ids.Lowest.text = f"The lowest percentage is {Min}%"
        sm.get_screen("Graph").ids.Average.text = f"The average percentage is {Avg}%"

        sm.get_screen("Graph").ids.Session1.text = f"Session 1: {Dates[0]}"
        sm.get_screen("Graph").ids.Session2.text = f"Session 2: {Dates[1]}"
        sm.get_screen("Graph").ids.Session3.text = f"Session 3: {Dates[2]}"
        sm.get_screen("Graph").ids.Session4.text = f"Session 4: {Dates[3]}"
        sm.get_screen("Graph").ids.Session5.text = f"Session 5: {Dates[4]}"
        sm.get_screen("Graph").ids.Session6.text = f"Session 6: {Dates[5]}"
        sm.get_screen("Graph").ids.Session7.text = f"Session 7: {Dates[6]}"
        sm.get_screen("Graph").ids.Session8.text = f"Session 8: {Dates[7]}"
        sm.get_screen("Graph").ids.Session9.text = f"Session 9: {Dates[8]}"
        sm.get_screen("Graph").ids.Session10.text = f"Session 10: {Dates[9]}"

        CloseDatabase(conn)

    def PlotLearnt(self):
        conn, c = OpenDatabase()

        if self.ids.spinner_id.text == "Flashcard Set":
            self.ids.spinner_id.text = "No set was selected"
            Clock.schedule_once(self.LoadError, 2)
            CloseDatabase(conn)
            return False

        plt.clf()
        sm.get_screen("Graph").ids.box.clear_widgets() 
        sm.get_screen("Graph").ids.box.add_widget(FigureCanvasKivyAgg(plt.gcf()))

        sm.current = "Graph"

        c.execute(f"SELECT SetID FROM FlashcardSet WHERE SetName = '{self.ids.spinner_id.text}' \
                   AND UserID = '{UserID}'")
        SetId = c.fetchone()[0]
        c.execute(f"SELECT ProgressID FROM MainProgress WHERE SetID = '{SetId}'")
        P_ID = c.fetchone()[0]

        c.execute(f"SELECT ProgressL FROM ProgressLearnt WHERE ProgressID = '{P_ID}' ORDER BY LearntID ASC")
        Learnt = c.fetchall()

        c.execute(f"SELECT LearntDate FROM ProgressLearnt WHERE ProgressID = '{P_ID}' ORDER BY LearntID ASC")
        Times = c.fetchall()
        Dates = []
        for Time in range(len(Times)):
            Dates.append(datetime.datetime.fromtimestamp(int(f"{Times[Time][0]}")).strftime('%d-%m-%Y %H:%M:%S'))

        x = [1,2,3,4,5,6,7,8,9,10]
        y = []

        for Card in range(len(Learnt)):
            y.append(Learnt[Card][0])

        c.execute(f"SELECT MIN(ProgressL) FROM ProgressLearnt WHERE ProgressID = '{P_ID}'")
        Min = c.fetchone()[0] 
        c.execute(f"SELECT MAX(ProgressL) FROM ProgressLearnt WHERE ProgressID = '{P_ID}'")
        Max = c.fetchone()[0]
        c.execute(f"SELECT AVG(ProgressL) FROM ProgressLearnt WHERE ProgressID = '{P_ID}'")
        Avg = c.fetchone()[0]
        
        while len(y) != 10:
            y.append(0)

        while len(Dates) != 10:
            Dates.append("None")

        plt.plot(x,y)
        plt.ylabel("Percentage Learnt")
        plt.xlabel("Sessions")
        plt.title("Percentage of flashcards learnt in the set")

        sm.get_screen("Graph").ids.Highest.text = f"The highest percentage is {Max}%"
        sm.get_screen("Graph").ids.Lowest.text = f"The lowest percentage is {Min}%"
        sm.get_screen("Graph").ids.Average.text = f"The average percentage is {Avg}%"

        sm.get_screen("Graph").ids.Session1.text = f"Session 1: {Dates[0]}"
        sm.get_screen("Graph").ids.Session2.text = f"Session 2: {Dates[1]}"
        sm.get_screen("Graph").ids.Session3.text = f"Session 3: {Dates[2]}"
        sm.get_screen("Graph").ids.Session4.text = f"Session 4: {Dates[3]}"
        sm.get_screen("Graph").ids.Session5.text = f"Session 5: {Dates[4]}"
        sm.get_screen("Graph").ids.Session6.text = f"Session 6: {Dates[5]}"
        sm.get_screen("Graph").ids.Session7.text = f"Session 7: {Dates[6]}"
        sm.get_screen("Graph").ids.Session8.text = f"Session 8: {Dates[7]}"
        sm.get_screen("Graph").ids.Session9.text = f"Session 9: {Dates[8]}"
        sm.get_screen("Graph").ids.Session10.text = f"Session 10: {Dates[9]}"
        CloseDatabase(conn)
    
    def LoadError(self, dt):
        self.ids.spinner_id.text = "Flashcard Set"

    def searcherror(dt):
        sm.get_screen("Progress").ids.searchbar.text = ""
class GraphPage(Screen):
    pass
class Edit(Screen):
    def on_pre_enter(self, *args):
        self.ids.topbar.ids.searchbar.text = ""
        self.ids.topbar.ids.spinner_id.text = "Select"
        return super().on_pre_enter(*args)

    def Previous(self):
        global Index, SideCard

        conn, c = OpenDatabase()

        Index -= 1
        if Index < 0:
            Index = len(Flashcards) - 1

        c.execute(f"SELECT Title FROM Flashcard WHERE FlashID = '{Flashcards[Index][0]}'")
        Title = c.fetchone()[0]
        self.ids.Title.text = Title

        c.execute(f"SELECT FrontCard FROM Flashcard WHERE FlashID = '{Flashcards[Index][0]}'")
        FrontCard = c.fetchone()[0]
        self.ids.Notes.text = FrontCard

        c.execute(f"SELECT Format FROM Flashcard WHERE FlashID = '{Flashcards[Index][0]}'")
        Format = c.fetchone()[0]
        if Format == 1:
            self.ids.Flip.disabled = True
        else:
            self.ids.Flip.disabled = False

        c.execute(f"SELECT Difficulty FROM Flashcard WHERE FlashID = {Flashcards[Index][0]}")
        Difficulty = c.fetchone()[0]
        self.ids.ChangeDifficulty.text = f"Difficulty: {Difficulty}"

        SideCard = "Front"

        CloseDatabase(conn)

    def EditFlashcard(self):
        global Side, Set, PrevScreen

        conn, c = OpenDatabase()

        PrevScreen = "Edit"

        c.execute(f"SELECT SetID FROM FlashcardSet WHERE SetName = '{sm.get_screen("LearnSelection").ids.spinner_id.text}' \
                  and UserID = '{UserID}'")
        Set = c.fetchone()[0]

        c.execute(f"SELECT Title FROM Flashcard WHERE FlashID = '{Flashcards[Index][0]}'")
        Title = c.fetchone()[0]
        self.ids.Title.text = Title

        c.execute(f"SELECT FrontCard FROM Flashcard WHERE FlashID = '{Flashcards[Index][0]}'")
        FrontCard = c.fetchone()[0]
        self.ids.Notes.text = FrontCard

        Side = "Front"
        sm.current = "CreateNotes"

        self.Next()

        CloseDatabase(conn)

    def Delete(self):
        global Index 

        conn, c = OpenDatabase()

        c.execute(f"DELETE FROM Flashcard WHERE FlashID = '{Flashcards[Index][0]}'")
        
        c.execute(f"SELECT NumCards FROM FlashcardSet WHERE SetID = '{Flashcards[Index][1]}'")
        Num = c.fetchone()[0]
        Num -=1

        c.execute(f"UPDATE FlashcardSet SET NumCards = {Num} WHERE SetID = {Flashcards[Index][1]}")
        Index -= 1

        CloseDatabase(conn)

    def Next(self):
        global Index, SideCard, Flashcards

        conn, c = OpenDatabase()

        c.execute(f"SELECT SetID FROM FlashcardSet WHERE SetName = '{sm.get_screen("LearnSelection").ids.spinner_id.text}' \
                and UserID = '{UserID}'")
        S_ID = c.fetchone()[0]
        c.execute(f"SELECT * FROM Flashcard WHERE SetID = '{S_ID}'")
        Flashcards = c.fetchall()

        if len(Flashcards) == 0:
            sm.current = "LearnSelection"
            CloseDatabase(conn)
            return False
        elif len(Flashcards) == 1:
            self.ids.Next.disabled = True
            self.ids.Previous.disabled = True
            
        Index += 1
        if Index == len(Flashcards):
            Index = 0

        c.execute(f"SELECT Title FROM Flashcard WHERE FlashID = '{Flashcards[Index][0]}'")
        Title = c.fetchone()[0]
        self.ids.Title.text = Title

        c.execute(f"SELECT FrontCard FROM Flashcard WHERE FlashID = '{Flashcards[Index][0]}'")
        FrontCard = c.fetchone()[0]
        self.ids.Notes.text = FrontCard

        c.execute(f"SELECT Format FROM Flashcard WHERE FlashID = '{Flashcards[Index][0]}'")
        Format = c.fetchone()[0]
        if Format == 1:
            self.ids.Flip.disabled = True
        else:
            self.ids.Flip.disabled = False

        c.execute(f"SELECT Difficulty FROM Flashcard WHERE FlashID = {Flashcards[Index][0]}")
        Difficulty = c.fetchone()[0]
        self.ids.ChangeDifficulty.text = f"Difficulty: {Difficulty}"

        SideCard = "Front"

        CloseDatabase(conn)

    def FlipCard(self):
        global SideCard
        
        conn, c = OpenDatabase()

        SideCard = Flip(SideCard)
        if SideCard == "Back":
            c.execute(f"SELECT BackCard FROM Flashcard WHERE FlashID = '{Flashcards[Index][0]}'")
            BackCard = c.fetchone()[0]
            self.ids.Notes.text = BackCard
        else:
            c.execute(f"SELECT FrontCard FROM Flashcard WHERE FlashID = '{Flashcards[Index][0]}'")
            FrontCard = c.fetchone()[0]
            self.ids.Notes.text = FrontCard

        CloseDatabase(conn)

    def searcherror(dt):
        sm.get_screen("Edit").ids.searchbar.text = ""

class InputAndButton(BoxLayout):
    def addset(self):
        conn, c = OpenDatabase()

        if self.ids.Title.text == "":
            sm.get_screen("CreateSelection").ids.Error.text = "No Title was entered"
            Clock.schedule_once(self.displayerror, 2)
            CloseDatabase(conn)
            return False
        c.execute(f"SELECT SetName FROM FlashcardSet WHERE UserID = '{UserID}'")
        Titles = c.fetchall()
        for name in range(len(Titles)):
            if self.ids.Title.text == Titles[name][0]:
                sm.get_screen("CreateSelection").ids.Error.text = "This set already exists"
                Clock.schedule_once(self.displayerror, 2)
                CloseDatabase(conn)
                return False
            
        c.execute(f"INSERT INTO FlashcardSet (SetName, NumCards, UserID, Premade) VALUES ('{self.ids.Title.text}', 0, {UserID}, 0)")
        self.ids.Title.text = ""
        
        CloseDatabase(conn)

    def displayerror(self, dt):
        sm.get_screen("CreateSelection").ids.Error.text = ""

class Graph(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.add_widget(FigureCanvasKivyAgg(plt.gcf()))

    def Update(self):
        plt.clf()
        self.clear_widgets() 
        self.add_widget(FigureCanvasKivyAgg(plt.gcf()))  


class MainApp(MDApp):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.other_class = LearnNotes()

    def build(self):
        global sm
        self.theme_cls.theme_style = "Light"
        self.theme_cls.primary_palette = "Teal"

        conn, c = OpenDatabase()

        c.execute("""CREATE TABLE if not exists UserAccount(
            UserID INTEGER PRIMARY KEY AUTOINCREMENT,
            Username TEXT,
            Password TEXT,
            Email TEXT)
        """)

        c.execute("""CREATE TABLE if not exists Flashcard(
            FlashID INTEGER PRIMARY KEY AUTOINCREMENT,
            SetID INTEGER,
            Title TEXT,
            FrontCard TEXT,
            BackCard TEXT,
            Format BOOLEAN,
            Learnt BOOLEAN,
            Flagged BOOLEAN,
            Viewed BOOLEAN,
            Difficulty TEXT)
        """)

        c.execute("""CREATE TABLE if not exists FlashcardSet(
            SetID INTEGER PRIMARY KEY AUTOINCREMENT,
            SetName TEXT,
            NumCards INTEGER,
            UserID INTEGER,
            Premade BOOLEAN,
            LastOpened INTEGER)
        """)

        c.execute("""CREATE TABLE if not exists MainProgress(
            ProgressID INTEGER PRIMARY KEY AUTOINCREMENT,
            SetID INTEGER)
        """)

        c.execute("""CREATE TABLE if not exists ProgressViewed(
            ViewedID INTEGER PRIMARY KEY AUTOINCREMENT,
            ProgressID INTEGER,
            ProgressV REAL,
            ViewedDate INTEGER)
        """)

        c.execute("""CREATE TABLE if not exists ProgressLearnt(
            LearntID INTEGER PRIMARY KEY AUTOINCREMENT,
            ProgressID INTEGER,
            ProgressL REAL,
            LearntDate INTEGER)
        """)

        c.execute("""CREATE TABLE if not exists ProgressFlagged(
            FlaggedID INTEGER PRIMARY KEY AUTOINCREMENT,
            ProgressID INTEGER,
            ProgressF REAL,
            FlaggedDate INTEGER)
        """)

        CloseDatabase(conn)
        
        from kivy.resources import resource_find
        filename = "main.kv"
        filename = resource_find(filename)
        if filename in Builder.files:
            Builder.unload_file(filename)
        Builder.load_file("main.kv")

        sm = ScreenManager()
        sm.add_widget(Login(name = "Login"))
        sm.add_widget(SignUp(name = "SignUp"))
        sm.add_widget(Account(name = "Account"))
        sm.add_widget(CreateNotes(name = "CreateNotes"))
        sm.add_widget(CreateSelection(name = "CreateSelection"))
        sm.add_widget(Help(name = "Help"))
        sm.add_widget(Home(name = "Home"))
        sm.add_widget(LearnNotes(name = "LearnNotes"))
        sm.add_widget(LearnSelection(name = "LearnSelection"))
        sm.add_widget(Progress(name = "Progress"))
        sm.add_widget(GraphPage(name = "Graph"))
        sm.add_widget(Edit(name= "Edit"))
        return sm
    
    def Confirm(self, MyPopup):
        conn, c = OpenDatabase()

        if MyPopup.ids.Yes.disabled == True:
            self.root.get_screen(f"{sm.current}").Delete()
            if sm.current == "LearnSelection":
                self.addvalues("LearnSelection")
            else:
                self.root.get_screen(f"{sm.current}").Next()
            MyPopup.dismiss()
        elif MyPopup.ids.No.disabled == True:
            MyPopup.dismiss()

    def Select(self, MyPopup):
        conn, c = OpenDatabase()

        c.execute(f"SELECT Difficulty FROM Flashcard WHERE FlashID = {Flashcards[Index][0]}")
        Difficulty = c.fetchone()[0]


        if MyPopup.ids.Easy.disabled == True and Difficulty != "Easy":
            c.execute(f"UPDATE Flashcard SET Difficulty = 'Easy' WHERE FlashID = '{Flashcards[Index][0]}'")
            MyPopup.dismiss()
            self.root.get_screen("Edit").ids.ChangeDifficulty.text = f"Difficulty: Easy"
        elif MyPopup.ids.Medium.disabled == True and Difficulty != "Medium":
            c.execute(f"UPDATE Flashcard SET Difficulty = 'Medium' WHERE FlashID = '{Flashcards[Index][0]}'")
            MyPopup.dismiss()
            self.root.get_screen("Edit").ids.ChangeDifficulty.text = f"Difficulty: Medium"
        elif MyPopup.ids.Hard.disabled == True and Difficulty != "Hard":
            c.execute(f"UPDATE Flashcard SET Difficulty = 'Hard' WHERE FlashID = '{Flashcards[Index][0]}'")
            MyPopup.dismiss()
            self.root.get_screen("Edit").ids.ChangeDifficulty.text = f"Difficulty: Hard"
        else:
            MyPopup.ids.ErrorMessage.text = "The flashcard is already set to that difficulty"
            Clock.schedule_once(lambda dt: self.Error(MyPopup, dt), 2)

        CloseDatabase(conn)


    def spinner_clicked(self, value):
        sm.get_screen(f"{sm.current}").ids.topbar.ids.spinner_id.text = value
    
    def displayerror(self, Text, dt):
        sm.get_screen(f"{sm.current}").ids.topbar.ids.searchbar.text = Text

    def Error(self, MyPopUp, dt):
        MyPopUp.ids.ErrorMessage.text = ""

    def search(self):
        conn, c = OpenDatabase()

        if sm.get_screen(f"{sm.current}").ids.topbar.ids.spinner_id.text == "Select":
            Text = sm.get_screen(f"{sm.current}").ids.topbar.ids.searchbar.text
            sm.get_screen(f"{sm.current}").ids.topbar.ids.searchbar.text = "Choose an option from the dropdown menu"
            Clock.schedule_once(lambda dt: self.displayerror(Text, dt), 2)
            return False
        elif sm.get_screen(f"{sm.current}").ids.topbar.ids.spinner_id.text == "Learn":
            Action = "Learn"
        elif sm.get_screen(f"{sm.current}").ids.topbar.ids.spinner_id.text == "Add":
            Action = "Add"
        elif sm.get_screen(f"{sm.current}").ids.topbar.ids.spinner_id.text == "Edit":
            Action = "Edit"

        c.execute(f"SELECT NumCards FROM FlashcardSet WHERE UserID = '{UserID}' \
                  AND SetName = '{sm.get_screen(f"{sm.current}").ids.topbar.ids.searchbar.text}'")
        NumCards = c.fetchone()
        if NumCards == None or NumCards[0] == 0:
            Text = sm.get_screen(f"{sm.current}").ids.topbar.ids.searchbar.text
            sm.get_screen(f"{sm.current}").ids.topbar.ids.searchbar.text = "This set does not exist or does not contain any cards"
            Clock.schedule_once(lambda dt: self.displayerror(Text, dt), 2)
            CloseDatabase(conn)
            return False
        
        if Action == "Learn":       
            sm.get_screen("LearnSelection").ids.spinner_id.text = sm.get_screen(f"{sm.current}").ids.topbar.ids.searchbar.text  
            LearnNotes.loadnotes(self,"Learn")
            sm.current = "LearnNotes"
        elif Action == "Edit":
            sm.get_screen("LearnSelection").ids.spinner_id.text = sm.get_screen(f"{sm.current}").ids.topbar.ids.searchbar.text
            LearnNotes.loadnotes(self, "Edit")
            sm.current = "Edit"
        elif Action == "Add":
            sm.get_screen("CreateSelection").ids.spinner_id.text = sm.get_screen(f"{sm.current}").ids.topbar.ids.searchbar.text

            sm.current = "CreateSelection"


        CloseDatabase(conn)
      
    def CheckDetails(self, MyPopup):
        global Code

        conn, c = OpenDatabase()
        
        c.execute(f"SELECT UserID FROM UserAccount WHERE Email = '{MyPopup.ids.Email.text}' \
            AND Username = '{MyPopup.ids.User.text}'")
        User = c.fetchone()
        if User == None:
            MyPopup.ids.ErrorMessage.text = "Details enetered are incorrect"
            Clock.schedule_once(lambda dt: self.Error(MyPopup, dt), 2)
            CloseDatabase(conn)
            return False
        else:
            MyPopup.ids.ErrorMessage.text = f"Code sent to {MyPopup.ids.Email.text}"
            Clock.schedule_once(lambda dt: self.Error(MyPopup, dt), 2)
            MyPopup.ids.Code.disabled = False
            MyPopup.ids.CodeButton.disabled = False

            email_sender = "appflashcard46@gmail.com"
            email_password = "fxsh sgkh ywcp phko"
            email_receiver = f"{MyPopup.ids.Email.text}"

            n = 6
            Code = ''.join(["{}".format(random.randint(0,9)) for num in range(0,n)])

            subject = "Reset Password Code"
            body = f"The code to reset your password is {Code}"

            em = EmailMessage()
            em['From'] = email_sender
            em['To'] = email_receiver
            em['Subject'] = subject
            em.set_content(body)

            context = ssl.create_default_context()

            with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
                smtp.login(email_sender, email_password)
                smtp.sendmail(email_sender, email_receiver, em.as_string())

        CloseDatabase(conn)

    def CheckCode(self, MyPopup):
        if str(Code) == MyPopup.ids.Code.text:
            MyPopup.ids.Pwd.disabled = False
            MyPopup.ids.Submit.disabled = False
            MyPopup.ids.ErrorMessage.text = "Code typed was correct"
            Clock.schedule_once(lambda dt: self.Error(MyPopup, dt), 2)
        else:
            MyPopup.ids.ErrorMessage.text = "Code typed was incorrect"
            MyPopup.ids.Code.text = ""
            Clock.schedule_once(lambda dt: self.Error(MyPopup, dt), 2)

    def searchbarclear(self):
        sm.get_screen(f"{sm.current}").ids.topbar.ids.searchbar.text = ""


    def ChangePassword(self, MyPopup):
        conn, c = OpenDatabase()

        if ValidPassword(MyPopup.ids.Pwd.text):
            c.execute(f"UPDATE UserAccount SET Password = '{HashPassword(MyPopup.ids.Pwd.text)}' WHERE Username = '{MyPopup.ids.User.text}'")
            MyPopup.ids.ErrorMessage.text = "Password Updated"
            Clock.schedule_once(lambda dt: self.Error(MyPopup, dt), 2)
        else:
            MyPopup.ids.ErrorMessage.text = "Password typed is invalid"
            Clock.schedule_once(lambda dt: self.Error(MyPopup, dt), 2)

        CloseDatabase(conn)
                
    def addvalues(self, Condition):
        conn, c = OpenDatabase()

        if Condition == "Pre-Made":
            sm.get_screen(f"{sm.current}").ids.NavBar.ids.PreMadeButton.disabled = True
            sm.get_screen(f"{sm.current}").ids.Edit.disabled = True
            sm.get_screen(f"{sm.current}").ids.Delete.disabled = True
            sm.get_screen(f"{sm.current}").ids.NavBar.ids.LearnFlashcard.disabled = False
            sm.get_screen(f"{sm.current}").ids.spinner_id.text = "Flashcard Set"
            sm.get_screen(f"{sm.current}").ids.click_label.text = "Pick the flashcard set that you would like to learn below"

            self.root.get_screen("LearnSelection").ids.spinner_id.values = []
            c.execute(f"SELECT SetName FROM FlashcardSet WHERE UserID = {UserID} AND Premade = 1")
            Sets = c.fetchall()
            Sets = MergeSort(Sets)
            for row in range(len(Sets)):
                self.root.get_screen("LearnSelection").ids.spinner_id.values.append(Sets[row][0])

        elif Condition == "LearnSelection":
            sm.get_screen(f"{sm.current}").ids.NavBar.ids.PreMadeButton.disabled = False
            sm.get_screen(f"{sm.current}").ids.Edit.disabled = False
            sm.get_screen(f"{sm.current}").ids.Delete.disabled = False
            sm.get_screen(f"{sm.current}").ids.NavBar.ids.LearnFlashcard.disabled = True
            sm.get_screen(f"{sm.current}").ids.spinner_id.text = "Flashcard Set"
            sm.get_screen(f"{sm.current}").ids.click_label.text = "Pick the flashcard set that you would like to learn below"

            self.root.get_screen("LearnSelection").ids.spinner_id.values = []
            c.execute(f"SELECT SetName FROM FlashcardSet WHERE UserID = {UserID} AND Premade = 0")
            Sets = c.fetchall()
            Sets = MergeSort(Sets)
            for row in range(len(Sets)):
                self.root.get_screen("LearnSelection").ids.spinner_id.values.append(Sets[row][0])
        
        else:
            self.root.get_screen("CreateSelection").ids.spinner_id.values = []
            c.execute(f"SELECT SetName FROM FlashcardSet WHERE UserID = {UserID} AND Premade = 0")
            Sets = c.fetchall()
            Sets = MergeSort(Sets)
            for row in range(len(Sets)):
                self.root.get_screen("CreateSelection").ids.spinner_id.values.append(Sets[row][0])

            CloseDatabase(conn)
    
    def GraphError(self, dt):
        self.root.get_screen("Graph").ids.Save.text = "Save Graph"
        

    def SaveGraph(self):
        name = self.root.get_screen("Graph").ids.name.text
        if name:
            plt.savefig(f"{name}.jpg")
            self.root.get_screen("Graph").ids.name.text = ""
        else:
            self.root.get_screen("Graph").ids.Save.text = "Name Required"
            Clock.schedule_once(lambda dt: self.GraphError(dt), 2)
                           
if __name__ == "__main__":
    MainApp().run()
    