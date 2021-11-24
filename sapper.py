from random import randrange

arxiv_p = []
arxiv_pm = []


def create_game(N, K, M):
    P = [-2] * N * K
    PM = [0] * N * K
    n = M
    while n>0:
        i = randrange(K)
        j = randrange(N)
        if PM[i*N+j] != 0:
            continue
        PM[i*N+j] = -1
        n -= 1
    for i in range(K):
        for j in range(N):
            if PM[i*N+j] >= 0:
                PM[i*N+j] = get_total_mines(i, j, PM)
    return PM, P


def get_total_mines(i, j, PM):
    n = 0
    for k in range(-1, 2):
        for l in range(-1, 2):
            x = i + k
            y = j + l
            if x < 0 or x >= N or y < 0 or y >= K:
                continue
            if PM[y * N + x] < 0:
                n += 1

    return n


def show(pole):
    for i in range(N):
        for j in range(N):
            print(str(pole[i*N+j]).rjust(3), end="")
        print()


def go():
    loop_input = True
    while loop_input:
        x, y = input('Введите координату x: '), input('Введите координату y: ')

        if not x.isdigit() or not y.isdigit():
            print("Координаты введены неверно")
            continue
        x = int(x) - 1
        y = int(y) - 1

        if x < 0 or x >= N or y < 0 or y >= N:
            print("Координаты выходят за пределы поля")
            continue
        action = input('Чтобы установить флажок на клетку, наберите flag; чтобы раскрыть клетку, наберите open: ')
        if action not in ('flag', 'open'):
            print("Действие введенно неверно")
            continue
        loop_input = False

    return x, y, action


def is_finish(PM, P, N, K):
    for i in range(N * K):
        if P[i] != -2 and PM[i] < 0: return -1
    for i in range(N * K):
        if P[i] == -2 and PM[i] >= 0: return 1

    return -2


def start_game():
    finish_state = is_finish(PM, P, N, K)
    flags_left = M
    while finish_state > 0:
        show(P)
        x, y, action = go()
        if action == 'open':
            P[x * N + y] = PM[x * N + y]
        elif flags_left > 0:
            P[x * N + y] = 'f'
            flags_left -= 1
        else:
            print('Вы поставили максимальное количество флагов')
            continue
        finish_state = is_finish(PM, P, N, K)
    arxiv_p.append(P)
    arxiv_pm.append(PM)
    return finish_state


are_continuing = True

while are_continuing:
    N, K = input('Введите размеры поля по горизонтали: '), input('Введите размеры поля по вертикали: ')
    M = input('Введите количество мин на поле: ')
    if not N.isdigit() or not K.isdigit() or not M.isdigit():
        print("Данные введены неверно")
        continue
    N, K, M = int(N), int(K), int(M)
    PM, P = create_game(N, K, M)
    res = start_game()
    if res == -1:
        print("Вы проиграли")
    else:
        print("Вы выиграли")
    say = '0'
    while say not in ('1','9'):
        say = input('''Чтобы выйти из игры, нажмите 1; чтобы продолжить, нажмите 9; если хотите получить архив ваших 
                    игр: для показа видимых части нажмите 5, а для показа скрытой (карт бомб) нажмите 7''')
        if say == '1':
            are_continuing = False
        elif say == '5':
            for pole in arxiv_p:
                show(pole)
        elif say == '7':
            for pole in arxiv_pm:
                show(pole)
        elif say == '9':
            break


print('Вы полностью вышли из игры')
