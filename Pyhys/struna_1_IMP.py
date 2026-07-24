from pptx import Presentation
from pptx.util import Inches, Pt, Emu
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE
import os

# ===== НАСТРОЙКИ СТИЛЯ =====
BG_COLOR = RGBColor(0x1A, 0x1A, 0x2E)        # Тёмно-синий фон
ACCENT_COLOR = RGBColor(0xFF, 0x8C, 0x00)     # Оранжевый акцент
WHITE = RGBColor(0xFF, 0xFF, 0xFF)
LIGHT_GRAY = RGBColor(0xB0, 0xB0, 0xB0)
RED = RGBColor(0xFF, 0x44, 0x44)
FONT_NAME = "Arial"  # Гротеск без засечек, доступен везде
SLIDE_WIDTH = Inches(13.333)
SLIDE_HEIGHT = Inches(7.5)

prs = Presentation()
prs.slide_width = SLIDE_WIDTH
prs.slide_height = SLIDE_HEIGHT

# ===== ВСПОМОГАТЕЛЬНЫЕ ФУНКЦИИ =====
def add_bg(slide):
    """Заливка фона тёмным цветом."""
    background = slide.background
    fill = background.fill
    fill.solid()
    fill.fore_color.rgb = BG_COLOR

def add_textbox(slide, left, top, width, height, text, font_size=18, bold=False, color=WHITE, alignment=PP_ALIGN.LEFT, font_name=FONT_NAME):
    """Универсальная текстовая рамка."""
    txBox = slide.shapes.add_textbox(Inches(left), Inches(top), Inches(width), Inches(height))
    tf = txBox.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = text
    p.font.size = Pt(font_size)
    p.font.bold = bold
    p.font.color.rgb = color
    p.font.name = font_name
    p.alignment = alignment
    return tf

def add_rect(slide, left, top, width, height, fill_color, border_color=None):
    """Прямоугольник-плашка."""
    shape = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(left), Inches(top), Inches(width), Inches(height))
    shape.fill.solid()
    shape.fill.fore_color.rgb = fill_color
    if border_color:
        shape.line.color.rgb = border_color
        shape.line.width = Pt(1)
    else:
        shape.line.fill.background()
    return shape

def add_arrow_down(slide, left, top, width, height, color=RED):
    """Стрелка вниз (треугольник)."""
    shape = slide.shapes.add_shape(MSO_SHAPE.DOWN_ARROW, Inches(left), Inches(top), Inches(width), Inches(height))
    shape.fill.solid()
    shape.fill.fore_color.rgb = color
    shape.line.fill.background()
    return shape

def add_arrow_up(slide, left, top, width, height, color=RGBColor(0x00, 0xCC, 0x66)):
    """Стрелка вверх."""
    shape = slide.shapes.add_shape(MSO_SHAPE.UP_ARROW, Inches(left), Inches(top), Inches(width), Inches(height))
    shape.fill.solid()
    shape.fill.fore_color.rgb = color
    shape.line.fill.background()
    return shape

def add_metric_card(slide, left, top, width, height, title, value, value_color=RED):
    """Карточка с заголовком и крупной цифрой."""
    add_rect(slide, left, top, width, height, RGBColor(0x25, 0x25, 0x40), border_color=RGBColor(0x40, 0x40, 0x60))
    add_textbox(slide, left + 0.2, top + 0.1, width - 0.4, 0.5, title, font_size=14, color=LIGHT_GRAY, alignment=PP_ALIGN.CENTER)
    add_textbox(slide, left + 0.2, top + 0.6, width - 0.4, 0.8, value, font_size=36, bold=True, color=value_color, alignment=PP_ALIGN.CENTER)

# ==================== СЛАЙД 1: ТИТУЛЬНЫЙ ====================
slide1 = prs.slides.add_slide(prs.slide_layouts[6])  # пустой
add_bg(slide1)
# Оранжевая линия сверху
add_rect(slide1, 0, 0, 13.333, 0.05, ACCENT_COLOR)
# Заголовок
add_textbox(slide1, 1.5, 2.0, 10.3, 1.5, "Фундамент вместо иллюзий:", font_size=44, bold=True, color=WHITE, alignment=PP_ALIGN.CENTER)
add_textbox(slide1, 1.5, 3.0, 10.3, 1.5, "как выжить на рынке, где код пишет ИИ", font_size=44, bold=True, color=ACCENT_COLOR, alignment=PP_ALIGN.CENTER)
# Подзаголовок
add_textbox(slide1, 2.5, 4.8, 8.3, 1.0, "Почему спрос на начинающих разработчиков упал до уровня 1980 года\nи что делать прямо сейчас", font_size=20, color=LIGHT_GRAY, alignment=PP_ALIGN.CENTER)

