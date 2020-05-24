from agent import ap

class console():
    def __init__(self):
        self.agent = ap()
        self.islogin = False
        self.quit = False
    
    def login(self):
        """call the login function of ap and control the login status"""
        username,password = self.agent.input_credential()
        self.islogin = self.agent.login(username,password)
        
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
