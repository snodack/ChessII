// pch.cpp: файл исходного кода, соответствующий предварительно скомпилированному заголовочному файлу

#include "pch.h"
#include <array>
#include <vector>
#include <map>
#include <string>
#include <iostream>
#include <vector>
#include <cctype>
using namespace::std;
// При использовании предварительно скомпилированных заголовочных файлов необходим следующий файл исходного кода для выполнения сборки.
#define CHESSDLL extern "C" __declspec(dllexport)
#define Board array<array<int, 8>, 8>
#define Castl_arr pair<pair<bool, bool>, pair<bool, bool>>

enum figures { KING = 6, QUEEN = 5, ROCK = 4, BISHOP = 3, KNIGHT = 2, PAWN = 1 };

int count_pos = 0;
class GamePos {
public:
    Board position = { {0} };
    Castl_arr castling;
    bool color;
    string last_move;
    GamePos(Board _position, Castl_arr _castling, bool _color, string _last_move) {
        position = _position;
        castling = _castling;
        color = _color;
        last_move = _last_move;
    }
    void change_color() {
        color = !color;
    }


};
bool is_enemy(int cell_position, int figure, bool enemy_color);
bool check_castling_shah(GamePos pos, string move);
GamePos make_move(GamePos current_pos, string move);
vector<string> find_chess_move(bool color, Board position, int rank, int file, pair<bool, bool> castling_data, string last_move);
vector<string> find_rock_moves(bool color, Board position, int rank, int file);
bool check_shah(GamePos pos);
float evaluate(GamePos position, int depth, float alpha, float beta);

const float K[8][8] = {
    {-3, -4, -4, -5, -5, -4, -4, -3},
        {-3, -4, -4, -5, -5, -4, -4, -3},
        {-3, -4, -4, -5, -5, -4, -4, -3},
        {-3, -4, -4, -5, -5, -4, -4, -3},
        {-2, -3, -3, -4, -4, -3, -3, -2},
        {-1, -2, -2, -2, -2, -2, -2, -1},
        {2, 2, 0, 0, 0, 0, 2, 2},
        {2, 3, 1, 0, 0, 1, 3, 2}
};
const float Q[8][8] = {
        { -2, -1, -1, -0.5, -0.5, -1, -1, -2},
        { -1,  0,  0,  0,  0,  0,  0, -1},
        { -1,  0,  0.5,  0.5,  0.5,  0.5,  0, -1},
        { -0.5,  0,  0.5,  0.5,  0.5,  0.5,  0, -0.5},
        {  0,  0,  0.5,  0.5,  0.5,  0.5,  0, -0.5},
        { -1,  0.5,  0.5,  0.5,  0.5,  0.5,  0, -1},
        { -1,  0,  0.5,  0,  0,  0,  0, -1},
        { -2, -1, -1, -0.5, -0.5, -1, -1, -2}
};
const float R[8][8] = {
        {  0.0,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0},
        {  0.5,  1.0,  1.0,  1.0,  1.0,  1.0,  1.0,  0.5},
        { -0.5,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0, -0.5},
        { -0.5,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0, -0.5},
        { -0.5,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0, -0.5},
        { -0.5,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0, -0.5},
        { -0.5,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0, -0.5},
        {  0.0,   0.0, 0.0,  0.5,  0.5,  0.0,  0.0,  0.0}
};
const float N[8][8] = {
        {-5.0, -4.0, -3.0, -3.0, -3.0, -3.0, -4.0, -5.0},
        {-4.0, -2.0,  0.0,  0.0,  0.0,  0.0, -2.0, -4.0},
        {-3.0,  0.0,  1.0,  1.5,  1.5,  1.0,  0.0, -3.0},
        {-3.0,  0.5,  1.5,  2.0,  2.0,  1.5,  0.5, -3.0},
        {-3.0,  0.0,  1.5,  2.0,  2.0,  1.5,  0.0, -3.0},
        {-3.0,  0.5,  1.0,  1.5,  1.5,  1.0,  0.5, -3.0},
        {-4.0, -2.0,  0.0,  0.5,  0.5,  0.0, -2.0, -4.0},
        {-5.0, -4.0, -3.0, -3.0, -3.0, -3.0, -4.0, -5.0}
};
const float B[8][8] = {
        { -2.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -2.0},
        { -1.0,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0, -1.0},
        { -1.0,  0.0,  0.5,  1.0,  1.0,  0.5,  0.0, -1.0},
        { -1.0,  0.5,  0.5,  1.0,  1.0,  0.5,  0.5, -1.0},
        { -1.0,  0.0,  1.0,  1.0,  1.0,  1.0,  0.0, -1.0},
        { -1.0,  1.0,  1.0,  1.0,  1.0,  1.0,  1.0, -1.0},
        { -1.0,  0.5,  0.0,  0.0,  0.0,  0.0,  0.5, -1.0},
        { -2.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -2.0}
};
const float P[8][8] = {
        {0.0,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0},
        {5.0,  5.0,  5.0,  5.0,  5.0,  5.0,  5.0,  5.0},
        {1.0,  1.0,  2.0,  3.0,  3.0,  2.0,  1.0,  1.0},
        {0.5,  0.5,  1.0,  2.5,  2.5,  1.0,  0.5,  0.5},
        {0.0,  0.0,  0.0,  2.0,  2.0,  0.0,  0.0,  0.0},
        {0.5, -0.5, -1.0,  0.0,  0.0, -1.0, -0.5,  0.5},
        {0.5,  1.0, 1.0,  -2.0, -2.0,  1.0,  1.0,  0.5},
        {0.0,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0}
};
map<string, int> figures_price = { {"K", 900}, {"Q", 90}, {"R", 50}, {"B", 30,}, {"N", 30}, {"P", 10} };

