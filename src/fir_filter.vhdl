library IEEE;
  use IEEE.STD_LOGIC_1164.all;
  use IEEE.NUMERIC_STD.all;

entity tt_um_hammal_fir_filter is
  generic (
    TAPS : integer := 3
  );
  port (
    ui_in   : in  std_logic_vector(7 downto 0);
    uo_out  : out std_logic_vector(7 downto 0);
    uio_in  : in  std_logic_vector(7 downto 0);
    uio_out : out std_logic_vector(7 downto 0);
    uio_oe  : out std_logic_vector(7 downto 0);
    ena     : in  std_logic;
    clk     : in  std_logic;
    rst_n   : in  std_logic
  );
end entity;

architecture Behavioral of tt_um_hammal_fir_filter is
  type coeffs is array (0 to TAPS - 1) of signed(5 downto 0);
  type delay_chain is array (0 to TAPS - 1) of signed(5 downto 0);

  signal h       : coeffs;                                     -- Filter coefficients
  signal reg     : delay_chain := (others => (others => '0')); -- Delay line
  signal acc     : signed(11 + TAPS downto 0);                 -- Accumulator for convolution sum
  signal load    : std_logic;                                  -- Load filter coefficients signal
  signal sat_pos : std_logic;                                  -- Saturation flags
  signal sat_neg : std_logic;

begin

  process (clk, rst_n)
    variable acc_var : signed(11 + TAPS downto 0);
    -- variable i : integer;
  begin
    if rst_n = '0' then
      reg <= (others => (others => '0'));
      acc <= (others => '0');
      for i in 0 to TAPS - 1 loop
        h(i) <= to_signed(1, 6); -- Example: all coefficients set to 1
      end loop;
    elsif rising_edge(clk) then
      if load = '1' then
        -- Load new coefficients from reg
        for i in 0 to TAPS - 1 loop
          h(i) <= reg(i);
          reg(i) <= (others => '0');
        end loop;
      else

        -- Shift the delay line
        for i in TAPS - 1 downto 1 loop
          reg(i) <= reg(i - 1);
        end loop;
        reg(0) <= signed(ui_in(5 downto 0));

        -- Compute the convolution sum
        acc_var := (others => '0');
        for i in 0 to TAPS - 1 loop
          acc_var := acc_var + (reg(i) * h(i));
        end loop;
        acc <= acc_var;
      end if;
    end if;
  end process;

  -- sat_pos <= '1' when acc > to_signed(31, acc'length) else '0';
  -- sat_neg <= '1' when acc < to_signed(- 32, acc'length) else '0';

  uo_out  <= "00" & std_logic_vector(resize(acc, 6));
  -- uo_out  <= "00011111" when sat_pos = '1' else "00100000" when sat_neg = '1' else "00" & std_logic_vector(resize(acc, 6));
  uio_out <= "00000000";
  uio_oe  <= "00000000";
  load    <= uio_in(0); -- Load filter coefficients signal
end architecture;
