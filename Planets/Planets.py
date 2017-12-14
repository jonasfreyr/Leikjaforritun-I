from tkinter import *
import random
import math
import time

#Fall sem resetar leikinn
def reset():
    for a in root.winfo_children():
        a.destroy()
    global dot
    global canvas
    global Sx
    global Sy
    global wW
    global wH
    global fY
    global speed
    global room
    global oldroom
    global Cy
    global Cx
    global star
    global Seaty
    global Seatx
    global sol
    global dod
    global tel
    global planets
    global rooms
    global Dx
    global Dy
    global Dr
    global fuel
    global maxfuel
    global eydsla
    global Etel

    Sx = 200
    Sy = 200

    wW = 1200
    wH = 900

    Seaty = wH / 2
    Seatx = 800

    Cx = Seatx
    Cy = Seaty

    fY = "a"

    tel = 0

    speed = 7

    planets = []
    star = []

    rooms = ["R1", "R2", "R3", "R4"]
    oldroom = ""

    Dx = random.randint(10, 600)
    Dy = random.randint(10, 600)
    Dr = "R1"

    maxfuel = 100
    fuel = 100
    eydsla = 20
    Etel = 1

    sol = []

    dod = False

    canvas = Canvas(root, width=wW, height=wH, borderwidth=0, highlightthickness=0, bg="black")
    dot = canvas.create_circle(Dx, Dy, 3, fill="yellow")
    stars(500, 10, 10, wW, wH)

    R1()

    canvas.bind("<Key>", key)
    canvas.bind("<Button-1>", callback)
    canvas.pack()
    root.wm_title("Planets")

    homeS()

# Svo það er þæginlegt að búa til hringi
def _create_circle(self, x, y, r, **kwargs):
    global canvas
    return self.create_oval(x - r, y - r, x + r, y + r, **kwargs)

# Til að geta notað command til að búa til hring
Canvas.create_circle = _create_circle

# Svo það er þæginlegt að búa til pizzu form
def _create_circle_arc(self, x, y, r, **kwargs):
    global canvas
    if "start" in kwargs and "end" in kwargs:
        kwargs["extent"] = kwargs["end"] - kwargs["start"]
        del kwargs["end"]
    return self.create_arc(x - r, y - r, x + r, y + r, **kwargs)

# Til að geta notað command til að búa til pizzu form
Canvas.create_circle_arc = _create_circle_arc