# ==================== СЛАЙД 2: ГЛАВНАЯ ЦИФРА ====================
slide2 = prs.slides.add_slide(prs.slide_layouts[6])
add_bg(slide2)
add_textbox(slide2, 1.0, 0.5, 11.3, 1.0, "–27,5%  за два года", font_size=48, bold=True, color=RED, alignment=PP_ALIGN.CENTER)
add_textbox(slide2, 1.0, 1.5, 11.3, 0.8, "Занятость программистов в США рухнула до уровня 45-летней давности", font_size=22, color=WHITE, alignment=PP_ALIGN.CENTER)
# График (упрощённый прямоугольниками)
add_rect(slide2, 2.5, 2.8, 8.3, 2.5, RGBColor(0x25, 0x25, 0x40), border_color=RGBColor(0x40, 0x40, 0x60))
add_textbox(slide2, 3.0, 3.0, 7.3, 0.5, "Число занятых в IT, США", font_size=16, color=LIGHT_GRAY)
# Столбцы-заменители графика (упрощение)
for i, (h, yr) in enumerate([(1.5, "'20"), (1.7, "'21"), (1.8, "'22"), (1.0, "'23"), (0.8, "'24")]):
    x = 4.0 + i * 1.2
    add_rect(slide2, x, 5.2 - h, 0.6, h, ACCENT_COLOR if h > 1.5 else RED)
    add_textbox(slide2, x, 5.3, 0.6, 0.4, yr, font_size=12, color=LIGHT_GRAY, alignment=PP_ALIGN.CENTER)
# Стрелка вниз и подпись
add_arrow_down(slide2, 5.8, 5.5, 1.5, 1.0)
add_textbox(slide2, 4.0, 6.5, 5.3, 0.5, "Уровень 1980 года", font_size=16, color=RED, alignment=PP_ALIGN.CENTER)
# Иконка ChatGPT (текстовая имитация)
add_textbox(slide2, 9.0, 2.5, 2.5, 0.5, "⚡ ChatGPT", font_size=18, bold=True, color=ACCENT_COLOR)

# ==================== СЛАЙД 3: ТРЕУГОЛЬНИК В РОМБ ====================
slide3 = prs.slides.add_slide(prs.slide_layouts[6])
add_bg(slide3)
add_textbox(slide3, 1.0, 0.5, 11.3, 0.8, "Рынок больше не треугольник", font_size=36, bold=True, color=WHITE, alignment=PP_ALIGN.CENTER)
# Треугольник
shape_tri = slide3.shapes.add_shape(MSO_SHAPE.ISOSCELES_TRIANGLE, Inches(2.0), Inches(1.8), Inches(3.5), Inches(4.0))
shape_tri.fill.solid(); shape_tri.fill.fore_color.rgb = RGBColor(0x30, 0x30, 0x50); shape_tri.line.fill.background()
add_textbox(slide3, 2.5, 5.2, 2.5, 0.5, "Было", font_size=16, color=LIGHT_GRAY, alignment=PP_ALIGN.CENTER)
# Стрелка трансформации
add_textbox(slide3, 5.8, 3.5, 1.5, 0.8, "→", font_size=48, bold=True, color=ACCENT_COLOR, alignment=PP_ALIGN.CENTER)
# Ромб
shape_rom = slide3.shapes.add_shape(MSO_SHAPE.DIAMOND, Inches(7.5), Inches(1.8), Inches(3.5), Inches(4.0))
shape_rom.fill.solid(); shape_rom.fill.fore_color.rgb = RGBColor(0x30, 0x30, 0x50); shape_rom.line.fill.background()
add_textbox(slide3, 8.0, 5.2, 2.5, 0.5, "Стало", font_size=16, color=LIGHT_GRAY, alignment=PP_ALIGN.CENTER)
# Подписи
add_textbox(slide3, 1.0, 6.5, 3.0, 0.5, "Много джуниоров", font_size=12, color=LIGHT_GRAY, alignment=PP_ALIGN.CENTER)
add_textbox(slide3, 9.5, 6.5, 3.0, 0.5, "Архитектура, ревью", font_size=12, color=ACCENT_COLOR, alignment=PP_ALIGN.CENTER)

