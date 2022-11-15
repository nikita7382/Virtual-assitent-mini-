import speech_recognition as sr
import pyttsx3
import datetime
import pywhatkit
import wikipedia
import bs4 as bs
import webbrowser
import smtplib
import pyjokes
import requests
import json
import winsound


email={'gaurav':'yourfreindemail@email.com'}

engine=pyttsx3.init()
voices=engine.getProperty('voices')
engine.setProperty('voice',voices[1].id)


def speak(audio):
    engine.say(audio)
    engine.runAndWait()

def sendemail(to,content):
    server=smtplib.SMTP('smtp.gmail.com',587)
    server.ehlo()
    server.starttls()
    server.login('dummy@email.com','hruxlxpvowpsntcv')
    server.sendmail('dummy@email.com',to,content)
    server.close()


def takecommand():
    
    with sr.Microphone() as source:
        print('listening....')
        listener=sr.Recognizer()
        listener.pause_threshold=1
        audio=listener.listen(source)

    try:
        print('recogninzing....')
        command=listener.recognize_google(audio)
        print(command)
        command=command.lower()
        if 'mini' in command:
            command=command.replace('mini','')
       

    except Exception:
        print(Exception)
        speak('Sorry! Will you repeat that again')
        return "None"
    return command



def runcommand():
    command=takecommand()
    print(command)
    if 'play' in command:
        play=command.replace('play','')
        pywhatkit.playonyt(play)
    
    elif 'search'in command:
        searchword=command.split('for')[-1].strip()
        print(searchword)
        try:
            result=wikipedia.summary(searchword,sentences=2)
            speak("According to wikipedia.."+result)

        except Exception:
            print(Exception)
            speak("Sorry i cannot find any matching results")
       
    elif 'time'in command:
        time=datetime.datetime.now().strftime('%I: %M %p')
        speak(f'The current Time is {time}')
        

    elif 'open' in command:
        browser=command.split('open')[-1].strip()
        print(browser)
        webbrowser.open(browser+'.com')
    
    elif 'send email' in command:
        to=command.split('to')[-1].strip()
        print(to)
        emailadd=email[to]
        print(emailadd)
        speak("What is the message?")
        content=takecommand()
        try:
            sendemail(emailadd,content)
            speak('Your email has been sent')
        except Exception:
            print(Exception)
            speak('Sorry! email cannot be sent due to some error.Please do it manually')
    

    elif 'joke' in command:
        joke=pyjokes.get_joke()
        print(joke)
        speak(joke)

    elif 'weather' in command:
        speak('which city?')
        city=takecommand()
        print(city)
        appid='7dffc8456d5bc572f1bb7f1ea69d83e8'
        URL='https://api.openweathermap.org/data/2.5/weather'
        info={'q':city,'appid':appid,'units':'metric'}
        r=requests.get(url=URL,params=info).json()
        temp=r['main']['temp']
        print(temp)
        weather=r['weather'][0]['description']
        print(weather)
        speak(f'weather of the {city} is {weather} and temperature is {temp} degree celcius')
        
    elif 'alarm' in command:
        speak("Please tell me the time.. example 5:20 am")
        time=takecommand().upper()
        print(time)
        
        current_time=datetime.datetime.now().strftime('%I:%M %p')
        while True:
            if current_time==time:
                print("alarm is running")
                winsound.PlaySound('abc',winsound.SND_LOOP)
 
            elif current_time>time:
                break
            
            else:
                speak('sorry i didnot get it')


        # print(formated_time)


        
def greeting():
    '''This function greet the user as soon as the program starts'''

    time=int(datetime.datetime.now().hour)
    if time>=0 and time<12:
        speak('Good Morning')
    elif time>=12 and time<18:
        speak('Good Afternoon!')
    else:
        speak('Good Evening!')

    speak('I am mini,How can i help you?')


if __name__=='__main__':
    greeting()
    while True:
        runcommand()
    
    
