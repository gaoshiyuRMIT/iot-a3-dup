from ap import ap

class console():
    def __init__(self):
        self.agent = ap()
        self.islogin = False
        self.quit = False
    
    def login(self):
        username,password = self.agent.input_credential()
        self.islogin = self.agent.login(username,password)
        
    def menu(self):
        print("1.unlock a car\n2.return a car\n3.quit")    
        user_input = input()
        self.read_input(user_input)
    
    def read_input(self,input):
        if input == '1':
            self.agent.find_booked_car()
        elif input == '2':
            self.agent.find_inprogress()
        elif input == '3':
            print("see u")
            self.quit = True
            
    def start_console(self):
        while True:
            if self.islogin:        
                self.menu()
            else:
                self.login() 
            if self.quit:
                break      