# ==================== СЛАЙД 4: КОГО СОКРАЩАЮТ ====================
slide4 = prs.slides.add_slide(prs.slide_layouts[6])
add_bg(slide4)
add_textbox(slide4, 1.0, 0.3, 11.3, 0.8, "Типовой код = конкуренция с машиной", font_size=34, bold=True, color=WHITE, alignment=PP_ALIGN.CENTER)
# Три карточки
add_metric_card(slide4, 1.0, 1.5, 3.5, 2.5, "Big Tech (SignalFire)", "–50%\nс 2019", RED)
add_metric_card(slide4, 5.0, 1.5, 3.5, 2.5, "«Великолепная семёрка»", "Доля студентов\nвдвое ↓", RED)
add_metric_card(slide4, 9.0, 1.5, 3.5, 2.5, "Klarna (ИИ-бот)", "= 700\nсотрудников", RED)
add_textbox(slide4, 1.0, 4.5, 11.3, 1.0, "Наём выпускников в крупнейшие компании упал на 25% за 2024 год", font_size=18, color=LIGHT_GRAY, alignment=PP_ALIGN.CENTER)

# ==================== СЛАЙД 5: ВЕСЫ ====================
slide5 = prs.slides.add_slide(prs.slide_layouts[6])
add_bg(slide5)
add_textbox(slide5, 1.0, 0.5, 11.3, 0.8, "Вы конкурируете с подпиской на Netflix", font_size=36, bold=True, color=WHITE, alignment=PP_ALIGN.CENTER)
# Левая чаша
add_rect(slide5, 2.5, 2.0, 3.5, 3.5, RGBColor(0x30, 0x30, 0x50), border_color=RED)
add_textbox(slide5, 2.7, 2.2, 3.1, 1.0, "👨‍💻 Junior Dev", font_size=24, bold=True, color=WHITE, alignment=PP_ALIGN.CENTER)
add_textbox(slide5, 2.7, 3.5, 3.1, 1.0, "Зарплата\n+ бонусы + офис", font_size=18, color=LIGHT_GRAY, alignment=PP_ALIGN.CENTER)
# Правая чаша
add_rect(slide5, 7.5, 2.0, 3.5, 3.5, RGBColor(0x30, 0x30, 0x50), border_color=RGBColor(0x00, 0xCC, 0x66))
add_textbox(slide5, 7.7, 2.2, 3.1, 1.0, "🤖 ChatGPT", font_size=24, bold=True, color=WHITE, alignment=PP_ALIGN.CENTER)
add_textbox(slide5, 7.7, 3.5, 3.1, 1.0, "≈ $20 / мес\n24/7, не устаёт", font_size=18, color=LIGHT_GRAY, alignment=PP_ALIGN.CENTER)
# Весы (текстовая имитация)
add_textbox(slide5, 5.8, 2.5, 2.0, 2.0, "⚖️", font_size=60, color=ACCENT_COLOR, alignment=PP_ALIGN.CENTER)
add_textbox(slide5, 3.0, 6.0, 7.3, 0.5, "Левая чаша резко уходит вверх", font_size=14, color=RED, alignment=PP_ALIGN.CENTER)

