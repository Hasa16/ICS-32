def boxes(num: int):
    """Return num diagonal boxs."""
    boxtop = '+-+'
    boxside = '| |'
    boxbottom = '+-+'
    indents = '  '
    boxconnecting = '+-+-+'
    if num == 1:
        print(boxtop)
        print(boxside)
        print(boxbottom)
    else:
        print(boxtop)
        print(boxside)
        print(boxconnecting)
        for j in range(num - 2):
            print(indents * (j+1) + boxside)
            print(indents * (j+1) + boxconnecting)
        print(indents * (num - 1) + boxside)
        print(indents * (num - 1) + boxbottom)
      
    
User_Input = int(input())
boxes(User_Input)
