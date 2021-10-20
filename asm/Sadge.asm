    .cpu cortex-m0
    .text
    .align 4
    .global sadge_san

sadge_san:
    push {r7, lr}
    sub sp, sp, #12
    mov r7, sp
    str r0, [r7, #4]
    mov r1, #11
    str r1, [r7, #8]
    ldr r0, [r7, #4]
    ldr r1, [r7, #8]
    cmp r0, r1
    blt .lt163true
    mov r0, #0
    b .lt163end
.lt163true:
    mov r0, #1
.lt163end:
    add sp, sp, #12
    pop {r7, pc}