# ==================== СЛАЙД 6: УСЛОЖНЕНИЕ ====================
slide6 = prs.slides.add_slide(prs.slide_layouts[6])
add_bg(slide6)
add_textbox(slide6, 1.0, 0.5, 11.3, 0.8, "Код сгенерирован. Что дальше?", font_size=36, bold=True, color=WHITE, alignment=PP_ALIGN.CENTER)
# Фрагмент "кода" (стилизованный прямоугольник)
add_rect(slide6, 1.5, 1.8, 5.5, 3.5, RGBColor(0x10, 0x10, 0x20), border_color=RGBColor(0x40, 0x40, 0x60))
add_textbox(slide6, 1.7, 2.0, 5.1, 3.0, "def process(data):\n  # [Баг?]\n  result = []\n  for item in data:\n    # [Уязвимость?]\n    result.append(item*2)\n  return result", font_size=16, color=RGBColor(0x00, 0xCC, 0x66), font_name="Courier New")
# Цитата
add_rect(slide6, 7.8, 1.8, 4.5, 3.5, RGBColor(0x25, 0x25, 0x40), border_color=ACCENT_COLOR)
add_textbox(slide6, 8.0, 2.0, 4.1, 0.5, "Гради Буч:", font_size=16, bold=True, color=ACCENT_COLOR)
add_textbox(slide6, 8.0, 2.5, 4.1, 2.5, "«ИИ может дать\nвам ответ, но он\nне может объяснить\n почему»", font_size=22, bold=True, color=WHITE)

# ==================== СЛАЙД 7: СМЕЩЕНИЕ ФОКУСА ====================
slide7 = prs.slides.add_slide(prs.slide_layouts[6])
add_bg(slide7)
add_textbox(slide7, 1.0, 0.3, 11.3, 0.8, "Меньше пишем код — больше думаем", font_size=36, bold=True, color=WHITE, alignment=PP_ALIGN.CENTER)
# Круг "Раньше"
shape_old = slide7.shapes.add_shape(MSO_SHAPE.OVAL, Inches(1.5), Inches(1.5), Inches(4.5), Inches(4.5))
shape_old.fill.solid(); shape_old.fill.fore_color.rgb = RED; shape_old.line.fill.background()
add_textbox(slide7, 1.8, 2.5, 3.9, 1.5, "Написание\nкода\n70%", font_size=28, bold=True, color=WHITE, alignment=PP_ALIGN.CENTER)
# Круг "Сейчас"
shape_new = slide7.shapes.add_shape(MSO_SHAPE.OVAL, Inches(7.5), Inches(1.5), Inches(4.5), Inches(4.5))
shape_new.fill.solid(); shape_new.fill.fore_color.rgb = RGBColor(0x00, 0xCC, 0x66); shape_new.line.fill.background()
add_textbox(slide7, 7.8, 2.2, 3.9, 2.0, "Архитектура\nДизайн систем\nПостановка\nзадач ИИ\n70%", font_size=22, bold=True, color=WHITE, alignment=PP_ALIGN.CENTER)
# Стрелка
add_textbox(slide7, 5.8, 3.0, 2.0, 1.0, "→", font_size=48, bold=True, color=WHITE, alignment=PP_ALIGN.CENTER)

# ==================== СЛАЙД 8: ВЕЧНЫЕ ЗНАНИЯ ====================
slide8 = prs.slides.add_slide(prs.slide_layouts[6])
add_bg(slide8)
add_textbox(slide8, 1.0, 0.5, 11.3, 0.8, "Фундамент не устаревает", font_size=36, bold=True, color=WHITE, alignment=PP_ALIGN.CENTER)
# Три колонки с "каменными" блоками
blocks = [("Алгоритмы\nи структуры\nданных", 1.5), ("Устройство\nсетей\nи памяти", 5.2), ("Архитектурные\nпаттерны", 8.9)]
for text, left in blocks:
    add_rect(slide8, left, 1.8, 3.0, 3.5, RGBColor(0x40, 0x40, 0x60))
    add_textbox(slide8, left + 0.2, 2.2, 2.6, 2.8, text, font_size=24, bold=True, color=WHITE, alignment=PP_ALIGN.CENTER)
    # Иконка замка́ (текстовая имитация)
    add_textbox(slide8, left + 0.2, 1.5, 2.6, 0.5, "🔒", font_size=28, color=ACCENT_COLOR, alignment=PP_ALIGN.CENTER)
add_textbox(slide8, 1.5, 5.8, 10.3, 0.8, "Стек меняется — база остаётся", font_size=18, color=LIGHT_GRAY, alignment=PP_ALIGN.CENTER)

