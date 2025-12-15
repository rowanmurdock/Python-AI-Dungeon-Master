from ui import build_main_menu
import sounds as sound

if __name__ == "__main__":
    app = build_main_menu()
    sound.start_bg_music()
    app.mainloop()
