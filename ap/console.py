from agent import ap

class console():
    def __init__(self):
        self.agent = ap()
        self.islogin = False
        self.quit = False
    
    def login(self):
        """call the login function of ap and control the login status"""
        input_valid = False
        while input_valid is False:
            user_input = input("\n\nEnter '1' to login with username and password\nEnter '2' to login using facial recognition\n")
            if (user_input == '1') or (user_input == '2'):
                input_valid = True
            else:
                print("you must enter '1' or '2'. Try again!")
        if user_input == 1:
            username, password = self.agent.input_credential()
            self.islogin = self.agent.login(username, password)
        else:
            p_data = self.agent.input_image_credential()
            if p_data is not None:
                self.islogin = self.agent.login_face(p_data)
        
    def menu(self):
        """print the menu for the user"""
        print("1.unlock a car\n2.return a car\n3.quit")    
        user_input = input()
        self.read_input(user_input)
    
    def read_input(self,input):
        """read the user input of the menu, and call the functions in ap"""
        if input == '1':
            self.agent.find_booked_car()
        elif input == '2':
            self.agent.find_inprogress()
        elif input == '3':
            print("see u")
            self.quit = True
            
            
    def start_console(self):
        """start console and make it running"""
        while True:
            if self.islogin:        
                self.menu()
            else:
                self.login() 
            if self.quit:
                break      
