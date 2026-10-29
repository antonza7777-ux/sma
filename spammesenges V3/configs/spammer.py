# ============================================
# spammesenges V3
# ============================================
# Hotkey: Right Ctrl — start/stop
# Exit: Esc
# Запускается через ALT*.bat, конфиг берётся из <altN>.json
# ============================================

import os
import sys
import json
import time
import random
import threading
from collections import deque
import keyboard
import pyperclip
import pyautogui

try:
    if sys.stdout.encoding != "utf-8":
        sys.stdout.reconfigure(encoding="utf-8")
    if sys.stderr.encoding != "utf-8":
        sys.stderr.reconfigure(encoding="utf-8")
except Exception:
    pass

APP_NAME = "spammesenges V3"
CONFIGS_DIR = os.path.dirname(os.path.abspath(__file__))


def _resolve_config_path():
    preset = None
    if len(sys.argv) > 1:
        preset = sys.argv[1].strip().lower()
    if not preset:
        preset = os.environ.get("SPAM_PRESET", "").strip().lower()
    if not preset:
        preset = "alt1"
    if preset.endswith(".json"):
        preset = preset[:-5]
    return preset, os.path.join(CONFIGS_DIR, f"{preset}.json")


PRESET_NAME, CONFIG_FILE = _resolve_config_path()


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


# ============================================================
# ТРАНСЛИТ
# ============================================================

RU_TO_LATIN = {
    "а": ["a"], "б": ["b"], "в": ["v", "b"], "г": ["g"], "д": ["d"],
    "е": ["e"], "ё": ["e"], "ж": ["jh", "zh"], "з": ["z", "3"],
    "и": ["i", "u"], "й": ["i", "y"], "к": ["k"], "л": ["l"],
    "м": ["m"], "н": ["n", "h"], "о": ["o"], "п": ["p"],
    "р": ["r", "p"], "с": ["s", "c"], "т": ["t"], "у": ["y", "u"],
    "ф": ["f"], "х": ["x"], "ц": ["ce", "c"], "ч": ["ch"],
    "ш": ["sh", "w"], "щ": ["sh"], "ы": ["ie", "bi"], "э": ["e"],
    "ю": ["y", "io"], "я": ["y", "ya"],
}

LATIN_TO_RU = {
    "a": ["а"], "b": ["в", "ь"], "c": ["с"], "d": ["д"],
    "e": ["е", "ё"], "f": ["ф"], "g": ["г"], "h": ["н"],
    "i": ["и", "й"], "j": ["ж"], "k": ["к"], "l": ["л"],
    "m": ["м"], "n": ["п"], "o": ["о"], "p": ["р"],
    "q": ["q"], "r": ["г"], "s": ["с"], "t": ["т"],
    "u": ["и", "у"], "v": ["в"], "w": ["ш"], "x": ["х"],
    "y": ["у"], "z": ["з"],
}

ES_LOOKALIKE = {
    "a": ["á", "à"], "e": ["é", "è"], "i": ["í", "ì"],
    "o": ["ó", "ò"], "u": ["ú", "ù", "ü"], "n": ["ñ"], "c": ["ç"],
}


# ============================================================
# ЭКЗОТИЧЕСКИЕ СИМВОЛЫ (для absolute_random / absolute_tail)
# ============================================================

