import turingarena as ta

H = 0   # horizontal placement of a tile (2 rows, 3 cols)
V = 1   # vertical placement of a tile (3 rows, 2 cols)

def offer_a_tiling(m,n):
    pass

def test_case(m,n):
    def turn_off_construction_goal_flags(m,n):
        if m == 1:
            ta.goals["construction_m1"] = False
        if m == 2:
            ta.goals["construction_m2"] = False
        if m <= 10 and n <= 10:
            ta.goals["construction_small"] = False
        ta.goals["construction"] = False

    def turn_off_decision_goal_flags(m,n):
        if m == 1:
            ta.goals["decision_m1"] = False
        if m == 2:
            ta.goals["decision_m2"] = False
        if m <= 10 and n <= 10:
            ta.goals["decision_small"] = False
        if m <= 100 and n <= 100:
            ta.goals["decision"] = False
        ta.goals["decision_huge"] = False
        
    with ta.run_algorithm(ta.submission.source) as p:
        print(f"case (m={m}, n={n})")
        res = p.functions.is_tilable(m, n)
        print(f"got {res}")
        tiling_exists = 1
        if (m*n)%6:
            tiling_exists = 0
        if (m <= 1) or (n<=1):
            tiling_exists = 0
        if res != tiling_exists:
            turn_off_decision_goal_flags(m,n)
            if res == 0:
                print("According to your is_tilable function, the %dx%d-grid is not tilable. However, we believe it is. If you need help, have a look at the tiling in the file: ... " % (m,n) )
                offer_a_tiling(m,n)
            if res != 0:
                print("According to your is_tilable function, the %dx%d-grid is tilable. Are you sure? If you can exhibit such a tiling, please contact turingarena.org, we look forward to see it." )
        
        if tiling_exists == 0:
            return

        if m > 100 or n > 100:
            return

        # BEGIN: testing of the procedure constructing the tiling
        posed_tiles = 0
        covered = [ [False for _ in range(n) ] for _ in range(m) ]
        def place_tile(row,col,dir):
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
                    print("La tua tessera fuoriesce dalla scacchiera nella cella (%d,%d)." % (row+1,col+1))
                    turn_off_construction_goal_flags(m,n)
                    return
                if covered[row][col]:
                    print("Due delle tue tegole coprono la cella (%d,%d)." % (row+1,col+1))
                    turn_off_construction_goal_flags(m,n)
                    return
                covered[row][col] = True

        print("[mostra il tiling (fino all'eventuale errore), magari in un file esterno da scaricare od un applet]")
        p.procedures.compose_tiling(m, n, callbacks = [place_tile] )
        if 6*posed_tiles == m*n:
            print("Complimenti! Hai riempito perfettamente la griglia. Il tuo tiling è stato verificato.")

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

ta.goals.setdefault("decision_m1", True)
ta.goals.setdefault("decision_m2", True)
ta.goals.setdefault("decision_small", True)
ta.goals.setdefault("decision", True)
ta.goals.setdefault("decision_huge", True)
ta.goals.setdefault("construction_m1", True)
ta.goals.setdefault("construction_m2", True)
ta.goals.setdefault("construction_small", True)
ta.goals.setdefault("construction", True)

print(ta.goals)

