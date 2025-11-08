# SPDX-FileCopyrightText: © 2024 Tiny Tapeout
# SPDX-License-Identifier: Apache-2.0

import cocotb
from cocotb.clock import Clock
from cocotb.triggers import ClockCycles


async def reset(dut):
    # Reset
    dut._log.info("Reset")
    dut.ui_in.value = 0
    dut.uio_in.value = 0
    dut.rst_n.value = 0
    await ClockCycles(dut.clk, 10)
    dut.rst_n.value = 1


@cocotb.test()
async def test_project(dut):
    dut._log.info("Start")

    # Set the clock period to 10 us (100 KHz)
    clock = Clock(dut.clk, 10, unit="us")
    cocotb.start_soon(clock.start())

    # Enable pin
    dut.ena.value = 1

    # reset
    await reset(dut)  # Await the reset function

    dut._log.info("Test project behavior")

    # Test coefficients one by one
    TAPS = 3
    SIZE = 100
    seq = [
        -3,
        1,
        3,
        -2,
        1,
        0,
        3,
        -1,
        -4,
        3,
        0,
        1,
        2,
        -3,
        -4,
        -2,
        -3,
        -1,
        1,
        -3,
        1,
        -4,
        2,
        1,
        -1,
        0,
        -4,
        -1,
        1,
        0,
        -2,
        -1,
        -2,
        2,
        -4,
        -4,
        -2,
        2,
        -3,
        2,
        -2,
        -1,
        0,
        -3,
        1,
        -2,
        2,
        1,
        2,
        -3,
        -3,
        3,
        0,
        3,
        1,
        -3,
        3,
        3,
        -2,
        -2,
        2,
        3,
        1,
        2,
        -4,
        0,
        -4,
        -4,
        -1,
        1,
        3,
        -1,
        -3,
        -1,
        -2,
        -2,
        -3,
        -1,
        0,
        -4,
        -1,
        -4,
        -3,
        -3,
        3,
        3,
        3,
        2,
        0,
        1,
        0,
        3,
        3,
        -3,
        0,
        -4,
        -3,
        -3,
        -3,
        -3,
    ]
    # seq = -np.ones(SIZE, dtype=int)
    # seq[SIZE//2:] = 0
    # h = np.ones(TAPS, dtype=int)  # Simple moving average filter coefficients
    h = [-4, 3, -2]
    y = [
        12,
        -13,
        -3,
        15,
        -16,
        7,
        -14,
        13,
        7,
        -22,
        17,
        -10,
        -5,
        16,
        3,
        2,
        14,
        -1,
        -1,
        17,
        -15,
        25,
        -22,
        10,
        3,
        -5,
        18,
        -8,
        1,
        5,
        6,
        -2,
        9,
        -12,
        26,
        0,
        4,
        -6,
        22,
        -21,
        20,
        -6,
        1,
        14,
        -13,
        17,
        -16,
        6,
        -9,
        16,
        -1,
        -15,
        15,
        -18,
        5,
        9,
        -23,
        3,
        11,
        -4,
        -10,
        -2,
        1,
        -11,
        20,
        -16,
        24,
        4,
        0,
        1,
        -7,
        11,
        3,
        -3,
        11,
        4,
        10,
        -1,
        3,
        18,
        -8,
        21,
        2,
        11,
        -15,
        3,
        -9,
        -5,
        0,
        -8,
        3,
        -14,
        -3,
        15,
        -15,
        22,
        0,
        11,
        9,
        9,
    ]
    print(y)
    # Load coefficients
    for i in range(TAPS):
        # await FallingEdge(dut.clk)
        dut.ui_in.value = int(h[-1 - i])
        await ClockCycles(dut.clk, 1)
    dut.uio_in.value = 1
    dut.ui_in.value = 0
    await ClockCycles(dut.clk, 1)
    dut.uio_in.value = 0

    for i in range(SIZE):
        dut.ui_in.value = int(seq[i])
        await ClockCycles(dut.clk, 1)
        if i > 2:
            signed_value = int(dut.uo_out.value) & 0b111111  # Take only 6 bits
            if signed_value >= 32:
                signed_value -= 64
            assert signed_value == int(
                y[i - 2]
            ), f"At index {i-2}, expected {y[i-2]}, got {signed_value}"
            dut._log.info(
                f"At index {i-2}, input: {seq[i]}, expected output: {y[i-2]}, got: {dut.uo_out.value}"
            )
