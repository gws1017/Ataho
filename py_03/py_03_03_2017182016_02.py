import turtle as t

t.up()
t.goto(-30,-100)
t.down()


count = 0
while(count<6):
    t.fd(500) #가로 전진
    t.up()
    t.goto(-30 + 100 * count , -100) #세로 전진전에 시작위치 이동
    t.down()
    t.lt(90)
    t.fd(500) #세로 전진
    t.up()
    t.goto(-30 , -100 + 100 * (count+1)) #가로 전진전에 시작위치 이동
    t.down()
    t.rt(90)
    count += 1

t.exitonclick()
 
