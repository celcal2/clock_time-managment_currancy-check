from tkinter import *
import time
from datetime import date,datetime, timedelta
from requests import get
import math


LIGHT = "#FFF0F5"
PEACH = '#FFEADD'
PURPULE = "#916DB3"
FONT_NAME = "Courier"

PINK = "#e2979c"
RED = "#e7305b"
GREEN = "#9bdeac"
YELLOW = "#f7f5dd"
WORK_MIN = 25
SHORT_BREAK_MIN = 5
LONG_BREAK_MIN = 20
reps = 0
timer = None

master = Tk()
master.state('zoomed')
master.config(padx=5, pady=5, bg=LIGHT)
master.title('TimeLife by Celina')
master.iconbitmap('flower.ico')

timenow = ' '
cframe = Frame(master, width = 5, height=5, bg=LIGHT, relief=RAISED)
cframe.grid(row=0, column=0)

clock = Label(cframe, bd=3, padx=1, pady=1,
              font=(FONT_NAME, 45, "bold"), text=timenow, relief=RAISED)
clock.grid(row=0, column=0)

today = datetime.today().strftime('%d-%m-%Y')
information = f'Dzisiaj jest {today}'
date_label = Label(cframe, text=today, bd=3,
              font=(FONT_NAME, 45, "bold"), bg=LIGHT, fg=PURPULE, relief=RAISED)
date_label.grid(row=1, column=0)

def tick():
    global timenow
    newtime = time.strftime('%H: %M: %S %p')
    if newtime != timenow:
        timenow = newtime
        clock.config(text=timenow, fg=PURPULE, bg=LIGHT, font=(FONT_NAME, 45, "bold"))

    return clock.after(100,tick)

def lived_days():

    dateOfBirth = date(int(year.get()), int(month.get()), int(day.get()))
    delta = date.today() - dateOfBirth
    words = f'Przeżyłeś już {delta.days} dni'
    napis = Label(text=words, fg=PURPULE,
                  bg=PEACH)
    napis.grid(row=5, column=0)
    year.delete(0, END)
    month.delete(0,END)
    day.delete(0,END)

def close():
    master.destroy()

def checking_dayweek(number_day):
    days = ['poniedziałek', 'wtorek', 'środa', 'czwartek', 'piątek', 'sobota', 'niedziela']
    today = number_day
    day_name = days[today]
    return day_name

def checking_currency():

    if int(datetime.today().weekday()) == 6:
        data = datetime.today().date() - timedelta(days=2)
        # msg = f"Dzisiaj jest {checking_dayweek()} {datetime.today().date()}"
    # elif:
    #     dt.datetime.today().weekday() == 7:
    #     data = dt.datetime.today().date() - dt.timedelta(days=3)
    #     msg = f"Dzisiaj jest {checking_dayweek()} {dt.datetime.today().date()}"
    else:
        data = datetime.today().date() - timedelta(days=1)
        # msg = f"Dzisiaj jest {checking_dayweek()} {datetime.today().date()}"

    euro = get(f'http://api.nbp.pl/api/exchangerates/rates/a/EUR/{data}/?format=json').json()
    dolar = get(f'http://api.nbp.pl/api/exchangerates/rates/a/USD/{data}/?format=json').json()

    kurs_euro = euro['rates'][0]['mid']
    kurs_dolar = dolar['rates'][0]['mid']
    day_name = checking_dayweek(int(data.weekday()))

    todays_currency = f'Średni kurs NBP z dnia {day_name} {data}\n1€ = {kurs_euro} PLN\n1$ = {kurs_dolar} PLN'
    currency = Label(text=todays_currency, fg=PURPULE, bg=PEACH)
    currency.grid(row=6, column=0)

def reset_timer():
    master.after_cancel(timer)
    check_mark.config(text='')
    timer_label.config(text="Timer")
    timer_text.config(text="00:00")
    global reps
    reps = 0