float eval_func(GamePos game) {
    float result = 0;
    for (size_t i = 0; i < 8; ++i) {
        for (size_t j = 0; j < 8; ++j) {
            bool color = game.position[i][j] > 0;
            int figure = abs(game.position[i][j]);
            switch (figure)
            {
            case KING:
            {
                if (color)
                    result += (figures_price["K"] + K[i][j]);
                else
                    result -= (figures_price["K"] + K[abs(int(i) - 7)][j]);
                break;
            }
            case QUEEN:
            {
                if (color)
                    result += (figures_price["Q"] + K[i][j]);
                else
                    result -= (figures_price["Q"] + K[abs(int(i) - 7)][j]);
                break;
            }
            case ROCK:
            {
                if (color)
                    result += (figures_price["R"] + K[i][j]);
                else
                    result -= (figures_price["R"] + K[abs(int(i) - 7)][j]);
                break;
            }
            case KNIGHT:
            {
                if (color)
                    result += (figures_price["N"] + K[i][j]);
                else
                    result -= (figures_price["N"] + K[abs(int(i) - 7)][j]);
                break;
            }
            case BISHOP:
            {
                if (color)
                    result += (figures_price["B"] + K[i][j]);
                else
                    result -= (figures_price["B"] + K[abs(int(i) - 7)][j]);
                break;
            }
            case PAWN:
            {
                if (color)
                    result += (figures_price["P"] + K[i][j]);
                else
                    result -= (figures_price["P"] + K[abs(int(i) - 7)][j]);
                break;
            }

            default:
                break;
            }
        }
    }
    return result;
}
string evaluate_root(GamePos position, int depth = 5) {
    /*
        Функция полной оценки

        Параметры :
    eval_func->функция оценки текущей позиции
        position->текущая позиция
        depth->глубина поиска

        Вызывается рекурсивно
        Возвращает оценку, положительно->перевес в сторону белых, отрицательно->в сторону черныx
        */
    if (depth == 0 or depth > 16)
        throw "Error depth search";
    float best_move_eval = position.color ? -9999.F : 9999.F;
    string best_move = "";
    for (int i = 0; i < 8; i++) {
        for (int j = 0; j < 8; j++) {
            vector<string> moves = find_chess_move(position.color, position.position, i, j, position.castling.second, "-");
            for (int move_i = 0; move_i < moves.size(); move_i++) {
                GamePos new_pos = make_move(position, moves[move_i]);
                new_pos.change_color();
                float eval = evaluate(new_pos, depth - 1, -10001, 10001);
                if ((position.color and eval > best_move_eval) or (!position.color and eval < best_move_eval)) {
                    best_move = moves[move_i];
                    best_move_eval = eval;
                }

            }


        }
    }

    cout << "evaluation of move " << best_move_eval;
    return best_move;
}
float evaluate(GamePos position, int depth, float alpha, float beta) {
    if (depth == 0)
        return eval_func(position);
    count_pos++;
    float best_move = position.color ? -9999 : 9999;
    for (int i = 0; i < 8; i++) {
        for (int j = 0; j < 8; j++) {
            vector<string> moves = find_chess_move(position.color, position.position, i, j, position.castling.second, "-");
            if (position.color) {
                for (int move_i = 0; move_i < moves.size(); move_i++) {
                    GamePos new_pos = make_move(position, moves[move_i]);
                    //Проверка на недопустимость хода
                    if (!check_shah(new_pos) or (moves[move_i].length() < 3 and !check_castling_shah(position, moves[move_i]))) continue;
                    new_pos.change_color();
                    best_move = max(best_move, evaluate(new_pos, depth - 1, alpha, beta));
                    alpha = max(alpha, best_move);
                    if (beta <= alpha)
                        return best_move;
                }
            }
            else {
                for (int move_i = 0; move_i < moves.size(); move_i++) {
                    GamePos new_pos = make_move(position, moves[move_i]);
                    //Проверка на недопустимость хода
                    if (!check_shah(new_pos) or (moves[move_i].length() < 3 and !check_castling_shah(position, moves[move_i]))) continue;
                    new_pos.change_color();
                    best_move = min(best_move, evaluate(new_pos, depth - 1, alpha, beta));
                    beta = min(beta, best_move);
                    if (beta <= alpha)
                        return best_move;
                }

            }
        }
    }
    return best_move;

}

