

def main():
    from QRCode import QR_reader
    Q= QR_reader()
    option="0"
    while(option!='2'):
        print("choose from the following options:\n1.scan QR code\n2.quit")
        option =input()
        if(option == '1'):
            Q.scan_QR()

if __name__ == "__main__":
    # execute only if run as a script
    main()