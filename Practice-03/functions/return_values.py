def p(widht,hight):
    area=widht*hight
    perimeter=2*(widht+hight)
    return area,perimeter
r_widht=int(input())
r_hight=int(input())
result_area,result_perimater=p(r_widht,r_hight)
print(result_area)
print(result_perimater)
