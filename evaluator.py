import turingarena as ta

H = 0   # horizontal placement of a tile (2 rows, 3 cols)
V = 1   # vertical placement of a tile (3 rows, 2 cols)

i_file_generated = 0
def offer_a_tiling(m,n):
    global i_file_generated
    i_file_generated += 1
    tiling="ciao mamma"
#    ta.send_file(tiling, filename=f"tiling_{i_file_generated}.txt")
#    ta.evallib.evaluation.send_file_as_path(tiling, filename=f"tiling_{i_file_generated}.txt")


def test_case(m,n):
    def turn_off_construction_goal_flags(m,n):
        if m == 2:
            ta.goals["construction_m2"] = False
        if m <= 10 and n <= 10:
            ta.goals["construction_small"] = False
        ta.goals["construction"] = False

    def turn_off_decision_goal_flags(m,n):
        if m == 2:
            ta.goals["decision_m2"] = False
        if m <= 10 and n <= 10:
            ta.goals["decision_small"] = False
        if m <= 100 and n <= 100:
            ta.goals["decision"] = False
        ta.goals["decision_huge"] = False
        
    with ta.run_algorithm(ta.submission.source) as p:
        print(f"case (m={m}, n={n})")
        tiling_exists = 1
        if (m*n)%6:
            tiling_exists = 0
        if (m <= 1) or (n<=1):
            tiling_exists = 0
        try:
            res = p.functions.is_tilable(m, n)
        except ta.AlgorithmError as e:
            print(f"During the execution of your function is_tilable({m},{n}) we got the following exception:")
            print(e)
            turn_off_decision_goal_flags(m,n)
        else:
            print(f"From your is_tilable({m},{n}) function we expected {tiling_exists}, got {res}")
            if res == tiling_exists:
                print("OK. The two values coincide.")
            else:
                turn_off_decision_goal_flags(m,n)
                if res == 0:
                    turn_off_construction_goal_flags(m,n)
                    print(f"According to your is_tilable function, the {m}x{n}-grid is not tilable with 2,3-bars. However, we believe it is! If you disbelieve this and/or need help to advance, have a look at the tiling offered in the spoiling solution file: ... ")
                    offer_a_tiling(m,n)
                if res != 0:
                    print(f"According to your is_tilable function, the {m}x{n}-grid is tilable. Are you sure?\n In case you can exhibit such a tiling, please contact turingarena.org, we look forward to see it." )
        
        if not tiling_exists or res == 0 or m > 100 or n > 100:
            return

        # BEGIN: testing of the procedure constructing the tiling
        print(f"Ok, you claim the tiling exists, and ({m},{n}) <= (100,100). Let's hence see if you can actually construct the tiling.")
        construction_ok = True
        posed_tiles = 0
        covered = [ [False for _ in range(n) ] for _ in range(m) ]
        def place_tile(row,col,dir):
            nonlocal construction_ok
            nonlocal posed_tiles
            nonlocal covered
            row, col = row - 1, col - 1
            if dir == H:
                cells = [ [row,col], [row,col+1], [row,col+2], [row+1,col], [row+1,col+1], [row+1,col+2] ]
            else:    
                cells = [ [row,col], [row+1,col], [row+2,col], [row,col+1], [row+1,col+1], [row+2,col+1] ]
            posed_tiles += 1
            for cell in cells:
                row = cell[0]
                col = cell[1]
                if row < 0 or col < 0 or row >= m or col >= n:
                    print(f"La tua tessera fuoriesce dalla scacchiera nella cella ({row},{col}).")
                    construction_ok = False
                    return
                if covered[row][col]:
                    print(f"Due delle tue tegole coprono la cella ({row},{col}).")
                    construction_ok = False
                    return
                covered[row][col] = True

        try:
            print("[mostra il tiling (fino all'eventuale errore), magari in un file esterno da scaricare od un applet]")
            p.procedures.compose_tiling(m, n, callbacks = [place_tile] )
        except ta.AlgorithmError as e:
            print(f"During the execution of your procedure compose_tiling({m},{n}) we got the following exception:")
            print(e)
            turn_off_construction_goal_flags(m,n)
        else:
            if construction_ok:
                if 6*posed_tiles == m*n:
                    print(f"Complimenti! Hai riempito perfettamente la griglia ({m},{n}). Il tuo tiling è corretto.")
                else:
                    print(f"NO: non hai ricoperto l'intera griglia ({m},{n}). Hai collocato solo {posed_tiles} tessere. Di positivo: non sei uscito dalla griglia ({m},{n}) e non hai sovrapposto tessere. Nessun conflitto.")
                    turn_off_construction_goal_flags(m,n)
            else:
                turn_off_construction_goal_flags(m,n)

                
def run_all_test_cases():
    for m in range(1,8):
        for n in range(1,8):
            test_case(m,n)
    test_case(9,9)        
    test_case(9,10)        
    test_case(10,10)        
    test_case(99,99)        
    test_case(100,100)        
    test_case(99999,99999)        
    test_case(100000,100000)        
        
run_all_test_cases()

ta.goals.setdefault("decision_m2", True)
ta.goals.setdefault("decision_small", True)
ta.goals.setdefault("decision", True)
ta.goals.setdefault("decision_huge", True)
ta.goals.setdefault("construction_m2", True)
ta.goals.setdefault("construction_small", True)
ta.goals.setdefault("construction", True)

print(ta.goals)