GREEK = "αβγδεζηθικλμνξοπρστυφχψωΑΒΓΔΕΖΗΘΙΚΛΜΝΞΟΠΡΣΤΥΦΧΨΩ"
ARABIC = "ابتثجحخدذرزسشصضطظعغفقكلمنهوي"
CHINESE = "的一是不了在人有我他这个们中来上大为和国地到以说时要就出会可也你对生能而子那得于着下自之年过发后作里用道行所然家种事成方多经么去法学如都同现当没动面起看定天分还进好小部其些主样理心她本前开但因只从想实日军者意无力它与长把机十民第公此已工使情明性知全三又关点正业外将两高间由问很最重并物手应战向头文体政美相见被利什二等产或新己制身果加西斯月话合回特代内信表化老给世位次度门任常先海通教儿原东声提立及比员解水名真论处走义各入几口认条平系气题活尔更别打女变四神总何电数安少报才结反受目太量再感建务做接必场件计管期市直德资命山金指克许统区保至队形社便空决治展马科司五基眼书非则听白却界达光放强即像难且权思王象完设式色路记南品住告类求据程北边死张该交规万取拉格望觉术领共确传师观清今切院让识候带导争运笑飞风步改收根干造言联持组每济车亲极林服快办议往元英士证近失转夫令准布始怎呢存未远叫台单影具罗字爱击流备兵连调深商算质团集百需价花党华城石级整府离况亚请技际约示复病息究线似官火断精满支视消越器容照须九增研写称企八功吗包片史委乎查轻易早曾除农找装广显吧阿李标谈吃图念六引历首医局突专费号尽另周较注语仅考落青随选列武红响虽推势参希古众构房半节土投某案黑维革划敌致陈律足态护七兴派孩验责营星够章音跟志底站严巴例防族供效续施留讲型料终答紧黄绝奇察母京段依批群项故按河米围江织害斗双境客纪采举杀攻父苏密低朝友诉止细愿千值仍男钱破网热助倒育属坐帝限船脸职速刻乐否刚威毛状率甚独球般普怕弹校苦创假久错承印晚兰试股拿脑预谁益阳若哪微尼继送急血惊伤素药适波夜省初喜卫源食险待述陆习置居劳财环排福纳欢雷警获模充负云停木游龙树疑层冷洲冲射略范竟句室异激汉村哈策演简卡罪判担州静退既衣您宗积余痛检差富灵协角占配征修皮挥胜降阶审沉坚善妈刘读啊超免压银买皇养伊怀执副乱抗犯追帮宣佛岁航优怪香著田铁控税左右份穿艺背阵草脚概恶块顿敢守酒岛托央户烈洋哥索胡款靠评版宝座释景顾弟登货互付伯慢欧换闻危忙核暗姐介坏讨丽良序升监临亮露永呼味野架域沙掉括舰鱼杂误湾吉减编楚肯测败屋跑梦散温困剑渐封救贵枪缺楼县尚毫移娘朋画班智亦耳恩短掌恐遗固席松秘谢鲁遇康虑幸均销钟诗藏赶剧票损忽巨炮旧端探湖录叶春乡附吸予礼港雨呀板庭妇归睛饭额含顺输摇招婚脱补谓督毒油疗旅泽材灭逐莫笔亡鲜词圣择寻厂睡博勒烟授诺伦岸奥唐卖俄炸载洛健堂旁宫喝借君禁阴园谋宋避抓荣姑孙逃牙束跳顶玉镇雪午练迫爷篇肉嘴馆遍凡础洞卷坦牛宁纸诸训私庄祖丝翻暴森塔默握戏隐熟骨访弱蒙歌店鬼软典欲萨伙遭盘爸扩盖弄雄稳忘亿刺拥徒姆杨齐赛趣曲刀床迎冰虚玩析窗醒妻透购替塞努休虎扬途侵刑绿兄迅套贸毕唯谷轮库迹尤竞街促延震弃甲伟麻川申缓潜闪售灯针哲络抵朱埃抱鼓植纯夏忍页杰筑折郑贝尊吴秀混臣雅振染盛怒舞圆搞狂措姓残秋培迷诚宽宇猛摆梅毁伸摩盟末乃悲拍丁赵硬麦蒋操耶阻订彩抽赞魔纷沿喊违妹浪汇币丰蓝殊献桌啦瓦莱援译夺汽烧烟肚炸郑忽劝零填汁岗暗姐介坏讨丽良序升监临亮露永呼味野架域沙掉括舰鱼杂误湾吉减编楚肯测败屋跑梦散温困剑渐封救贵枪缺楼县尚毫移娘朋画班智亦耳恩短掌恐遗固席松秘谢鲁遇康虑幸均销钟诗藏赶剧票损忽巨炮旧端探湖录叶春乡附吸予礼港雨呀板庭妇归睛饭额含顺输摇招婚脱补谓督毒油疗旅泽材灭逐莫笔亡鲜词圣择寻厂睡博勒烟授诺伦岸奥唐卖俄炸载洛健堂旁宫喝借君禁阴园谋宋避抓荣姑孙逃牙束跳顶玉镇雪午练迫爷篇肉嘴馆遍凡础洞卷坦牛宁纸诸训私庄祖丝翻暴森塔默握戏隐熟骨访弱蒙歌店鬼软典欲萨伙遭盘爸扩盖弄雄稳忘亿刺拥徒姆杨齐赛趣曲刀床迎冰虚玩析窗醒妻透购替塞努休虎扬途侵刑绿兄迅套贸毕唯谷轮库迹尤竞街促延震弃甲伟麻川申缓潜闪售灯针哲络抵朱埃抱鼓植纯夏忍页杰筑折郑贝尊吴秀混臣雅振染盛怒舞圆搞狂措姓残秋培迷诚宽宇猛摆梅毁伸摩盟末乃悲拍丁赵硬麦蒋操耶阻订彩抽赞魔纷沿喊违妹浪汇币丰蓝殊献桌啦瓦莱援译夺汽烧烟肚炸郑忽劝零填汁岗暗"

