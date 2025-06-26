#include <SDL2/SDL.h>
#include <emscripten.h>
#include <iostream>

const int SCREEN_WIDTH = 800;
const int SCREEN_HEIGHT = 600;

SDL_Window* window = nullptr;
SDL_Renderer* renderer = nullptr;

// 画面全体を四角形として扱う
SDL_Rect rect = {0, 0, SCREEN_WIDTH, SCREEN_HEIGHT}; // 画面全体
bool rect_clicked = false;

void render() {
    // 画面全体を塗りつぶし
    if (rect_clicked) {
        SDL_SetRenderDrawColor(renderer, 255, 0, 0, 255); // 赤色（クリック済み）
    } else {
        SDL_SetRenderDrawColor(renderer, 255, 165, 0, 255); // オレンジ色（通常）
    }
    SDL_RenderClear(renderer);
    
    // 中央に小さな白い点を描画（表示確認用）
    SDL_SetRenderDrawColor(renderer, 255, 255, 255, 255);
    SDL_Rect center_dot = {SCREEN_WIDTH/2 - 5, SCREEN_HEIGHT/2 - 5, 10, 10};
    SDL_RenderFillRect(renderer, &center_dot);
    
    SDL_RenderPresent(renderer);
}

void handle_click(int mouse_x, int mouse_y) {
    // 四角形の範囲内をクリックしたかチェック
    if (mouse_x >= rect.x && mouse_x <= rect.x + rect.w &&
        mouse_y >= rect.y && mouse_y <= rect.y + rect.h) {
        rect_clicked = !rect_clicked; // 状態を切り替え
        std::cout << "Rectangle clicked! New state: " << (rect_clicked ? "red" : "blue") << std::endl;
    }
}

void main_loop() {
    SDL_Event e;
    while (SDL_PollEvent(&e)) {
        if (e.type == SDL_QUIT) {
            emscripten_cancel_main_loop();
            return;
        } else if (e.type == SDL_MOUSEBUTTONDOWN) {
            handle_click(e.button.x, e.button.y);
        }
    }
    render();
}

int main() {
    if (SDL_Init(SDL_INIT_VIDEO) < 0) {
        std::cout << "SDL initialization failed: " << SDL_GetError() << std::endl;
        return 1;
    }
    
    window = SDL_CreateWindow(
        "Simple Click Test",
        SDL_WINDOWPOS_UNDEFINED,
        SDL_WINDOWPOS_UNDEFINED,
        SCREEN_WIDTH,
        SCREEN_HEIGHT,
        SDL_WINDOW_SHOWN
    );
    
    if (!window) {
        std::cout << "Window creation failed: " << SDL_GetError() << std::endl;
        SDL_Quit();
        return 1;
    }
    
    renderer = SDL_CreateRenderer(window, -1, SDL_RENDERER_ACCELERATED);
    if (!renderer) {
        std::cout << "Renderer creation failed: " << SDL_GetError() << std::endl;
        SDL_DestroyWindow(window);
        SDL_Quit();
        return 1;
    }
    
    std::cout << "Simple rectangle click test initialized" << std::endl;
    std::cout << "Click the blue rectangle to turn it red!" << std::endl;
    
    emscripten_set_main_loop(main_loop, 60, 1);
    
    SDL_DestroyRenderer(renderer);
    SDL_DestroyWindow(window);
    SDL_Quit();
    
    return 0;
}