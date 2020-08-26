import json
import os
import random
import socket
import sys

sys.path.append(os.getcwd())

from lib.player_base import Player, PlayerShip


get_msg = {}

class RandomPlayer(Player):

    def __init__(self):

        # フィールドを2x2の配列として持っている．
        self.field = [[i, j] for i in range(Player.FIELD_SIZE)
                      for j in range(Player.FIELD_SIZE)]

        # 初期配置を非復元抽出でランダムに決める．
        """
        ps = random.sample(self.field, 3)
        positions = {'w': ps[0], 'c': ps[1], 's': ps[2]}
        """

        positions = {'w': [1,1], 'c': [0,0], 's': [4,4] }

        self.counter_1 = 0
        self.counter_2 = 0
        self.counter_3 = 0

        super().__init__(positions)

    #
    # 移動か攻撃かランダムに決める．
    # どれがどこへ移動するか，あるいはどこに攻撃するかもランダム．
    #
    def action(self,get_msg):
        """
        act = random.choice(["move", "attack"])

        if act == "move":
            ship = random.choice(list(self.ships.values()))
            to = random.choice(self.field)
            while not ship.can_reach(to) or not self.overlap(to) is None:
                to = random.choice(self.field)

            return json.dumps(self.move(ship.type, to))
        elif act == "attack":
            to = random.choice(self.field)
            while not self.can_attack(to):
                to = random.choice(self.field)

            return json.dumps(self.attack(to))
        """


        


        self.counter_1 = self.counter_1 + 1

        if self.counter_1 % 10 != 0:
            self.counter_2 = self.counter_2 + 1
            if self.counter_2 % 9 ==1:
                to = [json.loads(get_msg)["condition"]["me"]["w"]["position"][0] - 1, json.loads(get_msg)["condition"]["me"]["w"]["position"][1] - 1] 
                return json.dumps(self.attack(to)) 
            elif self.counter_2 % 9 ==2:
                to = [json.loads(get_msg)["condition"]["me"]["w"]["position"][0] - 0, json.loads(get_msg)["condition"]["me"]["w"]["position"][1] - 1] 
                return json.dumps(self.attack(to)) 
            elif self.counter_2 % 9 ==3:
                to = [json.loads(get_msg)["condition"]["me"]["w"]["position"][0] + 1, json.loads(get_msg)["condition"]["me"]["w"]["position"][1] - 1] 
                return json.dumps(self.attack(to)) 
            elif self.counter_2 % 9 ==4:
                to = [json.loads(get_msg)["condition"]["me"]["w"]["position"][0] - 1, json.loads(get_msg)["condition"]["me"]["w"]["position"][1] + 0] 
                return json.dumps(self.attack(to)) 
            elif self.counter_2 % 9 ==5:
                to = [json.loads(get_msg)["condition"]["me"]["w"]["position"][0] + 1, json.loads(get_msg)["condition"]["me"]["w"]["position"][1] + 0] 
                return json.dumps(self.attack(to)) 
            elif self.counter_2 % 9 ==6:
                to = [json.loads(get_msg)["condition"]["me"]["w"]["position"][0] - 1, json.loads(get_msg)["condition"]["me"]["w"]["position"][1] + 1] 
                return json.dumps(self.attack(to)) 
            elif self.counter_2 % 9 ==7:
                to = [json.loads(get_msg)["condition"]["me"]["w"]["position"][0] - 0, json.loads(get_msg)["condition"]["me"]["w"]["position"][1] + 1] 
                return json.dumps(self.attack(to)) 
            elif self.counter_2 % 9 ==8:
                to = [json.loads(get_msg)["condition"]["me"]["w"]["position"][0] + 1, json.loads(get_msg)["condition"]["me"]["w"]["position"][1] + 1] 
                return json.dumps(self.attack(to)) 
            elif self.counter_2 % 9 ==0:
                to = [json.loads(get_msg)["condition"]["me"]["w"]["position"][0] + 0, json.loads(get_msg)["condition"]["me"]["w"]["position"][1] + 0] 
                return json.dumps(self.attack(to)) 
        
        
        elif self.counter_1 % 10 == 0:
            self.counter_3 = self.counter_3 + 1
            if self.counter_3 % 4 == 1:
                to = [1,3]
                return json.dumps(self.move("w", to)) 
            elif self.counter_3 % 4 == 2:
                to = [3,3]
                return json.dumps(self.move("w", to)) 
            elif self.counter_3 % 4 == 3:
                to = [3,1]
                return json.dumps(self.move("w", to)) 
            elif self.counter_3 % 4 == 0:
                to = [1,1]
                return json.dumps(self.move("w", to)) 

# 仕様に従ってサーバとソケット通信を行う．
def main(host, port, seed=0):
    assert isinstance(host, str) and isinstance(port, int)

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.connect((host, port))
        with sock.makefile(mode='rw', buffering=1) as sockfile:
            get_msg = sockfile.readline()
            print(get_msg)
            player = RandomPlayer()
            sockfile.write(player.initial_condition()+'\n')

            while True:
                info = sockfile.readline().rstrip()
                print(info)
                
                if info == "your turn":
                    sockfile.write(player.action(get_msg)+'\n')
                    get_msg = sockfile.readline()
                    player.update(get_msg)
                    
                elif info == "waiting":
                    get_msg = sockfile.readline()
                    player.update(get_msg)
                    
                elif info == "you win":
                    break
                elif info == "you lose":
                    break
                elif info == "even":
                    break
                else:
                    raise RuntimeError("unknown information")


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(description="Sample Player for Submaline Game")
    parser.add_argument(
        "host",
        metavar="H",
        type=str,
        help="Hostname of the server. E.g., localhost",
    )
    parser.add_argument(
        "port",
        metavar="P",
        type=int,
        help="Port of the server. E.g., 2000",
    )
    parser.add_argument(
        "--seed",
        type=int,
        help="Random seed of the player",
        required=False,
        default=0,
    )
    args = parser.parse_args()

    main(args.host, args.port, seed=args.seed)