JAPANESE = "あいうえおかきくけこさしすせそたちつてとなにぬねのはひふへほまみむめもやゆよらりるれろわをんアイウエオカキクケコサシスセソタチツテトナニヌネノハヒフヘホマミムメモヤユヨラリルレロワヲン"
KOREAN = "가나다라마바사아자차카타파하거너더러머버서어저처커터퍼허고노도로모보소오조초코토포호구누두루무부수우주추쿠투푸후"
HEBREW = "אבגדהוזחטיכלמנסעפצקרשת"
THAI = "กขฃคฅฆงจฉชซฌญฎฏฐฑฒณดตถทธนบปผฝพฟภมยรลวศษสหฬอฮ"
DEVANAGARI = "अआइईउऊऋएऐओऔकखगघङचछजझञटठडढणतथदधनपफबभमयरलवशषसह"
GEORGIAN = "აბგდევზთიკლმნოპჟრსტუფქღყშჩცძწჭხჯჰ"
ARMENIAN = "աբգդեզէըթժիլխծկհձղճմյնշոչպջռսվտրցուփքօֆ"

WEIRD_SYMBOLS = (
    "†‡§¶©®™°±×÷≠≤≥∞∑∏∫√∛∜∝∟∠∡∢∣∤∥∦∧∨∩∪∴∵∶∷∸∹∺∻∼∽∾∿"
    "←↑→↓↔↕↖↗↘↙↚↛↜↝↞↟↠↡↢↣↤↥↦↧↨↩↪↫↬↭↮↯"
    "♠♣♥♦♤♧♡♢★☆✦✧✩✪✫✬✭✮✯✰"
    "ᚠᚡᚢᚣᚤᚥᚦᚧᚨᚩᚪᚫᚬᚭᚮᚯᚰᚱᚲᚳᚴᚵᚶᚷᚸᚹᚺᚻᚼᚽᚾᚿᛀᛁᛂᛃᛄᛅᛆᛇᛈᛉᛊᛋᛌᛍᛎᛏᛐᛑᛒᛓᛔᛕᛖᛗᛘᛙᛚᛛᛜᛝᛞᛟ"
    "☀☁☂☃☄★☆☇☈☉☊☋☌☍☎☏☐☑☒☓☔☕☖☗☘☙☚☛☜☝☞☟☠☡☢☣☤☥☦☧☨☩☪☫☬☭☮☯"
    "⚀⚁⚂⚃⚄⚅⚆⚇⚈⚉⚊⚋⚌⚍⚎⚏⚐⚑⚒⚓⚔⚕⚖⚗⚘⚙⚚⚛⚜⚝⚞⚟"
    "♔♕♖♗♘♙♚♛♜♝♞♟♠♡♢♣♤♥♦♧♨♩♪♫♬♭♮♯"
)

