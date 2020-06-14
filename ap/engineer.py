

def main():
    from QRCode import QR_reader
    Q= QR_reader()
    option="0"
    while(option!='2'):
        print("choose from the following options:\n1.scan QR code\n2.quit")
        option =input()
        if(option == '1'):
            try:
                Q.scan_QR()
            except:
                print("wrong input path ot invalid QR code")    
        if(option!='1' and option!='2'):
            print('invalid input ')        

if __name__ == "__main__":
    # execute only if run as a script
    main()