# Þegar er ýtt á takka er farið hér
def key(event):
    global canvas
    global listi
    for a in listi:
        canvas.delete(a)
    print("pressed", repr(event.char))
    global fuel
    global maxfuel
    global eydsla
    global Etel
    global Sx
    global Sy
    global wW
    global wH
    global fY
    global speed
    global room
    global oldroom
    global Cy
    global Cx
    global star
    global Seaty
    global Seatx
    global sol
    global dod
    if event.char == "q":
        if room == "sR1" and Cx == Seatx and Cy == Seaty:
            if oldroom == "R1":
                R1()
            elif oldroom == "R2":
                R2()
            elif oldroom == "R3":
                R3()
            elif oldroom == "R4":
                R4()
        elif room != "sR1" and room != "sR2" and room != "sR3":
            oldroom = room
            sR1()
    if room == "sR1" or room == "sR2" or room == "sR3":
        if event.char == "w":
            if Cy > 254:
                Cy -= speed
        elif event.char == "s":
            if Cy < wH - 254:
                Cy += speed
        elif event.char == "a":
            if room != "sR3":
                if Cx > 50:
                    Cx -= speed
                else:
                    if room == "sR2":
                        sR3()
                    elif room == "sR1":
                        sR2()
                    Cx = wW
            else:
                if Cx > 303 + 50:
                    Cx -= speed
        elif event.char == "d":
            if room != "sR1":
                if Cx < wW - 50:
                    Cx += speed
                else:
                    if room == "sR2":
                        sR1()
                    elif room == "sR3":
                        sR2()
                    Cx = 2
            else:
                if Cx < 934 - 50:
                    Cx += speed

    else:
        if Etel % eydsla == 0:
            fuel = fuel - 1
        Etel += 1
        if event.char == "w":
            if Sy > 8:
                Sy -= speed
                fY = "w"
            else:
                if room == "R3":
                    R1()
                    Sy = wH
                elif room == "R4":
                    R2()
                    Sy = wH
        elif event.char == "s":
            if Sy < wH - 6:
                Sy += speed
                fY = "s"
            else:
                if room == "R1":
                    R3()
                    Sy = 0
                elif room == "R2":
                    R4()
                    Sy = 0
        elif event.char == "a":
            if Sx > 8:
                Sx -= speed
                fY = "a"
            else:
                if room == "R2":
                    R1()
                    Sx = wW
                elif room == "R4":
                    R3()
                    Sx = wW
        elif event.char == "d":
            if Sx < wW - 6:
                Sx += speed
                fY = "d"
            else:
                if room == "R1":
                    R2()
                    Sx = 0
                elif room == "R3":
                    R4()
                    Sx = 0
        for a in sol:
            canvas.delete(a)
        inn = False
        if room == "R1":
            tel = 0
            for a in range(628):
                if Sy > round(900 + 400 * math.sin(tel)) and Sx > round(
                                1200 + 400 * math.cos(tel)):  # 1200, 900
                    inn = True
                if Sy > round(900 + 300 * math.sin(tel)) and Sx > round(1200 + 300 * math.cos(tel)):
                    dod = True
                    break
                tel = round(tel + 0.01, 2)
        elif room == "R2":
            tel = 0
            for a in range(628):
                if Sy > round(900 + 400 * math.sin(tel)) and Sx < round(0 + 400 * math.cos(tel)):  # 0, 900
                    inn = True
                if Sy > round(900 + 300 * math.sin(tel)) and Sx < round(0 + 300 * math.cos(tel)):
                    dod = True
                    break
                tel = round(tel + 0.01, 2)
        elif room == "R3":
            tel = 0
            for a in range(628):
                if Sy < round(0 + 400 * math.sin(tel)) and Sx > round(1200 + 400 * math.cos(tel)):  # 1200, 0
                    inn = True
                if Sy < round(0 + 300 * math.sin(tel)) and Sx > round(1200 + 300 * math.cos(tel)):
                    dod = True
                    break
                tel = round(tel + 0.01, 2)
        elif room == "R4":
            tel = 0
            for a in range(628):
                if Sy < round(0 + 400 * math.sin(tel)) and Sx < round(0 + 400 * math.cos(tel)):  # 0, 0
                    inn = True
                if Sy < round(0 + 300 * math.sin(tel)) and Sx < round(0 + 300 * math.cos(tel)):
                    dod = True
                    break
                tel = round(tel + 0.01, 2)
        if inn == True:
            if dod == True:
                for a in sol:
                    canvas.delete(a)
                destroy(15)
            elif dod == False:
                sol.append(canvas.create_text(wW / 2, wH / 2, text="Heat Warning!", fill="white"))
    if room == "sR1" or room == "sR2" or room == "sR3":
        homeSS()
    else:
        homeS()
#Fall fyrir ef þú ert bensínlaus
def emty():
    global dod
    global sol
    dod = True
    canvas.bind("<Key>", dead)
    for a in sol:
        canvas.delete(a)
    user()
    canvas.create_text(wW / 2, wH / 2, text="Ship is out of fuel!", fill="white")
    canvas.create_rectangle((wW / 2) - 50, (wH / 2) + 10, (wW / 2) + 50, (wH / 2) + 50, fill="grey")
    canvas.create_text(wW / 2, (wH / 2) + 30, text="Restart", fill="white", anchor="center")

# Dautt fall(bara svo að þegar þú ert dauður getur ekki haldið áfram)
def dead(key):
    pass

# Þegar þú deyrð
def destroy(boom):
    global canvas
    global listi
    global sol
    global wW
    global wH
    canvas.create_circle(Sx, Sy, boom, fill="orange")
    for a in listi:
        canvas.delete(a)
    canvas.bind("<Key>", dead)
    user()
    canvas.create_text(wW / 2, wH / 2, text="Ship destroyed!", fill="white")
    canvas.create_rectangle((wW / 2) - 50, (wH / 2) + 10, (wW / 2) + 50, (wH / 2) + 50, fill="grey")
    canvas.create_text(wW / 2, (wH / 2) + 30, text="Restart", fill="white", anchor="center")

def user():
    global wW
    global wH
    global e1
    e1 = Entry(canvas)
    canvas.create_text(wW / 2, (wH / 2) + 60, text="Sláðu inn notenda nafn þitt", fill="white")
    canvas.create_window(wW / 2, (wH / 2) + 80, window=e1)
# Ef það er ýtt á músa takkann
def callback(event):
    global canvas
    global dod
    global tel
    global e1
    canvas.focus_set()
    print("clicked at", event.x, event.y)
    if dod == True:
        if event.x > (wW / 2) - 50 and event.y > (wH / 2) + 10 and event.x < (wW / 2) + 50 and event.y < (wH / 2) + 50:
            nafn = e1.get()
            if nafn != "":
                entry = ","+nafn+":"+str(tel)
                with open("scores.txt","a") as f:
                    f.write(entry)
            reset()

