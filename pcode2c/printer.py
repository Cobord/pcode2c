import pypcode


def is_branch(op: pypcode.OpCode):
    return op in (
        pypcode.OpCode.BRANCH,
        pypcode.OpCode.CBRANCH,
        pypcode.OpCode.BRANCHIND,
        pypcode.OpCode.CALL,
        pypcode.OpCode.CALLIND,
        pypcode.OpCode.RETURN,
    )


def fmt_varnode(varnode: pypcode.Varnode):
    if varnode.space.name == "const":
        return hex(varnode.offset) + ", " + hex(varnode.size)

    regname = varnode.getRegisterName()
    if regname != "":
        regname = f" /* {regname} */"
    return (
        f"{varnode.space.name}_space + {hex(varnode.offset)}{regname}, {varnode.size}"
    )


def fmt_insn(op: pypcode.PcodeOp):
    args = [fmt_varnode(op.output)] if op.output else []
    args.extend(fmt_varnode(varnode) for varnode in op.inputs)
    args = ", ".join(args)
    opcode = str(op.opcode).replace("pypcode.pypcode_native.OpCode.", "")
    if is_branch(op.opcode):
        return f"{opcode}({args});break;"
    else:
        return f"{opcode}({args});"


"""
def dump_insns(insns):
    output = []
    for addr, ins in insns.items():
        entry = insns[addr]
        output.append(
           
        )
    return "\n".join(output)
"""

header = """\
/* AUTOGENERATED. DO NOT EDIT. */
#include "_pcode.h"
void pcode2c(CPUState *state, size_t breakpoint){
    uint8_t* register_space = state->reg; 
    uint8_t* unique_space = state->unique; 
    uint8_t* ram_space = state->ram;
    uint8_t* ram = ram_space; // TODO: remove this
    for(;;){
    switch(state->pc){"""

footer = """\
        default: assert(state->pc != -1); // Unexpected PC value
}}}"""


def fmt_arch_header(ctx):
    output = []
    for reg, vnode in ctx.registers.items():
        output.append(f"#define {reg} 0x{vnode.offset:x}")
    return "\n".join(output)
