    .data
.org             0x00
input_addr:      .word  0x80
output_addr:     .word  0x84
count:           .word  0x01               \count divs (included n himself as div)
divisor:         .word  0x00               \contain current div
n:               .word  0x00

    .text
    .org 0x100
    \=====================================

_start:

    @p input_addr a! @       \ dataStack.push(n)

    lit -1
    +
    dup

    -if count_devisors       \ if (n - 1) >= 0 goto count_devisors

    return_value_error       \ else return -1

    \=====================================

return_value_error:
    @p output_addr a!
    lit -1 !
    halt

    \=====================================

return_result:
    @p output_addr a!
    @p count !
    halt

    \=====================================

count_devisors:

    dup
    >r                       \  returnStack.push(n - 1)

    lit 1
    +
    !p n                     \ access to input number (n) through label

    lit divisor
    b!                       \ B <- divisor (label addr)

count_devisors_loop:

    @p n
    a!                       \ A <- n

    r>
    dup
    !p divisor
    >r                       \ returnStack.top() -> mem[B]

    divide

    if update_count          \ if n % divisor == 0 goto update_count

    next count_devisors_loop

    return_result

    \=====================================

divide:

    lit 31 >r                \cycle counter (word)

    lit 0
    lit 0                    \ DStack prep

divide_loop:
    +/                       \ divide_loop -> T: n // div ; S: n % div
    next divide_loop

    drop                     \ S --> T
    ;

    \=====================================

update_count:
    @p count
    lit 1
    +
    !p count                 \ count += 1
    next count_devisors_loop

    \=====================================
