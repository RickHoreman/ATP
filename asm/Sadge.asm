    .cpu cortex-m0
    .text
    .align 4
    .global even_chan
    .global odd_tan
    .global sommig_sama
    .global sadge_sensei_k
    .global recursiveExpression_oujosama_k
    .global compare_san
    .global forLoop_san
    .global printXtimes_chan

even_chan:
    push {r7, lr}
    sub sp, sp, #12
    mov r7, sp
    str r0, [r7, #4]
    ldr r1, [r7, #4]
    mov r2, #0
    cmp r1, r2
    blt .lt26.21true
    mov r1, #0
    b .lt26.21end
.lt26.21true:
    mov r1, #1
.lt26.21end:
    str r1, [r7, #8]
    ldr r1, [r7, #8]
    mov r2, #1
    cmp r1, r2
    bne .if5.22end
    mov r0, #0
    mov r1, #1
    sub r0, r0, r1
    mov sp, r7
    add sp, sp, #12
    pop {r7, pc}
.if5.22end:
    ldr r1, [r7, #4]
    mov r2, #0
    cmp r1, r2
    bne .if5.26else
    mov r0, #1
    mov sp, r7
    add sp, sp, #12
    pop {r7, pc}
    b .if5.26end
.if5.26else:
    ldr r0, [r7, #4]
    mov r1, #1
    sub r0, r0, r1
    bl odd_tan
    mov r0, r0
    mov sp, r7
    add sp, sp, #12
    pop {r7, pc}
.if5.26end:
    mov sp, r7
    add sp, sp, #12
    pop {r7, pc}

odd_tan:
    push {r7, lr}
    sub sp, sp, #12
    mov r7, sp
    str r0, [r7, #4]
    ldr r1, [r7, #4]
    mov r2, #0
    cmp r1, r2
    blt .lt26.6true
    mov r1, #0
    b .lt26.6end
.lt26.6true:
    mov r1, #1
.lt26.6end:
    str r1, [r7, #8]
    ldr r1, [r7, #8]
    mov r2, #1
    cmp r1, r2
    bne .if5.7end
    mov r0, #0
    mov r1, #1
    sub r0, r0, r1
    mov sp, r7
    add sp, sp, #12
    pop {r7, pc}
.if5.7end:
    ldr r1, [r7, #4]
    mov r2, #0
    cmp r1, r2
    bne .if5.11else
    mov r0, #0
    mov sp, r7
    add sp, sp, #12
    pop {r7, pc}
    b .if5.11end
.if5.11else:
    ldr r0, [r7, #4]
    mov r1, #1
    sub r0, r0, r1
    bl even_chan
    mov r0, r0
    mov sp, r7
    add sp, sp, #12
    pop {r7, pc}
.if5.11end:
    mov sp, r7
    add sp, sp, #12
    pop {r7, pc}

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
.fl21.38:
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
    bge .ge21.38true
    mov r1, #0
    b .ge21.38end
.ge21.38true:
    mov r1, #1
.ge21.38end:
    cmp r1, #1
    beq .fl21.38
    ldr r0, [r7, #8]
    mov sp, r7
    add sp, sp, #24
    pop {r7, pc}
    mov sp, r7
    add sp, sp, #24
    pop {r7, pc}

sadge_sensei_k:
    push {r7, lr}
    sub sp, sp, #16
    mov r7, sp
    mov r1, #6
    mov r2, #3
    add r1, r1, r2
    str r1, [r7, #4]
    ldr r0, [r7, #4]
    bl odd_tan
    mov r1, r0
    str r1, [r7, #8]
    mov r1, #0
    str r1, [r7, #12]
    ldr r1, [r7, #8]
    mov r2, #1
    cmp r1, r2
    bne .if5.49end
    ldr r0, [r7, #4]
    bl sommig_sama
    mov r1, r0
    str r1, [r7, #12]
.if5.49end:
    ldr r0, [r7, #12]
    mov sp, r7
    add sp, sp, #16
    pop {r7, pc}
    mov sp, r7
    add sp, sp, #16
    pop {r7, pc}

recursiveExpression_oujosama_k:
    push {r7, lr}
    sub sp, sp, #8
    mov r7, sp
    mov r1, #8
    str r1, [r7, #4]
    push {r0}
    mov r0, #9
    bl sommig_sama
    mov r1, r0
    mov r0, #3
    sub r0, r0, r1
    mov r1, r0
    pop {r0}
    mov r0, #42
    add r0, r0, r1
    push {r0}
    ldr r0, [r7, #4]
    mov r1, #7
    add r0, r0, r1
    mov r1, #11
    sub r0, r0, r1
    mov r1, r0
    pop {r0}
    add r0, r0, r1
    mov sp, r7
    add sp, sp, #8
    pop {r7, pc}
    mov sp, r7
    add sp, sp, #8
    pop {r7, pc}

compare_san:
    push {r7, lr}
    sub sp, sp, #16
    mov r7, sp
    str r0, [r7, #4]
    str r1, [r7, #8]
    str r2, [r7, #12]
    ldr r1, [r7, #12]
    mov r2, #0
    cmp r1, r2
    bne .if5.62end
    ldr r0, [r7, #4]
    ldr r1, [r7, #8]
    cmp r0, r1
    bgt .gt22.64true
    mov r0, #0
    b .gt22.64end
.gt22.64true:
    mov r0, #1
.gt22.64end:
    mov sp, r7
    add sp, sp, #16
    pop {r7, pc}
.if5.62end:
    ldr r1, [r7, #12]
    mov r2, #1
    cmp r1, r2
    bne .if5.66end
    ldr r0, [r7, #4]
    ldr r1, [r7, #8]
    cmp r0, r1
    bge .ge22.68true
    mov r0, #0
    b .ge22.68end
.ge22.68true:
    mov r0, #1
.ge22.68end:
    mov sp, r7
    add sp, sp, #16
    pop {r7, pc}
.if5.66end:
    ldr r1, [r7, #12]
    mov r2, #2
    cmp r1, r2
    bne .if5.70end
    ldr r0, [r7, #4]
    ldr r1, [r7, #8]
    cmp r0, r1
    blt .lt22.72true
    mov r0, #0
    b .lt22.72end
.lt22.72true:
    mov r0, #1
.lt22.72end:
    mov sp, r7
    add sp, sp, #16
    pop {r7, pc}
.if5.70end:
    ldr r1, [r7, #12]
    mov r2, #3
    cmp r1, r2
    bne .if5.74else
    ldr r0, [r7, #4]
    ldr r1, [r7, #8]
    cmp r0, r1
    ble .le22.76true
    mov r0, #0
    b .le22.76end
.le22.76true:
    mov r0, #1
.le22.76end:
    mov sp, r7
    add sp, sp, #16
    pop {r7, pc}
    b .if5.74end
.if5.74else:
    mov r0, #0
    mov r1, #1
    sub r0, r0, r1
    mov sp, r7
    add sp, sp, #16
    pop {r7, pc}
.if5.74end:
    mov sp, r7
    add sp, sp, #16
    pop {r7, pc}

forLoop_san:
    push {r7, lr}
    sub sp, sp, #36
    mov r7, sp
    str r0, [r7, #4]
    str r1, [r7, #8]
    str r2, [r7, #12]
    str r3, [r7, #16]
    ldr r1, [r7, #16]
    mov r2, #0
    cmp r1, r2
    bne .if5.84end
    mov r1, #0
    str r1, [r7, #20]
    mov r1, #0
    str r1, [r7, #24]
    ldr r1, [r7, #12]
    str r1, [r7, #28]
    mov r1, #1
    str r1, [r7, #32]
.fl32.88:
    ldr r1, [r7, #20]
    mov r2, #1
    add r1, r1, r2
    str r1, [r7, #20]
    ldr r1, [r7, #24]
    ldr r2, [r7, #32]
    add r1, r1, r2
    str r1, [r7, #24]
    ldr r1, [r7, #24]
    ldr r2, [r7, #28]
    cmp r1, r2
    blt .lt32.88true
    mov r1, #0
    b .lt32.88end
.lt32.88true:
    mov r1, #1
.lt32.88end:
    cmp r1, #1
    beq .fl32.88
    ldr r0, [r7, #20]
    mov sp, r7
    add sp, sp, #36
    pop {r7, pc}
.if5.84end:
    ldr r1, [r7, #16]
    mov r2, #1
    cmp r1, r2
    bne .if5.94end
    mov r1, #0
    str r1, [r7, #20]
    ldr r1, [r7, #4]
    str r1, [r7, #24]
    ldr r1, [r7, #12]
    str r1, [r7, #28]
    mov r1, #1
    str r1, [r7, #32]
.fl37.98:
    ldr r1, [r7, #20]
    mov r2, #1
    add r1, r1, r2
    str r1, [r7, #20]
    ldr r1, [r7, #24]
    ldr r2, [r7, #32]
    add r1, r1, r2
    str r1, [r7, #24]
    ldr r1, [r7, #24]
    ldr r2, [r7, #28]
    cmp r1, r2
    blt .lt37.98true
    mov r1, #0
    b .lt37.98end
.lt37.98true:
    mov r1, #1
.lt37.98end:
    cmp r1, #1
    beq .fl37.98
    ldr r0, [r7, #20]
    mov sp, r7
    add sp, sp, #36
    pop {r7, pc}
.if5.94end:
    ldr r1, [r7, #16]
    mov r2, #2
    cmp r1, r2
    bne .if5.104end
    mov r1, #0
    str r1, [r7, #20]
    ldr r1, [r7, #4]
    str r1, [r7, #24]
    ldr r1, [r7, #12]
    str r1, [r7, #28]
    mov r1, #0
    sub r1, r1, #1
    str r1, [r7, #32]
.fl37.108:
    ldr r1, [r7, #20]
    mov r2, #1
    add r1, r1, r2
    str r1, [r7, #20]
    ldr r1, [r7, #24]
    ldr r2, [r7, #32]
    add r1, r1, r2
    str r1, [r7, #24]
    ldr r1, [r7, #24]
    ldr r2, [r7, #28]
    cmp r1, r2
    bgt .gt37.108true
    mov r1, #0
    b .gt37.108end
.gt37.108true:
    mov r1, #1
.gt37.108end:
    cmp r1, #1
    beq .fl37.108
    ldr r0, [r7, #20]
    mov sp, r7
    add sp, sp, #36
    pop {r7, pc}
.if5.104end:
    ldr r1, [r7, #16]
    mov r2, #3
    cmp r1, r2
    bne .if5.114else
    mov r1, #0
    str r1, [r7, #20]
    ldr r1, [r7, #4]
    str r1, [r7, #24]
    ldr r1, [r7, #12]
    str r1, [r7, #28]
    ldr r1, [r7, #8]
    str r1, [r7, #32]
.fl37.118:
    ldr r1, [r7, #20]
    mov r2, #1
    add r1, r1, r2
    str r1, [r7, #20]
    ldr r1, [r7, #24]
    ldr r2, [r7, #32]
    add r1, r1, r2
    str r1, [r7, #24]
    ldr r1, [r7, #24]
    ldr r2, [r7, #28]
    cmp r1, r2
    blt .lt37.118true
    mov r1, #0
    b .lt37.118end
.lt37.118true:
    mov r1, #1
.lt37.118end:
    cmp r1, #1
    beq .fl37.118
    ldr r0, [r7, #20]
    mov sp, r7
    add sp, sp, #36
    pop {r7, pc}
    b .if5.114end
.if5.114else:
    mov r0, #0
    mov r1, #1
    sub r0, r0, r1
    mov sp, r7
    add sp, sp, #36
    pop {r7, pc}
.if5.114end:
    mov sp, r7
    add sp, sp, #36
    pop {r7, pc}

printXtimes_chan:
    push {r7, lr}
    sub sp, sp, #24
    mov r7, sp
    str r0, [r7, #4]
    str r1, [r7, #8]
    mov r1, #0
    str r1, [r7, #12]
    ldr r1, [r7, #8]
    str r1, [r7, #16]
    mov r1, #1
    str r1, [r7, #20]
.fl28.131:
    ldr r0, [r7, #4]
    bl print
    ldr r1, [r7, #12]
    ldr r2, [r7, #20]
    add r1, r1, r2
    str r1, [r7, #12]
    ldr r1, [r7, #12]
    ldr r2, [r7, #16]
    cmp r1, r2
    blt .lt28.131true
    mov r1, #0
    b .lt28.131end
.lt28.131true:
    mov r1, #1
.lt28.131end:
    cmp r1, #1
    beq .fl28.131
    mov sp, r7
    add sp, sp, #24
    pop {r7, pc}