ACCENTED_LATIN = "àáâãäåāăąçćĉċčèéêëēĕėęěìíîïĩīĭįıðñńņňòóôõöøōŏőùúûüũūŭůűųýÿŷżźž"

ALL_EXOTIC = (
    GREEK + ARABIC + CHINESE + JAPANESE + KOREAN + WEIRD_SYMBOLS
    + ACCENTED_LATIN + HEBREW + THAI + DEVANAGARI + GEORGIAN + ARMENIAN
)


# ============================================================
# ЗАГРУЗКА КОНФИГА
# ============================================================

def load_config():
    if not os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, "w", encoding="utf-8") as f:
            json.dump(DEFAULT_CONFIG, f, ensure_ascii=False, indent=2)
        print(f"[INFO] Создан {os.path.basename(CONFIG_FILE)} с настройками по умолчанию.")
        return DEFAULT_CONFIG.copy()
    try:
        with open(CONFIG_FILE, "r", encoding="utf-8") as f:
            cfg = json.load(f)
        for k, v in DEFAULT_CONFIG.items():
            cfg.setdefault(k, v)
        return cfg
    except Exception as e:
        print(f"[ERROR] Не удалось прочитать {os.path.basename(CONFIG_FILE)}: {e}")
        return DEFAULT_CONFIG.copy()


CFG = load_config()
pyautogui.PAUSE = 0
spamming = False
spam_thread = None
_history = deque(maxlen=CFG.get("history_size", 50))


# ============================================================
# ТРАНСЛИТ
# ============================================================

def _translit_ru_to_en(ch):
    v = RU_TO_LATIN.get(ch.lower())
    if not v:
        return ch
    pick = random.choice(v)
    return pick.capitalize() if ch.isupper() else pick


def _translit_en_to_ru(ch):
    v = LATIN_TO_RU.get(ch.lower())
    if not v:
        return ch
    pick = random.choice(v)
    return pick.upper() if ch.isupper() else pick


def _translit_to_es(ch):
    v = ES_LOOKALIKE.get(ch.lower())
    if not v:
        return ch
    pick = random.choice(v)
    return pick.upper() if ch.isupper() else pick


def _maybe_translit(ch):
    mode = CFG.get("translit_mode", "off")
    if mode == "off" or not ch.isalpha():
        return ch
    if random.random() > CFG.get("translit_chance", 0.4):
        return ch
    if ch.isascii():
        if mode == "en_to_ru":
            return _translit_en_to_ru(ch)
        elif mode == "mix":
            return _translit_en_to_ru(ch) if random.random() < 0.5 else _translit_to_es(ch)
        return ch
    else:
        if mode in ("ru_to_en", "mix"):
            return _translit_ru_to_en(ch)
        return ch


# ============================================================
# РАНДОМИЗАЦИЯ
# ============================================================

def _random_digits():
    n = random.randint(CFG["digits_min"], CFG["digits_max"])
    return "".join(random.choice("0123456789") for _ in range(n))


def _random_symbols():
    n = random.randint(CFG["symbols_min"], CFG["symbols_max"])
    emoji_mode = CFG.get("emoji_mode", "off")
    emoji_chance = CFG.get("emoji_chance", 0.5)
    emoji_list = CFG.get("emoji_list", [])
    symbols_list = CFG.get("random_symbols", [])
    out = []
    for _ in range(n):
        use_emoji = False
        if emoji_mode == "emoji":
            use_emoji = True
        elif emoji_mode == "mixed":
            use_emoji = random.random() < emoji_chance
        if use_emoji and emoji_list:
            out.append(random.choice(emoji_list))
        elif symbols_list:
            out.append(random.choice(symbols_list))
        elif emoji_list:
            out.append(random.choice(emoji_list))
    return "".join(out)


def _absolute_randomize_char(ch, used):
    """Возвращает случайный экзотический символ, не пересекающийся с used."""
    pool = ALL_EXOTIC
    for _ in range(50):
        cand = random.choice(pool)
        if cand not in used:
            return cand
    return random.choice(pool)


