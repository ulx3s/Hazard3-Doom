Overview and Board Variants
===========================

What ULX4M is
-------------

ULX4M is a family of open-hardware FPGA system-on-module boards intended to fit
carrier boards using the Raspberry Pi Compute Module 4 mechanical/connector
format. The module can also be used in arrangements where its own USB,
programming, and exposed interfaces are sufficient.

The family follows the ULX3S idea - an accessible ECP5 development platform -
but moves it into a compact module format and exposes additional high-speed
connectivity. The two names used throughout the project are:

``ULX4M-LS``
   Lattice ECP5 plus external single-data-rate SDR SDRAM.

``ULX4M-LD``
   Lattice ECP5 plus external DDR3/DDR3L. Hazard3-Doom uses LiteDRAM and the
   ECP5 DDR PHY on this target.

Published specifications are revision-sensitive
------------------------------------------------

There is no single table on the Internet that safely describes every ULX4M ever
built. The public sources describe different revisions and component choices.
That is normal for an open-hardware project that evolved over time, but it means
part numbers must be tied to a source or a physical board.

.. list-table:: Examples found in public ULX4M material
   :header-rows: 1
   :widths: 22 26 26 26

   * - Source/variant
     - Memory described
     - Ethernet described
     - Interpretation
   * - Crowd Supply ULX4M-LS
     - 64 MiB ``IS42S16320D-6BLI``
     - ``KSZ9031RNXCA``
     - Campaign/project description for the promoted LS configuration.
   * - Upstream ULX4M-LS user-manual page
     - 32 MiB ``IS42S16160G-7BL``
     - ``LAN8720A``
     - Documents an earlier/different LS population.
   * - Crowd Supply ULX4M-LD
     - 1 GiB ``MT41K512M16HA-125``
     - ``KSZ9031RNXCA``
     - Matches the Micron 8-Gbit class supported by current Hazard3-Doom profiles.
   * - Upstream ULX4M-LD user-manual page
     - 512 MiB ``MT41K256M16TW-107``
     - ``KSZ9031RNXCA``
     - Documents another LD population/revision.
   * - Hazard3-Doom current LD profiles
     - ``MT41K512M16HA`` or ``AS4C256M16D3``
     - Not used by the current Doom design
     - Project-supported DDR controller profiles, not a claim that all boards use either device.

This is why this manual does not reduce ULX4M to "the 1 GB board" or "the 32 MB
board." Identify the hardware first, then select the matching build profile.

Hazard3-Doom target summary
---------------------------

The current project board profiles are summarized below. See
:doc:`../../reference/board-profiles` for the release qualification record.

.. list-table::
   :header-rows: 1
   :widths: 20 20 24 18 18

   * - Target
     - FPGA/build class
     - External memory path
     - Hazard3 clock
     - Project status
   * - ULX4M-LS 85F
     - ECP5 85K build
     - 16-bit SDR SDRAM through the native project SDR controller
     - 50 MHz
     - Supported build path; verify board population/revision.
   * - ULX4M-LD 85F
     - ``LFE5UM-85F-8BG381C``
     - x16 DDR3 through LiteDRAM/``ECP5DDRPHY``
     - 40 MHz
     - Hardware-qualified with the Micron 8-Gbit profile; Alliance profile is also generated/supported.

The LS build requires the 85K-class FPGA for the current Hazard3-Doom resource
configuration. The common smaller LS population is useful for many ULX4M
examples, but the present Doom configuration consumes more ECP5 block RAM than
the 12K device can provide.

Board-level resources
---------------------

Across the ULX4M family, published designs expose a broad set of resources:

* ECP5 FPGA and external SDR or DDR3 memory;
* 128-Mbit class SPI configuration flash in common published populations;
* USB DFU bootloader/programming path;
* external JTAG and JTAG-over-GPIO options;
* GPDI video outputs;
* micro-SD connectivity through the CM4-style interface;
* Ethernet hardware on documented variants;
* CSI/DSI-style camera/display connectors;
* GPIO, buttons, DIP switches, and LEDs; and
* SerDes/PCIe/high-speed connections where the fitted ECP5 device provides the
  required SerDes capability and the board revision routes it.

Do not read that list as a statement that Hazard3-Doom currently drives all of
those interfaces. The current design concentrates on the CPU, external memory,
HDMI/GPDI video, UART/JTAG debug, programming/boot paths, and ongoing SD-card
integration.

Board tour: follow the data
---------------------------

A useful way to inspect a ULX4M is to follow one transaction instead of naming
components in isolation. A Doom load from external memory follows roughly this
path on ULX4M-LD:

.. code-block:: text

   Hazard3 load/store
          |
          v
      AHB5 fabric
          |
          v
   ahb_litedram.v
          |
      clock-domain crossing
          |
          v
   128-bit LiteDRAM Wishbone user port
          |
          v
   LiteDRAM controller + ECP5DDRPHY
          |
          v
   ECP5 package pins / SSTL I/O
          |
          v
   x16 DDR3 device on the module

The same software-visible load on ULX4M-LS reaches the native SDR controller
instead. That contrast is one of the most useful educational features of the
ULX4M family: the CPU can stay almost unchanged while the board-level memory
implementation changes substantially.
