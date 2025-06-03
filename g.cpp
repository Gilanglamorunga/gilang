#include <iostream>
#include <vector>
#include <cstdlib>
#include <ctime>
#include <conio.h>   // untuk _kbhit() dan _getch() di Windows
#include <thread>
#include <chrono>

using namespace std;

const int WIDTH = 20;
const int HEIGHT = 10;

char map[HEIGHT][WIDTH];
int px = WIDTH / 2, py = HEIGHT / 2; // Player
int ex, ey; // Enemy
int score = 0, lives = 3, level = 1;
int enemy_speed = 5;
int frame = 0;

vector<pair<int, int>> walls = {
    {5, 3}, {6, 3}, {7, 3}, {8, 3}, {9, 3},
    {3, 7}, {4, 7}, {5, 7}, {6, 7}, {7, 7}, {8, 7}, {9, 7}
};

void init() {
    srand(time(0));
    px = WIDTH / 2;
    py = HEIGHT / 2;
    ex = rand() % WIDTH;
    ey = rand() % HEIGHT;
}

bool isWall(int x, int y) {
    for (auto& w : walls)
        if (w.first == x && w.second == y)
            return true;
    return false;
}

void draw() {
    system("cls"); // untuk Windows, gunakan "clear" di Linux/Mac
    for (int y = 0; y < HEIGHT; y++) {
        for (int x = 0; x < WIDTH; x++) {
            if (x == px && y == py)
                cout << 'P';
            else if (x == ex && y == ey)
                cout << 'E';
            else if (isWall(x, y))
                cout << '#';
            else
                cout << '.';
        }
        cout << endl;
    }
    cout << "Score: " << score << " | Lives: " << lives << " | Level: " << level << endl;
}

void input() {
    if (_kbhit()) {
        char ch = _getch();
        int nx = px, ny = py;
        if (ch == 'w') ny--;
        else if (ch == 's') ny++;
        else if (ch == 'a') nx--;
        else if (ch == 'd') nx++;
        else if (ch == 'q') exit(0); // Quit

        // Batasi layar dan tembok
        if (nx >= 0 && nx < WIDTH && ny >= 0 && ny < HEIGHT && !isWall(nx, ny)) {
            px = nx;
            py = ny;
        }
    }
}

void update() {
    // Enemy moves every enemy_speed frames
    if (frame % enemy_speed == 0) {
        if (ex < px && !isWall(ex + 1, ey)) ex++;
        else if (ex > px && !isWall(ex - 1, ey)) ex--;
        if (ey < py && !isWall(ex, ey + 1)) ey++;
        else if (ey > py && !isWall(ex, ey - 1)) ey--;
    }

    // Collision
    if (px == ex && py == ey) {
        lives--;
        if (lives <= 0) {
            cout << "Game Over! Skor akhir: " << score << endl;
            exit(0);
        } else {
            px = WIDTH / 2; py = HEIGHT / 2;
            ex = rand() % WIDTH; ey = rand() % HEIGHT;
        }
    }

    // Skor dan level naik
    if (frame % 20 == 0) {
        score++;
        if (score % 10 == 0) {
            level++;
            if (enemy_speed > 1) enemy_speed--; // musuh jadi lebih cepat
        }
    }

    frame++;
}

int main() {
    init();
    while (true) {
        draw();
        input();
        update();
        this_thread::sleep_for(chrono::milliseconds(100)); // delay ~10 FPS
    }
}