def _absolute_randomize_segment(segment):
    """Полная рандомизация сегмента — ни один символ не повторяется."""
    used = set()
    out = []
    for ch in segment:
        # пробелы не считаются "символами" — просто вставляем разделитель
        if ch == " ":
            out.append(" ")
            continue
        c = _absolute_randomize_char(ch, used)
        used.add(c)
        out.append(c)

        # между символами вставляем доп. символы
        if random.random() < CFG.get("insert_chance", 0.5):
            extra_n = random.randint(CFG.get("symbols_min", 1), CFG.get("symbols_max", 3))
            for _ in range(extra_n):
                e = _absolute_randomize_char(ch, used)
                used.add(e)
                out.append(e)
    return "".join(out)


def _generate_absolute_tail():
    """Генерирует случайный хвост после защищённого слова."""
    lo = CFG.get("absolute_tail_min", 8)
    hi = CFG.get("absolute_tail_max", 20)
    length = random.randint(lo, hi)
    used = set()
    out = []
    for _ in range(length):
        # изредка вставляем пробел
        if random.random() < 0.15:
            out.append(" ")
            continue
        c = _absolute_randomize_char("", used)
        used.add(c)
        out.append(c)
    return "".join(out)


def _randomize_segment(segment):
    if not segment:
        return segment

    absolute = CFG.get("absolute_random", False)

    if absolute:
        return _absolute_randomize_segment(segment)

    # ===== обычный режим =====
    if CFG.get("translit_mode", "off") != "off":
        segment = "".join(_maybe_translit(ch) for ch in segment)

    if CFG["replace_spaces_with_digits"]:
        segment = "".join(_random_digits() if ch == " " else ch for ch in segment)

    if CFG["insert_between_letters"]:
        buf = []
        for i, ch in enumerate(segment):
            if CFG["randomize_case"] and ch.isalpha():
                buf.append(ch.upper() if random.random() < 0.5 else ch.lower())
            else:
                buf.append(ch)
            if i < len(segment) - 1 and ch.isalpha() and segment[i + 1].isalpha():
                if random.random() < CFG["insert_chance"]:
                    buf.append(_random_symbols())
        segment = "".join(buf)
    elif CFG["randomize_case"]:
        segment = "".join(
            (c.upper() if random.random() < 0.5 else c.lower()) if c.isalpha() else c
            for c in segment
        )
    return segment


def _is_protected_at(text, i, protected_sorted):
    for word in protected_sorted:
        if text[i:i + len(word)].lower() == word.lower():
            if i == 0 or text[i - 1] in " \t":
                after = i + len(word)
                if after == len(text) or not text[after].isalnum():
                    return word
    return None


def randomize_message(text):
    protected = CFG.get("protected_words", [])
    absolute = CFG.get("absolute_random", False)
    absolute_tail = CFG.get("absolute_tail", False)

    if not protected:
        # если нет защищённых — просто рандомизируем всё,
        # но при absolute_tail дописываем сгенерированный хвост
        base = _randomize_segment(text) if text else ""
        if absolute_tail:
            sep = " " if base else ""
            return base + sep + _generate_absolute_tail()
        return base

    protected_sorted = sorted(protected, key=len, reverse=True)
    result = []
    i, n = 0, len(text)
    last_was_protected_end = False

    while i < n:
        matched = _is_protected_at(text, i, protected_sorted)
        if matched:
            result.append(text[i:i + len(matched)])
            i += len(matched)
            last_was_protected_end = True

            if i < n and text[i] == " ":
                result.append(" ")
                i += 1
            elif CFG.get("space_after_protected", True) and i < n:
                result.append(" ")
        else:
            j = i
            while j < n:
                if _is_protected_at(text, j, protected_sorted):
                    break
                j += 1
            result.append(_randomize_segment(text[i:j]))
            i = j
            last_was_protected_end = False

    out = "".join(result)

    # ===== ABSOLUTE_TAIL: если всё сообщение — только защищённые слова =====
    # то есть после обработки никакого "не защищённого" текста не осталось
    if absolute_tail and absolute:
        # проверяем, есть ли в исходнике что-то кроме защищённых слов и пробелов
        stripped = text
        for word in protected_sorted:
            stripped = stripped.replace(word, "")
        stripped = stripped.replace(" ", "").replace("\t", "")

        if not stripped:
            # значит после защищённого слова нужно сгенерировать хвост
            # ищем последнее защищённое слово и всё, что после
            sep = " " if out and not out.endswith(" ") else ""
            out = out + sep + _generate_absolute_tail()

    return out


