    .data
.org             0x00
buffer:          .byte  '________________________________' ; 32-byte storage
reserve:         .byte  '___'              ; 3 bytes (unstable)
input_addr:      .word  0x80
output_addr:     .word  0x84
buffer_ptr:      .word  0                  ; buffer pointer
current_size:    .word  0                  ; used buffer space
max_size:        .word  32
const_FF:        .word  0xFF
symbol_Alpha_left_bound: .word  'A'
symbol_Alpha_right_bound: .word  '['                ;'Z' + 1
symbol_alpha_left_bound: .word  'a'
symbol_alpha_right_bound: .word  '{'                ;'z' + 1

current_symbol:  .word  0
flag:            .word  1                  ; trigger for toUpper/toLower

    .text
    .org         0x100

_start:
    load -10
    halt