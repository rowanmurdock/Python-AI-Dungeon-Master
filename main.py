from ui import build_ui
import sounds as sound

if __name__ == "__main__":
    app = build_ui()
    sound.start_bg_music()
    app.mainloop()
