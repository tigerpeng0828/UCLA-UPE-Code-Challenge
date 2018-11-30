import requests
row = 0
col = 0

def getStatus(token):
    return requests.post("http://ec2-34-216-8-43.us-west-2.compute.amazonaws.com/game?token="+token).json()

def main():
    laoji = {"uid":"904971546"}

    r = requests.post("http://ec2-34-216-8-43.us-west-2.compute.amazonaws.com/session", data=laoji)
    response = r.json()
    token = response['token']
    for i in range(5):
        game_states = requests.get("http://ec2-34-216-8-43.us-west-2.compute.amazonaws.com/game?token="+token).json()
        c,r = game_states['maze_size'][0], game_states['maze_size'][1]
        #current = game_states["current_location"]
        x = game_states["current_location"][0]
        y = game_states["current_location"][1]
        current = [y,x]
        print(game_states["status"])
        print(game_states["levels_completed"])
        row = r
        col = c
        maze(token, current)

def out_of_bound (coordinate, row, col):
    if coordinate[0] < 0 or coordinate[0] >= row or coordinate[1] < 0 or coordinate[1] >= col:
        return False
    return True

def reverse_dir (dir):
    if dir == "UP":
        return "DOWN"
    elif dir == "LEFT":
        return "RIGHT"
    elif dir == "RIGHT":
        return "LEFT"
    else:
        return "UP"

def maze(token,current):

    discovered_or_wall = []
    discovered_or_wall.append(current)
    helpmaze(current, token, discovered_or_wall)


def helpmaze(current, token,discovered_or_wall):

    dict={
    "UP" : [current[0]-1,current[1]] ,
    "DOWN": [current[0] + 1, current[1]],
    "LEFT": [current[0] , current[1]-1],
    "RIGHT":[current[0], current[1]+1]
    }

    for dir,coordinate in dict.items():
        if (not out_of_bound(coordinate,row,col)) and (coordinate not in discovered_or_wall):
            result = requests.post("http://ec2-34-216-8-43.us-west-2.compute.amazonaws.com/game?token="+token, {"action":dir}).json()
            print(result)
            if result["result"] == "WALL":
                discovered_or_wall.append(coordinate)
            elif result["result"] == "END":
                return True
            elif result["result"] == "SUCCESS":
                discovered_or_wall.append(coordinate)
                if helpmaze(coordinate, token, discovered_or_wall):
                    return True
                else:
                    r=requests.post("http://ec2-34-216-8-43.us-west-2.compute.amazonaws.com/game?token="+token, {"action":reverse_dir(dir)}).json()



    return False






if __name__ == '__main__':
    main()