vector<string> find_rock_moves(bool color, Board position, int rank, int file) {
    string current_pos_dig_not = to_string(file) + to_string(rank);
    vector<string> moves = {};
    vector<pair<int, int>>default_rock_moves = { {-1, 0} ,{1, 0},{0, -1},{0, 1} };
    moves = {};
    for (int i = 0; i < default_rock_moves.size(); i++) {
        pair<int, int> current_pair = default_rock_moves[i];
        for (int j = 1; j < 8; j++) {
            int cache_file = file + current_pair.first * j;
            int cache_rank = rank + current_pair.second * j;
            if ((0 <= cache_file and cache_file <= 7) and (0 <= cache_rank and cache_rank <= 7)) {
                if (position[cache_file][cache_rank] == 0) {
                    //cout << current_pos_dig_not + to_string(cache_file) + to_string(cache_rank) << ", ";
                    moves.push_back(current_pos_dig_not + to_string(cache_file) + to_string(cache_rank));
                }
                else if ((position[cache_file][cache_rank] < 0 and color) or (not color and position[cache_file][cache_rank] > 0)) {
                    //cout << current_pos_dig_not + to_string(cache_file) + to_string(cache_rank) << ", ";
                    moves.push_back(current_pos_dig_not + to_string(cache_file) + to_string(cache_rank));
                    break;
                }
                else
                    break;
            }
            else
                break;
        }

    }

    return moves;
}
vector<string> find_bishop_moves(bool color, Board position, int rank, int file) {
    string current_pos_dig_not = to_string(file) + to_string(rank);
    vector<string> moves = {};
    vector<pair<int, int>>default_bishop_moves = { {-1, 1} ,{1, 1},{1, -1},{-1, -1} };
    moves = {};
    for (int i = 0; i < default_bishop_moves.size(); i++) {
        pair<int, int> current_pair = default_bishop_moves[i];
        for (int j = 1; j < 8; j++) {
            int cache_file = file + current_pair.first * j;
            int cache_rank = rank + current_pair.second * j;
            if ((0 <= cache_file and cache_file <= 7) and (0 <= cache_rank and cache_rank <= 7)) {
                if (position[cache_file][cache_rank] == 0) {
                    //cout << current_pos_dig_not + to_string(cache_file) + to_string(cache_rank) << ", ";
                    moves.push_back(current_pos_dig_not + to_string(cache_file) + to_string(cache_rank));
                }
                else if ((position[cache_file][cache_rank] < 0 and color) or (not color and position[cache_file][cache_rank] > 0)) {
                    //cout << current_pos_dig_not + to_string(cache_file) + to_string(cache_rank) << ", ";
                    moves.push_back(current_pos_dig_not + to_string(cache_file) + to_string(cache_rank));
                    break;
                }
                else
                    break;
            }
            else
                break;
        }

    }

    return moves;
}
vector<string> find_knight_moves(bool color, Board position, int rank, int file) {
    string current_pos_dig_not = to_string(file) + to_string(rank);
    vector<string> moves = {};
    vector<pair<int, int>>default_knight_moves = { {-2, -1} ,{-2, 1},{2, -1},{2, 1},{-1, -2},{1, -2},{-1, 2},{1, 2} };
    moves = {};
    for (int i = 0; i < default_knight_moves.size(); i++) {
        pair<int, int> current_pair = default_knight_moves[i];
        int cache_file = file + current_pair.first;
        int cache_rank = rank + current_pair.second;
        if ((0 <= cache_file and cache_file <= 7) and (0 <= cache_rank and cache_rank <= 7)) {
            if (position[cache_file][cache_rank] == 0) {
                //cout << current_pos_dig_not + to_string(cache_file) + to_string(cache_rank) << ", ";
                moves.push_back(current_pos_dig_not + to_string(cache_file) + to_string(cache_rank));
            }
            else if ((position[cache_file][cache_rank] < 0 and color) or (not color and position[cache_file][cache_rank] > 0)) {
                //cout << current_pos_dig_not + to_string(cache_file) + to_string(cache_rank) << ", ";
                moves.push_back(current_pos_dig_not + to_string(cache_file) + to_string(cache_rank));
            }
        }
    }
    return moves;
}
vector<string> find_queen_moves(bool color, Board position, int rank, int file) {
    vector<string> rock_moves = find_rock_moves(color, position, rank, file);
    vector<string> bishop_moves = find_bishop_moves(color, position, rank, file);
    rock_moves.insert(rock_moves.end(), bishop_moves.begin(), bishop_moves.end());
    return rock_moves;
}
vector<string> find_king_moves(bool color, Board position, int rank, int file, pair<bool, bool> castling_data) {
    string current_pos_dig_not = to_string(file) + to_string(rank);
    vector<string> moves = {};
    vector<pair<int, int>>default_king_moves = { {1,-1}, {1,0}, {1,1}, {0,-1}, {0,1},{-1,-1}, {-1,0}, {-1,1} };
    for (int i = 0; i < default_king_moves.size(); i++) {
        pair<int, int> current_pair = default_king_moves[i];
        int cache_file = file + current_pair.first;
        int cache_rank = rank + current_pair.second;
        if ((0 <= cache_file and cache_file <= 7) and (0 <= cache_rank and cache_rank <= 7)) {
            if (position[cache_file][cache_rank] == 0) {
                //cout << current_pos_dig_not + to_string(cache_file) + to_string(cache_rank) << ", ";
                moves.push_back(current_pos_dig_not + to_string(cache_file) + to_string(cache_rank));
            }
            else if ((position[cache_file][cache_rank] < 0 and color) or (not color and position[cache_file][cache_rank] > 0)) {
                //cout << current_pos_dig_not + to_string(cache_file) + to_string(cache_rank) << ", ";
                moves.push_back(current_pos_dig_not + to_string(cache_file) + to_string(cache_rank));
            }
        }
    }
    //Рокировка
    //Короткая 0 - 0
    if (castling_data.first and position[file][rank + 1] == 0 and position[file][rank + 2] == 0) {
        moves.push_back("OO");
    }
    if (castling_data.second and
        position[file][rank - 1] == 0 and
        position[file][rank - 2] == 0 and
        position[file][rank - 3] == 0) {
        moves.push_back("OOO");
    }
    return moves;
}
vector<string> find_pawn_moves(bool color, Board position, int rank, int file, string last_move) {
    int player_move_direction = color ? -1 : 1;
    string current_pos_dig_not = to_string(file) + to_string(rank);
    vector<string> moves = {};
    int cache_file = file + player_move_direction;
    //Ходы вперед
    if (cache_file >= 8 or cache_file <= -1) return {};
    if (position[cache_file][rank] == 0) {
        if ((cache_file) % 7 == 0) {
            //Превращение пешек пока так
            moves.push_back(current_pos_dig_not + to_string(cache_file) + to_string(rank) + '1');
        }
        else {
            moves.push_back(current_pos_dig_not + to_string(cache_file) + to_string(rank));
            if (((file == 1 and !color) or (file == 6 and color)) and // до 3 полосы - два хода пешкой
                position[cache_file + player_move_direction][rank] == 0) {
                moves.push_back(current_pos_dig_not + to_string(file + 2 * player_move_direction) + to_string(rank));
            }
        }

    }
    //Взятие другие фигур
    if (rank + 1 <= 7 and
        ((position[cache_file][rank + 1] < 0 and color) or (not color and position[cache_file][rank + 1] > 0))) {
        if ((cache_file) % 7 == 0) {
            //Превращение пешек
            moves.push_back(current_pos_dig_not + to_string(cache_file) + to_string(rank + 1) + '#');
        }
        else
            moves.push_back(current_pos_dig_not + to_string(cache_file) + to_string(rank + 1));
    }
    if (rank - 1 >= 0 and
        ((position[cache_file][rank - 1] < 0 and color) or (not color and position[cache_file][rank - 1] > 0))) {
        if ((cache_file) % 7 == 0) {
            //Превращение пешек
            moves.push_back(current_pos_dig_not + to_string(cache_file) + to_string(rank - 1) + '#');
        }
        else
            moves.push_back(current_pos_dig_not + to_string(cache_file) + to_string(rank - 1));
    }
    if (last_move != "-" and //На той же высоте
        (4 - 1 * color) == (int)last_move[1] - 1 == file and //На сосеедней клетке
        false) {//abs(rank - last_move.get_to_int()[1]) == 1) :
        moves.push_back(current_pos_dig_not + to_string(cache_file) + to_string(rank + (last_move[1] - rank)));
    }
    return moves;
}
vector<string> find_chess_move(bool color, Board position, int rank, int file, pair<bool, bool> castling_data, string last_move) {
    int figure = position[file][rank];
    //своя фигура
    if (color and figure > 0 or not color and figure < 0) {
        switch (abs(figure))
        {
        case 6: return find_king_moves(color, position, rank, file, castling_data);
        case 5: return find_queen_moves(color, position, rank, file);
        case 4: return find_rock_moves(color, position, rank, file);
        case 3: return find_bishop_moves(color, position, rank, file);
        case 2: return find_knight_moves(color, position, rank, file);
        case 1: return find_pawn_moves(color, position, rank, file, last_move);

        default:
            break;
        }
    }
    return {};
}

