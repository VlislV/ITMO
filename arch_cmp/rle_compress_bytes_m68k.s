    .data

.org             0x00



input_addr:      .word  0x80

output_addr:     .word  0x84

stack_top:       .word  0x500

str_ptr:         .word  0x300              ; буфер для результата



    .text

    .org     0x100



; ======================================== Обработка ошибок ===

ret_err:

    move.l   -1, (A1)

    halt



ret_emp:

    move.l   0, (A1)

    halt



; ======================================== Новая пара ===

push_new_pair:

    add.b    2, (A5)                         ; счётчик пар +1

    move.b   1, -(A6)                        ; count = 1

    move.b   D5, -(A6)                       ; byte

    jmp      return



; ======================================== Сравнение байта ===

    ; D5 = текущий байт, D7 = счётчик оставшихся байт

    ; (A5) = кол-во пар, (A6) = предыдущий байт, 1(A6) = счётчик повторов пары

compare:

    sub.l    1, D7                           ; осталось--

    bmi      return                          ; if < 0 D7 -> return



    cmp.b    0, (A5)                         ; есть ли уже пары?

    beq      push_new_pair                   ; нет -> первая пара



    cmp.b    D5, (A6)                        ; совпадает с предыдущим байтом?

    bne      push_new_pair                   ; нет -> новая пара



    add.b    1, 1(A6)                        ; да -> счётчик повторов++

    jmp      return



; ======================================== Разбор слова на байты и сжатие ===

compressor:

    move.l   D1, D2

    move.l   D1, D3

    move.l   D1, D4



    and.l    0xFF000000, D4                  ; старший

    and.l    0x00FF0000, D3                  ; второй

    and.l    0x0000FF00, D2                  ; третий



    lsr.l    24, D4

    lsr.l    16, D3

    lsr.l    8, D2



    move.b   D4, D5

    jsr      compare

    move.b   D3, D5

    jsr      compare

    move.b   D2, D5

    jsr      compare

    move.b   D1, D5

    jsr      compare

    jmp      return



; ======================================== start ===

_start:

    movea.l  input_addr, A0                  ; A0 = адрес порта ввода

    movea.l  (A0), A0                        ; A0 = 0x80

    movea.l  output_addr, A1                 ; A1 = 0x84

    movea.l  (A1), A1

    movea.l  stack_top, A7                   ; A7 = стек 0x500

    movea.l  (A7), A7



    move.l   (A0), D0                        ; D0 = длина

    cmp.l    0, D0

    bmi      ret_err

    beq      ret_emp



    move.l   D0, D7                          ; D7 = счётчик байт

    jsr      load_words

    halt



; ======================================== Загрузка и сжатие ===

load_words:

    movea.l  str_ptr, A6

    movea.l  (A6), A5                        ; A5 = 0x300 вершина буфера (const)

    movea.l  (A6), A6                        ; A6 = 0x300 вершина буфера



    move.b   0, (A5)



    add.l    3, D0                           ; округление вверх

    div.l    4, D0                           ; D0 = кол-во слов



load_words_loop:

    sub.l    1, D0

    bmi      stack_out                       ; все слова обработаны



    move.l   (A0), D1                        ; чтение слова из input

    jsr      compressor

    jmp      load_words_loop



; ======================================== Вывод в output ===

stack_out:

    move.b   (A5), (A1)                      ; длина

    move.b   (A5), D6

    add.l    3, D6

    div.l    4, D6                           ; D6 = кол-во слов для вывода



stack_out_loop:

    sub.b    1, D6

    bmi      return

    move.l   -(A5), (A1)

    jmp      stack_out_loop



return:

    rts