# ==================== СЛАЙД 9: ПРОГНОЗ BLS ====================
slide9 = prs.slides.add_slide(prs.slide_layouts[6])
add_bg(slide9)
add_textbox(slide9, 1.0, 0.3, 11.3, 1.2, "+17% спрос на архитекторов к 2033", font_size=40, bold=True, color=RGBColor(0x00, 0xCC, 0x66), alignment=PP_ALIGN.CENTER)
add_textbox(slide9, 2.0, 1.5, 9.3, 0.8, "Прогноз Бюро трудовой статистики США", font_size=20, color=LIGHT_GRAY, alignment=PP_ALIGN.CENTER)
# Стрелка роста
add_arrow_up(slide9, 5.5, 2.5, 2.3, 3.0, RGBColor(0x00, 0xCC, 0x66))
add_textbox(slide9, 4.0, 5.8, 5.3, 0.5, "2024                                               2033", font_size=14, color=LIGHT_GRAY, alignment=PP_ALIGN.CENTER)
add_textbox(slide9, 2.0, 6.3, 9.3, 0.8, "Разработчики, проектирующие системы, а не просто пишущие код", font_size=18, color=WHITE, alignment=PP_ALIGN.CENTER)

# ==================== СЛАЙД 10: КЛЮЧЕВАЯ ФРАЗА ====================
slide10 = prs.slides.add_slide(prs.slide_layouts[6])
add_bg(slide10)
# Оранжевая рамка для цитаты
add_rect(slide10, 2.0, 2.0, 9.3, 3.5, RGBColor(0x25, 0x25, 0x40), border_color=ACCENT_COLOR)
add_textbox(slide10, 2.5, 2.3, 8.3, 2.8, "«Вашу работу заберёт\nне ИИ,\nа человек, который умело\nего использует»", font_size=36, bold=True, color=WHITE, alignment=PP_ALIGN.CENTER)

# ==================== СЛАЙД 11: ПОРТРЕТ ВЫЖИВШЕГО ====================
slide11 = prs.slides.add_slide(prs.slide_layouts[6])
add_bg(slide11)
add_textbox(slide11, 1.0, 0.3, 11.3, 0.8, "Кто будет проектировать системы завтра?", font_size=34, bold=True, color=WHITE, alignment=PP_ALIGN.CENTER)
items = [
    ("Инвестирует время в фундамент сегодня", "📚"),
    ("Ставит задачи ИИ и проверяет результат", "🎯"),
    ("Понимает, что под капотом", "⚙️"),
]
for i, (text, icon) in enumerate(items):
    y = 1.8 + i * 1.8
    add_rect(slide11, 2.5, y, 8.3, 1.2, RGBColor(0x25, 0x25, 0x40), border_color=ACCENT_COLOR)
    add_textbox(slide11, 2.7, y + 0.2, 1.0, 0.8, icon, font_size=28, alignment=PP_ALIGN.CENTER)
    add_textbox(slide11, 3.8, y + 0.3, 6.8, 0.6, text, font_size=22, bold=True, color=WHITE)

# ==================== СЛАЙД 12: ЗАВЕРШЕНИЕ ====================
slide12 = prs.slides.add_slide(prs.slide_layouts[6])
add_bg(slide12)
add_textbox(slide12, 1.0, 1.0, 11.3, 1.5, "Избавляйтесь\nот чёрных ящиков", font_size=44, bold=True, color=WHITE, alignment=PP_ALIGN.CENTER)
add_textbox(slide12, 1.0, 2.8, 11.3, 1.0, "Не будьте теми 700 сотрудниками,\nкоторых заменил один бот", font_size=22, color=LIGHT_GRAY, alignment=PP_ALIGN.CENTER)
add_textbox(slide12, 1.0, 4.5, 11.3, 1.0, "Спасибо. Вопросы?", font_size=32, bold=True, color=ACCENT_COLOR, alignment=PP_ALIGN.CENTER)
add_textbox(slide12, 1.0, 6.5, 11.3, 0.5, "Берегите себя и своих близких", font_size=16, color=LIGHT_GRAY, alignment=PP_ALIGN.CENTER)

# ===== СОХРАНЕНИЕ =====
output_path = os.path.join(os.path.expanduser("~"), "Desktop", "IT_Fundamentals_vs_AI.pptx")
prs.save(output_path)
print(f"Презентация сохранена: {output_path}")