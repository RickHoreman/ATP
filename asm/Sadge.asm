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
    ldr r1, [r7, #8]
    ldr r2, [r7, #4]
    cmp r1, r2
    bne .if5.3else
    ldr r0, [r7, #8]
    ldr r1, [r7, #4]
    add r0, r0, r1
    add sp, sp, #12
    pop {r7, pc}
    b .if5.3end
.if5.3else:
    ldr r0, [r7, #8]
    ldr r1, [r7, #4]
    sub r0, r0, r1
    add sp, sp, #12
    pop {r7, pc}
.if5.3end:
    add sp, sp, #12
    pop {r7, pc}