GamePos from_fem(const char* fen_pos, size_t size) {
    //rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1 - начальная позиция
    Board position = { {0} };
    bool color;
    Castl_arr castling = { {false, false},{false, false} };
    string last_move = "-";

    int file = 0;
    int rank = 0;
    int i = 0;
    map<char, int> figures = { {'k', 6}, {'q', 5}, {'r', 4}, {'b', 3}, {'n', 2}, {'p', 1} };
    for (i = 0; i < size; i++) {
        char current_char = fen_pos[i];
        if (rank >= 8) {
            file++;
            rank = 0;
            if (file >= 8) break;
        }
        if (current_char == '/') {
            //Конец ряда
            continue;
        }
        else if (isdigit(current_char)) {
            int skip_i = atoi(&current_char);
            rank += skip_i;
        }
        else {
            position[file][rank] = isupper(current_char) ? figures[tolower(current_char)] : -figures[current_char];
            rank++;
        }

    }
    i++;
    //Пропускаем _ или ' '
    color = (fen_pos[i] == 'w') ? true : false;

    i += 2;
    if (fen_pos[i] == '-') {
        i++;
    }
    else {
        while (fen_pos[i] != ' ') {
            switch (fen_pos[i])
            {
            case 'k': {castling.second.first = true; break; }
            case 'K': {castling.first.first = true; break; }
            case 'Q': {castling.first.second = true; break; }
            case 'q': {castling.second.second = true; break; }
            default:
                break;
            }
            i++;
        }
    }
    i++;

    if (fen_pos[i] != '-') {
        last_move = fen_pos[i];
        i++;
        fen_pos += fen_pos[i];
    }


    return GamePos(position, castling, color, last_move);
}

