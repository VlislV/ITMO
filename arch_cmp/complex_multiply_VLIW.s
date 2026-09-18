    .data
input_addr:      .word  0x80
output_addr:     .word  0x84
    .text
    .org 0x100
_start:
    ;### load *ptr to MMIO
    lui t0, %hi(input_addr)      / lui t5, %hi(output_addr)      / nop          / nop
    addi t0, t0, %lo(input_addr) / addi t5, t5, %lo(output_addr) / nop          / nop
    nop                          / nop                           / lw t0, 0(t0) / nop
    nop                          / nop                           / lw t5, 0(t5) / nop

    ;### load (a,b,c,d) -> (t1, t2, t3, t4), s7 == 1, goto complex_multiply
    nop                          / nop                           / lw t1, 0(t0) / nop
    nop                          / nop                           / lw t2, 0(t0) / nop
    addi s7, s7, 0x1             / nop                           / lw t3, 0(t0) / nop
    nop                          / nop                           / lw t4, 0(t0) / jal ra, complex_multiply


    ;### a0 -> Re a4 -> Im
return_parts:
    nop                          / nop                           / sw a0, 0(t5) / nop
    nop                          / nop                           / sw a4, 0(t5) / nop
    nop                          / nop                           / nop          / halt

complex_multiply:

    ;### (if a * c || b * d > 0xFFFFFFFF than goto return_error)
    mul a0, t1, t3               / mulh a1, t1, t3               / nop          / bgt a1, s7, return_error
    mul a2, t2, t4               / mulh a3, t2, t4               / nop          / bgt a3, s7, return_error

    xor a1, t1, t3               / xor a3, t2, t4                / nop          / beq a0, zero, continue1
    xor a1, a1, a0               / xor a3, a3, a2                / nop          / beq a2, zero, continue1

    ;### (if a != 0 & c != 0) -> (if (a ^ c) ^ (a * c) & 0x80000000 == 1 than goto return_error)
    nop                          / nop                           / nop          / blt a1, zero, return_error
    nop                          / nop                           / nop          / blt a3, zero, return_error

continue1:

    mul a4, t1, t4               / mulh a5, t1, t4               / nop          / bgt a5, s7, return_error
    mul a6, t2, t3               / mulh a7, t2, t3               / nop          / bgt a7, s7, return_error

    xor a5, t1, t4               / xor a7, t2, t3                / nop          / beq a4, zero, continue2
    xor a5, a5, a4               / xor a7, a7, a6                / nop          / beq a6, zero, continue2

    nop                          / nop                           / nop          / blt a5, zero, return_error
    nop                          / nop                           / nop          / blt a7, zero, return_error

continue2:
    sub a0, a0, a2               / add a4, a4, a6                / nop          / jr ra

return_error:
    lui a0, %hi(0xCCCCCCCC)      / nop                           / nop          / nop
    addi a0, a0, %lo(0xCCCCCCCC) / nop                           / nop          / nop
    nop                          / nop                           / sw a0, 0(t5) / nop
    nop                          / nop                           / nop          / halt