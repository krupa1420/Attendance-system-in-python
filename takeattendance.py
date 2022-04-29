import tkinter as tk
from tkinter import *
import os, cv2
import shutil
import _csv
import numpy as np
from PIL import ImageTk, Image
import pandas as pd
import datetime
import time
import tkinter.ttk as tkk
import tkinter.font as font

haarcasecade_path = "E:\\6 SEM\\3CP08 - DE\\Project\\haarcascade_frontalface_default.xml"
trainimagelabel_path = (
    "E:\\6 SEM\\3CP08 - DE\\Project\\face_enc.yml"
)
trainimage_path = "E:\\6 SEM\\3CP08 - DE\\Project\\TrainingImage"
studentdetail_path = (
    "E:\\6 SEM\\3CP08 - DE\\Project\\StudentDetails\\studentdetails.csv"
)
attendance_path = "E:\\6 SEM\\3CP08 - DE\\Project\\Attendance"

# for choose subject and fill attendance
def subjectChoose(text_to_speech):
    def FillAttendance():
        sub = tx.get()
        now = time.time()
        future = now + 50
        #print(now)
        #print(future)
        if sub == "":
            t = "Please enter the subject name!!!"
            text_to_speech(t)
        else:
            try:
                recognizer = cv2.face.LBPHFaceRecognizer_create()

                while True:
                    recognizer.read(trainimagelabel_path)
                    cam = cv2.VideoCapture(0)
                    ___, im = cam.read()
                    col_names = ["Enrollment", "Name"]
                    attendance = pd.DataFrame(columns=col_names)
                    facecasCade = cv2.CascadeClassifier(haarcasecade_path)
                    df = pd.read_csv(studentdetail_path)
                    gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
                    faces = facecasCade.detectMultiScale(gray, 1.3, 5)
                    for (x, y, w, h) in faces:
                        print("in..")
                        global Id
                        Id, pred = recognizer.predict(gray[y:y + h, x:x + w])
                        conf = int(100*(1-pred/300))
                        if conf > 50:
                            print(pred)
                            global Subject
                            global aa
                            global date
                            global timeStamp
                            aa = df.loc[df["Enrollment"] == Id]["Name"].values
                            global tt
                            tt = str(Id) + "-" + aa
                            print(tt)
                            Subject = tx.get()
                            ts = time.time()
                            date = datetime.datetime.fromtimestamp(ts).strftime(
                                "%Y-%m-%d"
                            )
                            timeStamp = datetime.datetime.fromtimestamp(ts).strftime(
                                "%H:%M:%S"
                            )
                            attendance.loc[len(attendance)] = [
                                Id,
                                aa,
                            ]
                            attendance[date] = 1
                            print(attendance)
                            fm = " Face found for attendance is" + tt
                            text_to_speech(fm)
                            exists = os.path.isfile("Attendance/" + Subject + ".csv")
                            if exists:
                                f = open("Attendance/" + Subject + ".csv", "a+")
                                attendance.to_csv(f, index=False)
                                f.close()
                            else:

                                f = open("Attendance/" + Subject + ".csv", "w")
                                attendance.to_csv(f, index=False)
                                f.close()

                            cv2.rectangle(im, (x, y), (x + w, y + h), (255, 0, 0), 2)
                            cv2.putText(
                                im, str(tt), (x + h, y), font, 1, (255, 255, 0,), 4
                            )
                            print("in....ttt")

                        else:
                            Id = "Unknown"
                            tt = str(Id)
                            print(tt)
                            cv2.rectangle(im, (x, y), (x + w, y + h), (255, 0, 0), 2)
                            cv2.putText(
                                im, str(tt), (x + h, y), font, 1, (0, 25, 255), 4
                            )

                    attendance = attendance.drop_duplicates(
                        ["Enrollment"], keep="first"
                    )
                    cv2.imshow("Filling Attendance...", im)
                    key = cv2.waitKey(30) & 0xFF
                    if key == 27:
                        break


                m = "Attendance Filled Successfully of " + Subject
                Notifica.configure(
                    text=m,
                    bg="black",
                    fg="yellow",
                    width=33,
                    relief=RIDGE,
                    bd=5,
                    font=("times", 15, "bold"),
                )
                text_to_speech(m)

                Notifica.place(x=20, y=250)

                cam.release()
                cv2.destroyAllWindows()


            except:
                cam.release()
                cv2.destroyAllWindows()
                #f = "No Face found for attendance"
                #text_to_speech(f)

    ###windo is frame for subject chooser
    subject = Tk()
    # windo.iconbitmap("AMS.ico")
    subject.title("Subject...")
    subject.geometry("580x320")
    subject.resizable(0, 0)
    subject.configure(background="black")
    # subject_logo = Image.open("UI_Image/0004.png")
    # subject_logo = subject_logo.resize((50, 47), Image.ANTIALIAS)
    # subject_logo1 = ImageTk.PhotoImage(subject_logo)
    titl = tk.Label(subject, bg="black", relief=RIDGE, bd=10, font=("arial", 30))
    titl.pack(fill=X)
    # l1 = tk.Label(subject, image=subject_logo1, bg="black",)
    # l1.place(x=100, y=10)
    titl = tk.Label(
        subject,
        text="Enter the Subject Name",
        bg="black",
        fg="green",
        font=("arial", 25),
    )
    titl.place(x=160, y=12)
    Notifica = tk.Label(
        subject,
        text="Attendance filled Successfully",
        bg="yellow",
        fg="black",
        width=33,
        height=2,
        font=("times", 15, "bold"),
    )

    def Attf():
        sub = tx.get()
        if sub == "":
            t = "Please enter the subject name!!!"
            text_to_speech(t)
        else:
            os.startfile(
                f"E:\\6 SEM\\3CP08 - DE\\Project\\Attendance\\{sub}"
            )

    sub = tk.Label(
        subject,
        text="Enter Subject",
        width=10,
        height=2,
        bg="black",
        fg="yellow",
        bd=5,
        relief=RIDGE,
        font=("times new roman", 15),
    )
    sub.place(x=50, y=100)

    tx = tk.Entry(
        subject,
        width=15,
        bd=5,
        bg="black",
        fg="yellow",
        relief=RIDGE,
        font=("times", 30, "bold"),
    )
    tx.place(x=190, y=100)

    fill_a = tk.Button(
        subject,
        text="Fill Attendance",
        command=FillAttendance,
        bd=7,
        font=("times new roman", 15),
        bg="black",
        fg="yellow",
        height=2,
        width=12,
        relief=RIDGE,
    )
    fill_a.place(x=195, y=170)
    subject.mainloop()
