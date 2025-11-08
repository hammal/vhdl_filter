# SPDX-FileCopyrightText: © 2024 Tiny Tapeout
# SPDX-License-Identifier: Apache-2.0

import cocotb
from cocotb.clock import Clock
from cocotb.triggers import ClockCycles
import pickle


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
    TAPS = 5
    SIZE = 100
    with open("test_data.pkl", "rb") as f:
        data = pickle.load(f)
    seq = data["seq"]
    # seq = -np.ones(SIZE, dtype=int)
    # seq[SIZE//2:] = 0
    # h = np.ones(TAPS, dtype=int)  # Simple moving average filter coefficients
    h = data["h"]
    y = data["y"]
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