# Til að búa til punkt
def new_dot():
    global canvas
    global speed
    global dot
    global tel
    tel += 1
    global Dx
    global Dy
    global Dr
    global rooms
    global room
    global dtel

    Dx = random.randint(0, 1200)
    Dy = random.randint(0, 900)
    Dr = random.choice(rooms)
    tel1 = 0
    for a in range(628):
        if Dr == "R1":
            print("Y:", Dy)
            print("X:", Dx)
            print("Ry:", round(900 + 300 * math.sin(tel)))
            print("Rx:", round(1200 + 300 * math.cos(tel)))
            if Dy > round(900 + 300 * math.sin(tel1)) and Dx > round(1200 + 300 * math.cos(tel1)):
                print("yay!!")
                new_dot()
        elif Dr == "R2":
            if Dy > round(900 + 300 * math.sin(tel1)) and Dx < round(0 + 300 * math.cos(tel1)):
                new_dot()
        elif Dr == "R3":
            if Dy < round(0 + 300 * math.sin(tel1)) and Dx > round(1200 + 300 * math.cos(tel1)):
                new_dot()
        elif Dr == "R4":
            if Dy < round(0 + 300 * math.sin(tel1)) and Dx < round(0 + 300 * math.cos(tel1)):
                new_dot()
        tel1 = round(tel1 + 0.01, 2)
        # print(tel)

# Aðal skjár í geimskipi
def homeSS():
    global canvas
    global dot
    global Cx
    global Cy
    global listi
    canvas.delete(dot)
    listi = []
    listi.append(canvas.create_circle(Cx, Cy, 50, fill="white", outline=""))

# Aðal skjár í geimnum
def homeS():
    global canvas
    global dot
    canvas.delete(dot)
    global Sx
    global Sy
    global listi
    listi = []
    global fY
    global room
    global Dr
    global dod
    global maxfuel
    global fuel
    global wW
    global wH
    if room == Dr:
        dot = canvas.create_circle(Dx, Dy, 3, fill="yellow")
    try:
        with open("scores.txt","r") as f:
            text = f.read()
            users = text.split(",")
        telja = 0
        for a in users:
            nota = a.split(":")
            if int(nota[1]) > int(telja):
                nafn = nota[0]
                telja = nota[1]
        listi.append(canvas.create_text(wW/2,0,text="Hæsti notandi: "+nafn+" : "+str(telja),fill ="white",anchor = N))
    except:
        listi.append(
            canvas.create_text(wW / 2, 0, text="Hæsti notandi: Enginn", fill="white",anchor=N))
    if dod == False:
        if fY == "s":
            listi.append(canvas.create_circle(Sx, Sy - 8, 3, fill="lightblue", outline=""))
        elif fY == "w":
            listi.append(canvas.create_circle(Sx, Sy + 2, 3, fill="lightblue", outline=""))
        elif fY == "a":
            listi.append(canvas.create_circle(Sx + 2, Sy, 3, fill="lightblue", outline=""))
        elif fY == "d":
            listi.append(canvas.create_circle(Sx - 8, Sy, 3, fill="lightblue", outline=""))

        if fY == "s" or fY == "w":
            listi.append(canvas.create_circle(Sx, Sy, 3, fill="grey", outline=""))
            listi.append(canvas.create_circle(Sx, Sy - 2, 3, fill="grey", outline=""))
            listi.append(canvas.create_circle(Sx, Sy - 4, 3, fill="grey", outline=""))
            listi.append(canvas.create_circle(Sx, Sy - 6, 3, fill="grey", outline=""))
        elif fY == "a" or fY == "d":
            listi.append(canvas.create_circle(Sx, Sy, 3, fill="grey", outline=""))
            listi.append(canvas.create_circle(Sx - 2, Sy, 3, fill="grey", outline=""))
            listi.append(canvas.create_circle(Sx - 4, Sy, 3, fill="grey", outline=""))
            listi.append(canvas.create_circle(Sx - 6, Sy, 3, fill="grey", outline=""))
        if Sx - 3 <= Dx + 3 and Sx + 3 >= Dx - 3 and Sy - 3 <= Dy + 3 and Sy + 3 >= Dy - 3 and room == Dr:
            fuel = fuel + 10
            if fuel > maxfuel:
                fuel = maxfuel
            new_dot()
        if fuel == 0:
            emty()
    listi.append(canvas.create_text(wW - 10, 10, text="Stig: " + str(tel), width=100, anchor=NE, fill="white"))
    listi.append(canvas.create_text(0 + 10, 10, text="Fuel: " + str(fuel), width=100, anchor=NW, fill="white"))