GamePos make_move(GamePos current_pos, string move) {
    GamePos new_pos(current_pos);
    bool current_color = current_pos.color;
    //new_pos.color = !current_color;
    int size_of_move = move.length();
    // Ходы с превращением пешки
    if (size_of_move > 4) {
        pair<int, int> curr_pos = { move[0] - '0', move[1] - '0' };
        pair<int, int> next_pos = { move[2] - '0', move[3] - '0' };
        new_pos.position[next_pos.first][next_pos.second] = current_color ? atoi(&(move[4])) : -atoi(&(move[4]));
        new_pos.position[curr_pos.first][curr_pos.second] = 0;
    }
    // Обычные ходы "2233"
    else if (size_of_move > 3) {
        pair<int, int> curr_pos = { move[0] - '0', move[1] - '0' };
        pair<int, int> next_pos = { move[2] - '0', move[3] - '0' };
        int figure = new_pos.position[curr_pos.first][curr_pos.second];
        new_pos.position[next_pos.first][next_pos.second] = figure;
        new_pos.position[curr_pos.first][curr_pos.second] = 0;
        //Убираем возможность рокировки, при движении короля
        if (abs(figure) == KING) {
            if (figure > 0) { new_pos.castling.first = { false, false }; }
            else { new_pos.castling.second = { false, false }; }
        }
        if (abs(figure) == ROCK) {
            // Движение Ладьи справа(сбивает короткую рокировку)
            if (curr_pos.second == 7 and ((curr_pos.first == 7 and current_color) or (!current_color and curr_pos.first == 0)))
                if (figure > 0) { new_pos.castling.first.first = false; }
                else { new_pos.castling.second.first = false; }
            else if (curr_pos.second == 0 and ((curr_pos.first == 7 and current_color) or (!current_color and curr_pos.first == 0))) {// Движение Ладьи cлева(сбивает длинную рокировку)
                if (figure > 0) { new_pos.castling.first.second = false; }
                else { new_pos.castling.second.second = false; }
            }
        }
        /*
        if (last_move != None and
            last_move.get_allow_aisle() and
            figure[1] == 'P' and
            global_position[next_position_figure[0]][next_position_figure[1]] == None and
            current_position_figure[1] != next_position_figure[1]) :
            cache = last_move.get_to_int()
            position[cache[0]][cache[1]] = None*/
    }
    //Длинная рокировка "ooo"
    else if (size_of_move > 2) {
        int king_file = current_color ? 7 : 0;
        new_pos.position[king_file][2] = current_pos.position[king_file][4];
        new_pos.position[king_file][4] = 0;
        new_pos.position[king_file][3] = current_pos.position[king_file][7];
        new_pos.position[king_file][0] = 0;
        if (current_color) { new_pos.castling.first = { false, false }; }
        else { new_pos.castling.second = { false, false }; }
    }
    //Короткая рокировка "00"
    else {
        int king_file = current_color ? 7 : 0;
        new_pos.position[king_file][4] = 0;
        new_pos.position[king_file][6] = current_pos.position[king_file][4];
        new_pos.position[king_file][5] = current_pos.position[king_file][7];
        new_pos.position[king_file][7] = 0;
        if (current_color) { new_pos.castling.first = { false, false }; }
        else { new_pos.castling.second = { false, false }; }
    }
    return new_pos;
}

