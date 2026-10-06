import re
def snal(snake):
    components=snake.split('_')
    return components[0] + ''.join(x.title() for x in components[1:])
text="hello_world_variable"
print(snal(text))