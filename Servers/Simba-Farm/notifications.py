import requests
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
import os
import base64

smtp_server = 'smtp.gmail.com'
smtp_port = 587  # SSL: 465, TLS/STARTTLS: 587
sender_email = 'machariaandrew1428@gmail.com'  # Replace with your Gmail address
password = 'carg yxei depl ossa'

class notify:
    def __init__(self):
        self.base_url = 'https://sms.textsms.co.ke/api/services/sendsms'
        self.payload = {
            "apikey":"7c3974460133560c59c413c701744c85",
            "partnerID":"9064",
            "message":"this is a test message",
            "shortcode":"TextSMS",
            "mobile":"254795359098"
        }

    def send_sms(self, product_notification):
        self.state = False
        for x in product_notification:
            self.payload["message"] = """
                    Dear %s:
                    An Order has been placed for:
                    Item Name: %s
                    Item No: %s
                    Kindy arrange dispatch within the next two working days after which funds
                    will be transfered to your account.
                    Best wishes Hustle Point
                    Thank You"""%(x["SellerName"], x["ProductName"], x["ProductMagnitude"])
            self.payload["mobile"] = x["sellersPhone"]
            print(str(self.payload["mobile"])[len(str(self.payload["mobile"]))-9:])
            new_phone = str(self.payload["mobile"])[len(str(self.payload["mobile"]))-9:]
            self.payload["mobile"] = "254%s"%(new_phone)
            print(self.payload["mobile"])
            # try:
            #     self.response = requests.post(self.base_url, data=self.payload)
            #     if self.response.status_code == 200:
            #         self.state = True
            #         print("Message Sent Successfully")
            #     else:
            #         self.state = False
            #         print("Error Sending Message ....")
            # except:
            #     print("Request failed")
        return self.state
    
    def send_email(self, recipient_email, email_subject, email_body):
        try:
            message = MIMEMultipart()
            message['From'] = sender_email
            message['To'] = recipient_email
            message['Subject'] = email_subject
            image_path = "simba_app.png"
            with open(image_path, 'rb') as img_file:
                img_data = img_file.read()
                img_data = MIMEImage(img_data)
            body = """
                    <!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Document</title>
    <style>
        body{
            /* background-image: linear-gradient(130deg, purple 40%, white); */
            background-color: rgb(213, 255, 255);
            margin: 0;
            padding: 0;
            height: 100vw;
            height: 100vh;
        }

        .container{
            width: 100%;
            height: 100%;
            border: 1.5px solid gray;
            border-radius: 10px;
        }

        .container header{
            width: 100%;
            border-bottom: 2px solid beige;
        }

        header img{
            height: 70px;
            margin-left: 2%;
        }

        header p{
            margin: 0;
            font-weight: 1000;
            justify-self: center;
            font-size: 2vw;
        }

        header span{
            margin: 0;
            font-weight: 600;
            justify-self: center;
            font-size: 12px;
        }

        .message{
            width: 100%;
            display: flex;
            flex-direction: column;
            align-items: center;
        }

        .message p{
            font-size: 1vw;
            width: 80%;
        }
    </style>
</head>
<body>
    <div class="container">
        <header>
            <img src="cid:image1" alt="">
            <p>SIMBA FARM</p>
            <span>
                <b>Email:</b> simba890@gmail.com
                <br>
                <b>Phone:</b> 0712345678
            </span>
        </header>
        <div class="message">
            <p>
                Dear Sir,<br>
                Lorem ipsum, dolor sit amet consectetur adipisicing elit. Facere dolores, mollitia quaerat iure commodi eius praesentium possimus aliquam saepe maiores corporis natus quas sint adipisci! Repellat eveniet maiores libero exercitationem.
                Lorem ipsum dolor sit, amet consectetur adipisicing elit. Cum facere cumque ex quo eaque officiis dolores, molestiae possimus nam deserunt, earum quas voluptatum tenetur dignissimos porro sunt nulla necessitatibus ut?
                Lorem ipsum dolor sit amet consectetur adipisicing elit. Nam qui, et autem animi alias commodi laboriosam minus expedita, voluptas quas tempore atque provident dolorem deserunt porro harum, odio sunt! Vero?Lorem ipsum, dolor sit amet consectetur adipisicing elit. Commodi consequuntur eum optio porro nemo atque rerum iusto libero dolore aut eius perspiciatis illum aperiam eveniet molestiae nobis, veniam voluptatibus pariatur?
                Lorem ipsum dolor sit amet, consectetur adipisicing elit. Blanditiis quidem error doloremque repellendus tempora aliquid at minima. Et, dolor. Voluptatem ea ducimus iusto ipsa aperiam vel ipsum veritatis excepturi esse.<br>
                Thank you
            </p>
        </div>
    </div>
</body>
</html>
                    """
            message.attach(MIMEText(body, 'html'))
            img_data.add_header('Content-ID', '<image1>')
            message.attach(img_data)
            server = smtplib.SMTP(smtp_server, smtp_port)
            server.starttls()
            server.login(sender_email, password)
            server.send_message(message)
            print("Email sent")
            return True
        except:
            print("Email NOT sent")
            return False


x = notify()
x.send_email("machariaandrew1428@gmail.com", "Test", "Test message .....")