#include <stdio.h>
#include <stdbool.h>
#include <windows.h>

void pressKey(WORD key, bool press) {
    INPUT input = {0};
    input.type = INPUT_KEYBOARD;
    input.ki.wVk = key;
    if (press) {
        SendInput(1, &input, sizeof(INPUT));
    } else {
        input.ki.dwFlags = KEYEVENTF_KEYUP;
        SendInput(1, &input, sizeof(INPUT));
    }
}

int main() {
    bool running = false;
    bool ctrlPressed = false;
    bool f12Pressed = false;

    printf("Pressione Ctrl + F12 para ligar/desligar o script.\n");

    while (true) {
        if ((GetAsyncKeyState(VK_CONTROL) & 0x8000) && (GetAsyncKeyState(VK_F12) & 0x8000)) {
            if (!ctrlPressed && !f12Pressed) {
                running = !running;
                if (running) {
                    printf("Script ativado.\n");
                } else {
                    printf("Script desativado.\n");
                }
            }
            ctrlPressed = true;
            f12Pressed = true;
        } else {
            ctrlPressed = false;
            f12Pressed = false;
        }

        if (running) {
            if ((GetAsyncKeyState('W') & 0x8000)) {
                pressKey('W', true);
            } else {
                pressKey('W', false);
            }

            if ((GetAsyncKeyState('S') & 0x8000)) {
                pressKey('S', true);
            } else {
                pressKey('S', false);
            }

            if ((GetAsyncKeyState('A') & 0x8000)) {
                pressKey('A', true);
            } else {
                pressKey('A', false);
            }

            if ((GetAsyncKeyState('D') & 0x8000)) {
                pressKey('D', true);
            } else {
                pressKey('D', false);
            }
        }

        Sleep(1);
    }

    return 0;
}