bool check_shah(GamePos pos) {
    pair<int, int> king_pos = { 0,0 };
    bool flag_king = false;
    for (int file = 0; file < 8; file++) {
        for (int rank = 0; rank < 8; rank++) {
            if ((pos.color and pos.position[file][rank] == 6) or (!pos.color and pos.position[file][rank] == -6)) {
                king_pos.first = file;
                king_pos.second = rank;
                flag_king = true;
                break;
            }
        }
        if (flag_king)
            break;
    }
    //Ищем пешки
    int pawn_direction = 1 - 2 * pos.color;
    for (int i = -1; i < 2; i += 2) {
        pair<int, int> figure_posit = { king_pos.first + pawn_direction, king_pos.second + i };
        if (0 <= figure_posit.first and figure_posit.first <= 7 and 0 <= figure_posit.second and figure_posit.second <= 7) {
            if (is_enemy(pos.position[figure_posit.first][figure_posit.second], PAWN, !pos.color)) {
                return false;
            }
        }
    }
    //Ищем слона или фирзя
    vector<pair<int, int>>default_bishop_moves = { {-1, 1} ,{1, 1},{1, -1},{-1, -1} };
    for (int i = 0; i < default_bishop_moves.size(); i++) {
        pair<int, int> current_pair = default_bishop_moves[i];
        for (int j = 1; j < 8; j++) {
            int cache_file = king_pos.first + current_pair.first * j;
            int cache_rank = king_pos.second + current_pair.second * j;
            if (0 <= cache_file and cache_file <= 7 and 0 <= cache_rank and cache_rank <= 7) {
                int figure_pos = pos.position[cache_file][cache_rank];
                //Вражеские фигуры
                if (is_enemy(figure_pos, BISHOP, !pos.color) or is_enemy(figure_pos, QUEEN, !pos.color))
                    return false;
                else if (figure_pos == 0)
                    continue;
                else
                    break;
            }
            else break;
        }
    }
    //Ищем ладьи или фирзя
    vector<pair<int, int>>default_rock_moves = { {-1, 0} ,{1, 0},{0, -1},{0, 1} };
    for (int i = 0; i < default_rock_moves.size(); i++) {
        pair<int, int> current_pair = default_rock_moves[i];
        for (int j = 1; j < 8; j++) {
            int cache_file = king_pos.first + current_pair.first * j;
            int cache_rank = king_pos.second + current_pair.second * j;
            if (0 <= cache_file and cache_file <= 7 and 0 <= cache_rank and cache_rank <= 7) {
                int figure_pos = pos.position[cache_file][cache_rank];
                //Вражеские фигуры
                if (is_enemy(figure_pos, ROCK, !pos.color) or is_enemy(figure_pos, QUEEN, !pos.color))
                    return false;
                else if (figure_pos == 0)
                    continue;
                else
                    break;
            }
            else break;
        }
    }
    //Ищем коня
    vector<pair<int, int>>default_knight_moves = { {-2, -1} ,{-2, 1},{2, -1},{2, 1},{-1, -2},{1, -2},{-1, 2},{1, 2} };
    for (int i = 0; i < default_knight_moves.size(); i++) {
        pair<int, int> current_pair = default_knight_moves[i];
        int cache_file = king_pos.first + current_pair.first;
        int cache_rank = king_pos.second + current_pair.second;
        if ((0 <= cache_file and cache_file <= 7) and (0 <= cache_rank and cache_rank <= 7)) {
            int figure_pos = pos.position[cache_file][cache_rank];
            if (is_enemy(figure_pos, KNIGHT, !pos.color)) {
                return false;
            }
        }
    }
    //Ищем короля
    vector<pair<int, int>>default_king_moves = { {-1, -1} ,{-1, 0},{-1, 1},{0, -1},{0, 1},{1, -1},{1, 0},{1, -1} };
    for (int i = 0; i < default_king_moves.size(); i++) {
        pair<int, int> current_pair = default_king_moves[i];
        int cache_file = king_pos.first + current_pair.first;
        int cache_rank = king_pos.second + current_pair.second;
        if ((0 <= cache_file and cache_file <= 7) and (0 <= cache_rank and cache_rank <= 7)) {
            int figure_pos = pos.position[cache_file][cache_rank];
            if (is_enemy(figure_pos, KING, !pos.color)) {
                return false;
            }
        }
    }
    return true;

}
bool check_castling_shah(GamePos pos, string move) {
    GamePos new_pos(pos);
    if (!check_shah(new_pos)) { return false; }
    int king_file = (int)(7 - 7 * (not new_pos.color));
    bool long_castling = false;
    if (move == "OOO") { long_castling = true; }
    else if (move == "OO") { long_castling = false; }
    else
        throw "check_castling invalid targer";
    new_pos.position[king_file][5 - 2 * long_castling] = pos.position[king_file][4];
    new_pos.position[king_file][4] = 0;
    if (!check_shah(new_pos)) { return false; }
    new_pos.position[king_file][6 - 4 * long_castling] = new_pos.position[king_file][5 - 2 * long_castling];
    new_pos.position[king_file][5 - 2 * long_castling] = 0;
    if (!check_shah(new_pos)) { return false; }
    return true;

}


bool is_enemy(int cell_position, int figure, bool enemy_color) {
    //Белый
    if (enemy_color) {
        return (abs(cell_position) == figure and cell_position > 0);
    }
    else
        return (abs(cell_position) == figure and cell_position < 0);
}

CHESSDLL const  wchar_t* eval_c(const char * pm, int depth) {
    string arr = string(pm);//"rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR b - - 0 1"; 'rnbqkb1r/pppppppp/5n2/8/4P3/5N2/PPPP1PPP/RNBQKB1R b KQkq - 0 3'
    GamePos pos = from_fem(arr.c_str(), arr.size());
    string best_move = evaluate_root(pos, depth);
    cout << " best_move c: " << best_move << endl;
    std::wstring widestr = std::wstring(best_move.begin(), best_move.end());
    const wchar_t* widecstr = widestr.c_str();
    return widecstr;

}