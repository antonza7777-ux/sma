# -*- coding: utf-8 -*-
import json
import os
import sys

try:
    if sys.stdout.encoding != "utf-8":
        sys.stdout.reconfigure(encoding="utf-8")
    if sys.stdin.encoding != "utf-8":
        sys.stdin.reconfigure(encoding="utf-8")
except Exception:
    pass

# Импорт шаблонов — файл рядом
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
try:
    from templates import TEMPLATES, get_template_names, get_template
except Exception:
    TEMPLATES = {}
    def get_template_names(): return []
    def get_template(k): return None

APP_NAME = "spammesenges V3"
CONFIGS_DIR = os.path.dirname(os.path.abspath(__file__))

DEFAULT_CONFIG = {
    "message": "/cc Привет мир",
    "delay": 0.01,
    "hotkey": "right ctrl",
    "protected_words": ["/cc", "/setwarp", "/warp", "/msg", "/tell", "/r"],
    "space_after_protected": True,
    "avoid_repeats": True,
    "history_size": 50,
    "max_generation_attempts": 20,
    "translit_mode": "mix",
    "translit_chance": 0.4,
    "replace_spaces_with_digits": True,
    "digits_min": 1,
    "digits_max": 3,
    "insert_between_letters": True,
    "emoji_mode": "mixed",
    "emoji_chance": 0.5,
    "emoji_list": [
        "💀", "🤬", "😭", "🧑‍🦼", "🧑‍🦼‍➡️", "🔥", "💩", "🤡", "👽",
        "🤖", "👾", "🎃", "😈", "☠️", "🖕", "🍆", "🎉", "✨", "⭐", "💯",
    ],
    "random_symbols": ["_", ".", "-", "!", "?", "*", "#", "~", "^", "+"],
    "insert_chance": 0.3,
    "symbols_min": 1,
    "symbols_max": 2,
    "randomize_case": False,
    "absolute_random": False,
    "absolute_tail": False,
    "absolute_tail_min": 8,
    "absolute_tail_max": 20,
}


def preset_path(name):
    return os.path.join(CONFIGS_DIR, f"{name}.json")


def load(name):
    p = preset_path(name)
    if not os.path.exists(p):
        save(name, DEFAULT_CONFIG)
        return DEFAULT_CONFIG.copy()
    try:
        with open(p, "r", encoding="utf-8") as f:
            cfg = json.load(f)
        for k, v in DEFAULT_CONFIG.items():
            cfg.setdefault(k, v)
        return cfg
    except Exception as e:
        print(f"[ОШИБКА] Не удалось прочитать {name}.json: {e}")
        return DEFAULT_CONFIG.copy()


def save(name, cfg):
    with open(preset_path(name), "w", encoding="utf-8") as f:
        json.dump(cfg, f, ensure_ascii=False, indent=2)


def clear():
    os.system("cls" if os.name == "nt" else "clear")


def pause():
    input("\n  Enter чтобы продолжить...")


def choose_preset():
    while True:
        clear()
        print("-----------------------------------------")
        print(f"Выбор настройки |{APP_NAME}|")
        print("-----------------------------------------")
        print()
        for i in range(1, 11):
            print(f"{i}. ALT{i}")
        print()
        print("0. Выход")
        print()
        choice = input("  Выбери пресет: ").strip()
        if choice == "0":
            return None
        if choice.isdigit() and 1 <= int(choice) <= 10:
            return f"alt{int(choice)}"
        print("  [!] Неверный выбор.")
        pause()


def apply_template(name, cfg):
    """Показывает список шаблонов и применяет выбранный."""
    clear()
    print("=" * 60)
    print(f"   ШАБЛОНЫ (пресет {name.upper()})")
    print("=" * 60)
    print()
    keys = get_template_names()
    for i, k in enumerate(keys, 1):
        t = TEMPLATES[k]
        print(f"  {i}. {t['name']}")
        print(f"     {t['desc']}")
        print()
    print("  0. Назад (не применять)")
    print()
    choice = input("  Выбери шаблон: ").strip()
    if choice == "0" or not choice.isdigit():
        return cfg
    idx = int(choice)
    if 1 <= idx <= len(keys):
        key = keys[idx - 1]
        t = get_template(key)
        if t:
            for k, v in t["settings"].items():
                cfg[k] = v
            save(name, cfg)
            print(f"\n  [OK] Применён шаблон: {t['name']}")
            pause()
    return cfg