def generate_unique_message():
    if not CFG.get("avoid_repeats", True):
        msg = randomize_message(CFG["message"])
        _history.append(msg)
        return msg
    attempts = CFG.get("max_generation_attempts", 20)
    last = None
    for _ in range(attempts):
        msg = randomize_message(CFG["message"])
        last = msg
        if msg not in _history:
            _history.append(msg)
            return msg
    if last is not None:
        _history.append(last)
    return last if last is not None else ""


# ============================================================
# СПАМ
# ============================================================

def spam_loop():
    global spamming
    time.sleep(0.3)
    while spamming:
        try:
            msg = generate_unique_message()
            pyperclip.copy(msg)
            keyboard.press_and_release("t")
            time.sleep(0.05)
            keyboard.press_and_release("ctrl+v")
            time.sleep(0.02)
            keyboard.press_and_release("enter")
            time.sleep(CFG["delay"])
        except Exception:
            break


def toggle_spam():
    global spamming, spam_thread
    if spamming:
        spamming = False
        print("[STOP] Остановлено.")
    else:
        spamming = True
        print("[START] Спам запущен! Right Ctrl — стоп.")
        spam_thread = threading.Thread(target=spam_loop, daemon=True)
        spam_thread.start()


def main():
    print("=" * 60)
    print(f"  {APP_NAME}  |  Пресет: {PRESET_NAME.upper()}")
    print("=" * 60)
    print(f"  Сообщение:           {CFG['message']}")
    print(f"  Задержка:            {CFG['delay']} сек")
    print(f"  Хоткей:              {CFG['hotkey'].upper()}")
    print(f"  Защищённые:          {', '.join(CFG['protected_words'])}")
    print(f"  Пробел после защиты: {CFG.get('space_after_protected', True)}")
    print(f"  Анти-повтор:         {CFG.get('avoid_repeats', True)} "
          f"(история {CFG.get('history_size', 50)})")
    print(f"  Транслит:            {CFG.get('translit_mode', 'off')} "
          f"(шанс {CFG.get('translit_chance', 0.4)})")
    print(f"  Пробелы→цифры:       {CFG['replace_spaces_with_digits']}")
    print(f"  Символы/эмодзи:      {CFG['insert_between_letters']} "
          f"(режим {CFG.get('emoji_mode', 'off')}, шанс вставки {CFG['insert_chance']})")
    print(f"  Рандом регистра:     {CFG['randomize_case']}")
    print(f"  АБСОЛЮТНАЯ РАНДОМ.:  {CFG.get('absolute_random', False)}")
    print(f"  Absolute Tail:       {CFG.get('absolute_tail', False)} "
          f"(длина {CFG.get('absolute_tail_min', 8)}-{CFG.get('absolute_tail_max', 20)})")
    print("=" * 60)
    print("  Примеры генерации:")
    for _ in range(5):
        print("   ", randomize_message(CFG["message"]))
    print("=" * 60)
    print("  Переключись в Minecraft и нажми Right Ctrl")
    print()

    global spamming
    last_toggle_time = 0
    while True:
        try:
            if keyboard.is_pressed(CFG["hotkey"]):
                now = time.time()
                if now - last_toggle_time > 0.3:
                    toggle_spam()
                    last_toggle_time = now
            if keyboard.is_pressed("menu"):
                spamming = False
                print("\n[EXIT] Закрыто.")
                break
            time.sleep(0.01)
        except KeyboardInterrupt:
            spamming = False
            print("\n[EXIT] Закрыто.")
            break


if __name__ == "__main__":
    main()