def start_timer():
    global reps
    reps +=1
    work_sec = WORK_MIN
    short_breake_sec = SHORT_BREAK_MIN
    long_breake_sec = LONG_BREAK_MIN

    if reps % 8 ==0:
        count_down(long_breake_sec)
        timer_label.config(text=f"{LONG_BREAK_MIN} min Breake", fg=RED)
    elif reps % 2 == 0:
        count_down(short_breake_sec)
        timer_label.config(text=f"{SHORT_BREAK_MIN} min Breake", fg=PINK)
    else:
        count_down(work_sec)
        timer_label.config(text="Work", fg=GREEN)


def count_down(count):

    count_min = math.floor(count / 60)
    count_sec = count % 60
    if count_sec == 0:
        count_sec = "00"
    elif count_sec <=9:
        count_sec = f'0{count_sec}'
    timer_text.config(text=f"{count_min}:{count_sec}")
    if count > 0:
        global timer
        timer = master.after(1000, count_down, count-1)
    else:
        start_timer()
        marks = ''
        work_seasion = math.floor(reps/2)
        for _ in range(work_seasion):
            marks += "✔"
            check_mark.config(text=marks)

year_label = Label(text="Podaj rok swojego urodzenia RRRR", fg=PURPULE, bg=LIGHT,
                   font=(FONT_NAME, 10, "bold"))
year_label.grid(row=2, column=0, sticky=E)

month_label = Label(text="Podaj miesiąc swojego urodzenia MM", fg=PURPULE, bg=LIGHT,
                    font=(FONT_NAME, 10, "bold"))
month_label.grid(row=3, column=0, sticky=E)

day_label = Label(text="Podaj dzień swojego urodzenia DD", fg=PURPULE, bg=LIGHT,
                  font=(FONT_NAME, 10, "bold"))
day_label.grid(row=4, column=0, sticky=E)

year = Entry(width=15)
year.insert(END, string="1983")
year.grid(row=2, column=1, sticky=W)

month = Entry(width=15)
month.insert(END, string="12")
month.grid(row=3, column=1, sticky=W)

day = Entry(width=15)
day.insert(END, string="08")
day.grid(row=4, column=1, sticky=W)

b1 = Button(text="How many days did you live?", command=lived_days,
            fg=PURPULE, bg=LIGHT, font=(FONT_NAME, 10, "bold"), activebackground=PURPULE)
b1.grid(row=5, column=1)

currency_check = Button(text="Check today's currency",  command=checking_currency, fg=PURPULE, bg=LIGHT, font=(FONT_NAME, 10, 'bold'), activebackground=PURPULE)
currency_check.grid(row=6, column=1,  sticky=W)

close = Button(text="Close", command=close, fg=PURPULE, bg=LIGHT, font=(FONT_NAME, 10, "bold"), activebackground=PURPULE)
close.grid(row=1, column=2,  sticky=E)

timer_label = Label(text="Timer", fg=PURPULE, bg=LIGHT, font=(FONT_NAME, 45, "italic"), activebackground=PURPULE)
timer_label.grid(row=8, column=1,  sticky=E)

check_mark = Label(fg=PURPULE, bg=LIGHT, font=(45))
check_mark.grid(row=13, column=1, sticky=W)

start_button = Button(text="Start", command=start_timer, fg=PURPULE, bg=LIGHT, font=(FONT_NAME, 10, "bold"), activebackground=PURPULE)
start_button.grid(row=10, column=0, columnspan=2, sticky=E)

reset_button = Button(text="Reset", command=reset_timer, fg=PURPULE, bg=LIGHT, font=(FONT_NAME, 10, "bold"), activebackground=PURPULE)
reset_button.grid(row=10, column=1, sticky=W)

timer_text = Label(text="00:00", fg=PURPULE, bg=LIGHT, font=(FONT_NAME, 45, "bold"), activebackground=PURPULE)
timer_text.grid(row=13, column=0, columnspan=2, sticky=E)


img = PhotoImage(file='obrazek.png')
canvas = Canvas(width=260, height=260, bg=LIGHT, highlightthickness=0)
canvas.create_image(130, 130, image=img)
canvas.grid(row=0, column=2)
tick()
master.mainloop()