# Til að búa til stjörnur
def stars(numb, x1, y1, x2, y2):
    global canvas
    for a in range(numb):
        x = random.randint(x1, x2)
        y = random.randint(y1, y2)
        star.append(canvas.create_circle(x, y, 1, fill="white", outline=""))

# Herbergi 1 í geimnum
def R1():
    global canvas
    global dot
    global room
    room = "R1"
    canvas.delete(dot)
    for a in planets:
        canvas.delete(a)
    planets.append(canvas.create_circle(100, 120, 50, fill="blue", outline="lightblue", width=4))
    planets.append(canvas.create_circle_arc(100, 120, 48, fill="green", outline="", start=45, end=140))
    planets.append(canvas.create_circle_arc(100, 120, 48, fill="green", outline="", start=275, end=305))
    planets.append(canvas.create_circle_arc(100, 120, 45, style="arc", outline="white", width=6, start=270 - 25,
                                            end=270 + 25))
    planets.append(canvas.create_circle(150, 40, 20, fill="#BBB", outline=""))
    planets.append(canvas.create_circle(140, 40, 2, fill="darkgrey", outline=""))
    planets.append(canvas.create_circle(160, 50, 4, fill="darkgrey", outline=""))
    planets.append(canvas.create_circle(160, 30, 3, fill="darkgrey", outline=""))

    planets.append(canvas.create_circle(1200, 900, 300, fill="#FF5C00"))
    planets.append(canvas.create_circle(1200, 900, 400, outline="#FF5C00"))

# Herbergi 2 í geimnum
def R2():
    global canvas
    global dot
    global room
    room = "R2"
    canvas.delete(dot)
    for a in planets:
        canvas.delete(a)
    planets.append(canvas.create_circle(0, 900, 300, fill="#FF5C00"))
    planets.append(canvas.create_circle(0, 900, 400, outline="#FF5C00"))

    planets.append(canvas.create_circle(900, 500, 45, fill="red"))
    planets.append(canvas.create_circle(880, 520, 10, fill="#E82A00", outline=""))
    planets.append(canvas.create_circle(920, 520, 8, fill="#E82A00", outline=""))
    planets.append(canvas.create_circle(900, 480, 5, fill="#E82A00", outline=""))

    planets.append(canvas.create_circle(500, 100, 60, fill="#FFA30B", outline="#FFBD05", width=4))

# Herbergi 3 í geimnum
def R3():
    global canvas
    global dot
    global room
    room = "R3"
    canvas.delete(dot)
    for a in planets:
        canvas.delete(a)
    planets.append(canvas.create_circle(1200, 0, 300, fill="#FF5C00"))
    planets.append(canvas.create_circle(1200, 0, 400, outline="#FF5C00"))

# Herbergi 4 í geimnum
def R4():
    global canvas
    global dot
    global room
    room = "R4"
    canvas.delete(dot)
    for a in planets:
        canvas.delete(a)
    planets.append(canvas.create_circle(0, 0, 300, fill="#FF5C00"))
    planets.append(canvas.create_circle(0, 0, 400, outline="#FF5C00"))

    planets.append(canvas.create_circle(900, 600, 150, fill="#FFA700"))
    planets.append(canvas.create_circle(900, 600, 225, outline="#FFE100", width=40))

# Herbergi 1 í geimskipi
def sR1():
    global canvas
    global dot
    global wW
    global wH
    global Seatx
    global Seaty
    global room
    room = "sR1"
    canvas.delete(dot)
    for a in planets:
        canvas.delete(a)
    planets.append(canvas.create_rectangle(0, 200, (wW / 4) * 3, 700, fill="darkgrey"))
    planets.append(canvas.create_polygon(900, 200, wW, wH / 2, 900, 700, fill="darkgrey"))
    planets.append(
        canvas.create_rectangle(Seatx - 50, Seaty - 50, Seatx + 50, Seaty + 50, fill="brown", outline=""))

# Herbergi 2 í geimskipi
def sR2():
    global canvas
    global wW
    global wH
    global room
    room = "sR2"
    for a in planets:
        canvas.delete(a)
    planets.append(canvas.create_rectangle(0, 200, wW, 700, fill="darkgrey"))

# Herbergi 3 í geimskipi
def sR3():
    global canvas
    global wW
    global wH
    global room
    room = "sR3"
    for a in planets:
        canvas.delete(a)
    planets.append(canvas.create_circle(300, wH / 2, 250, fill="lightblue", outline=""))
    planets.append(canvas.create_rectangle(300, 200, wW, 700, fill="darkgrey", outline=""))


root = Tk()
reset()
root.mainloop()