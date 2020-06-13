import qrcode
import time

def create_qr_code(string):
    """
    QR code creation function 
    
    :param string: the encode data
    :return:
    """
    qr = qrcode.QRCode(
        version=1, 
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=2,
    ) 

    data = string 
    qr.add_data(data)
    qr.make(fit=True)
    img = qr.make_image(fill_color='black', back_color='white')

    FileName = 'Images/qrcode' + time.strftime('_%Y_%m_%d_%H_%M_%S',
                    time.localtime(time.time())) + ".png"
    img.save(FileName) 
    return FileName