def menu(name, cfg):
    while True:
        clear()
        print("=" * 60)
        print(f"   {APP_NAME} - НАСТРОЙКИ  |  Пресет: {name.upper()}")
        print("=" * 60)
        print()
        print(f"  [1] Сообщение:            {cfg['message']}")
        print(f"  [2] Задержка:             {cfg['delay']} сек")
        print(f"  [3] Защищённые слова:     {', '.join(cfg['protected_words'])}")
        print(f"  [4] Пробел после защиты:  {cfg['space_after_protected']}")
        print(f"  [5] Анти-повтор:          {cfg.get('avoid_repeats', True)}")
        print(f"      (история {cfg.get('history_size', 50)} сообщений)")
        print(f"  [6] Транслит:             {cfg.get('translit_mode', 'off')}")
        print(f"      (шанс замены {cfg.get('translit_chance', 0.4)})")
        print(f"  [7] Пробелы → цифры:      {cfg['replace_spaces_with_digits']}")
        print(f"      (диапазон цифр: {cfg['digits_min']}-{cfg['digits_max']})")
        print(f"  [8] Символы между букв:   {cfg['insert_between_letters']}")
        print(f"      (шанс {cfg['insert_chance']}, символов {cfg['symbols_min']}-{cfg['symbols_max']})")
        print(f"  [9] Набор символов:       {' '.join(cfg['random_symbols'])}")
        print(f"  [0] Рандом регистра:      {cfg['randomize_case']}")
        print()
        print(f"  [E] Эмодзи:               режим={cfg.get('emoji_mode', 'off')}, "
              f"шанс={cfg.get('emoji_chance', 0.5)}")
        print(f"      Список:               {' '.join(cfg.get('emoji_list', [])[:8])}"
              + (" ..." if len(cfg.get('emoji_list', [])) > 8 else ""))
        print()
        print(f"  [X] АБСОЛЮТНАЯ РАНДОМ.:   {cfg.get('absolute_random', False)}")
        print(f"  [Y] Рандом-хвост:         {cfg.get('absolute_tail', False)}")
        print(f"      (длина {cfg.get('absolute_tail_min', 8)}-{cfg.get('absolute_tail_max', 20)} симв.)")
        print()
        print("  [D] Диапазон цифр       [S] Диапазон символов")
        print("  [C] Шанс вставки        [H] Хоткей")
        print("  [R] Анти-повтор         [T] Транслит")
        print("  [L] Длина рандом-хвоста")
        print()
        print("  [M] ПРИМЕНИТЬ ШАБЛОН (7 пресетов)")
        print()
        print("  [B] Сменить пресет")
        print("  [P] Показать config.json")
        print("  [Q] Выход")
        print()
        choice = input("  Выбери пункт: ").strip().lower()

        if choice == "q":
            print("Пока!")
            break
        elif choice == "b":
            return "switch"
        elif choice == "m":
            cfg = apply_template(name, cfg)
        elif choice == "x":
            cfg["absolute_random"] = not cfg.get("absolute_random", False)
            save(name, cfg)
        elif choice == "y":
            cfg["absolute_tail"] = not cfg.get("absolute_tail", False)
            save(name, cfg)
        elif choice == "l":
            try:
                print(f"\n  Текущая длина хвоста: {cfg.get('absolute_tail_min', 8)}-{cfg.get('absolute_tail_max', 20)}")
                cfg["absolute_tail_min"] = int(input("  Мин. длина: "))
                cfg["absolute_tail_max"] = int(input("  Макс. длина: "))
                save(name, cfg)
            except ValueError:
                print("  [!] Нужны числа.")
                pause()
        elif choice == "0":
            cfg["randomize_case"] = not cfg["randomize_case"]
            save(name, cfg)
        elif choice == "1":
            print(f"\n  Текущее: {cfg['message']}")
            new = input("  Новое сообщение: ")
            if new.strip():
                cfg["message"] = new
                save(name, cfg)
        elif choice == "2":
            print(f"\n  Текущая: {cfg['delay']}")
            try:
                cfg["delay"] = float(input("  Новая (сек): ").replace(",", "."))
                save(name, cfg)
            except ValueError:
                print("  [!] Нужно число.")
                pause()
        elif choice == "3":
            print(f"\n  Текущие: {', '.join(cfg['protected_words'])}")
            new = input("  Новые (через запятую): ")
            if new.strip():
                cfg["protected_words"] = [x.strip() for x in new.split(",") if x.strip()]
                save(name, cfg)
        elif choice == "4":
            cfg["space_after_protected"] = not cfg["space_after_protected"]
            save(name, cfg)
        elif choice == "5":
            cfg["avoid_repeats"] = not cfg.get("avoid_repeats", True)
            save(name, cfg)
        elif choice == "6":
            order = ["off", "ru_to_en", "en_to_ru", "mix"]
            cur = cfg.get("translit_mode", "off")
            idx = order.index(cur) if cur in order else 0
            cfg["translit_mode"] = order[(idx + 1) % len(order)]
            save(name, cfg)
        elif choice == "7":
            cfg["replace_spaces_with_digits"] = not cfg["replace_spaces_with_digits"]
            save(name, cfg)
        elif choice == "8":
            cfg["insert_between_letters"] = not cfg["insert_between_letters"]
            save(name, cfg)
        elif choice == "9":
            print(f"\n  Текущие: {' '.join(cfg['random_symbols'])}")
            new = input("  Новые (подряд без пробелов): ")
            if new.strip():
                cfg["random_symbols"] = list(new.replace(" ", ""))
                save(name, cfg)
        elif choice == "e":
            print("\n  === ЭМОДЗИ ===")
            print("  Режимы: off / emoji / mixed")
            print(f"  Текущий: {cfg.get('emoji_mode', 'off')}")
            nm = input("  Новый режим: ").strip().lower()
            if nm in ("off", "emoji", "mixed"):
                cfg["emoji_mode"] = nm
            try:
                print(f"\n  Текущий шанс: {cfg.get('emoji_chance', 0.5)}")
                v = float(input("  Шанс (0.0-1.0): ").replace(",", "."))
                cfg["emoji_chance"] = v
            except ValueError:
                pass
            print(f"\n  Текущий список ({len(cfg.get('emoji_list', []))}):")
            print("  " + " ".join(cfg.get("emoji_list", [])))
            new_em = input("\n  Новые (через запятую, Enter — оставить): ").strip()
            if new_em:
                items = [x.strip() for x in new_em.split(",") if x.strip()]
                if items:
                    cfg["emoji_list"] = items
            save(name, cfg)
        elif choice == "d":
            try:
                cfg["digits_min"] = int(input("  Мин. цифр: "))
                cfg["digits_max"] = int(input("  Макс. цифр: "))
                save(name, cfg)
            except ValueError:
                print("  [!] Нужны числа.")
                pause()
        elif choice == "s":
            try:
                cfg["symbols_min"] = int(input("  Мин. символов: "))
                cfg["symbols_max"] = int(input("  Макс. символов: "))
                save(name, cfg)
            except ValueError:
                print("  [!] Нужны числа.")
                pause()
        elif choice == "c":
            try:
                v = float(input("  Шанс вставки (0.0-1.0): ").replace(",", "."))
                cfg["insert_chance"] = v
                save(name, cfg)
            except ValueError:
                print("  [!] Нужно число.")
                pause()
        elif choice == "h":
            new = input(f"  Новый хоткей (текущий {cfg['hotkey']}): ").strip()
            if new:
                cfg["hotkey"] = new
                save(name, cfg)
        elif choice == "r":
            try:
                cfg["history_size"] = int(input("  Размер истории: "))
                cfg["max_generation_attempts"] = int(input("  Макс. попыток: "))
                save(name, cfg)
            except ValueError:
                print("  [!] Нужны числа.")
                pause()
        elif choice == "t":
            print("\n  === ТРАНСЛИТ ===")
            print("  off / ru_to_en / en_to_ru / mix")
            print(f"  Текущий: {cfg.get('translit_mode', 'off')}")
            nm = input("  Новый режим: ").strip().lower()
            if nm in ("off", "ru_to_en", "en_to_ru", "mix"):
                cfg["translit_mode"] = nm
            try:
                print(f"\n  Текущий шанс: {cfg.get('translit_chance', 0.4)}")
                v = float(input("  Шанс (0.0-1.0): ").replace(",", "."))
                cfg["translit_chance"] = v
            except ValueError:
                pass
            save(name, cfg)
        elif choice == "p":
            clear()
            print("=" * 60)
            print(f"   {name}.json")
            print("=" * 60)
            with open(preset_path(name), "r", encoding="utf-8") as f:
                print(f.read())
            pause()


def main():
    while True:
        preset = choose_preset()
        if preset is None:
            print("Пока!")
            break
        cfg = load(preset)
        result = menu(preset, cfg)
        if result == "switch":
            continue
        else:
            break


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nПока!")