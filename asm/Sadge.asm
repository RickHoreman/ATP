    .cpu cortex-m0
    .text
    .align 4
    .global sommig_sama
    .global sadge_san

sommig_sama:
    push {r7, lr}
    sub sp, sp, #24
    mov r7, sp
    str r0, [r7, #4]
    mov r1, #0
    str r1, [r7, #8]
    ldr r1, [r7, #4]
    str r1, [r7, #12]
    mov r1, #1
    str r1, [r7, #16]
    mov r1, #0
    sub r1, r1, #1
    str r1, [r7, #20]
.fl21.4:
    ldr r1, [r7, #8]
    ldr r2, [r7, #12]
    add r1, r1, r2
    str r1, [r7, #8]
    ldr r1, [r7, #12]
    ldr r2, [r7, #20]
    add r1, r1, r2
    str r1, [r7, #12]
    ldr r1, [r7, #12]
    ldr r2, [r7, #16]
    cmp r1, r2
    bge .ge21.4true
    mov r1, #0
    b .ge21.4end
.ge21.4true:
    mov r1, #1
.ge21.4end:
    cmp r1, #1
    beq .fl21.4
    ldr r0, [r7, #8]
    add sp, sp, #24
    pop {r7, pc}
    mov sp, r7
    add sp, sp, #24
    pop {r7, pc}

sadge_san:
    push {r7, lr}
    sub sp, sp, #8
    mov r7, sp
    str r0, [r7, #4]
    ldr r0, [r7, #4]
    bl sommig_sama
    mov r0, r0
    add sp, sp, #8
    pop {r7, pc}
    mov sp, r7
    add sp, sp, #8
    pop {r7, pc}
