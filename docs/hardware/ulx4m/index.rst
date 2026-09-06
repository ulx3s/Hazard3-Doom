ULX4M Hardware Guide
====================

**Architecture, components, interfaces, and their use by Hazard3-Doom.**

The ULX4M is much more than the FPGA that runs Hazard3. It is a modular,
open-hardware computing platform containing a Lattice ECP5 FPGA, external
memory, SPI configuration flash, video and high-speed interfaces, removable
storage connections, debugging/programming paths, and two high-density
CM4-compatible expansion connectors.

Understanding how those parts are connected makes the Hazard3-Doom design much
easier to understand. This guide follows signals from physical board components
through FPGA pins and constraints, into Verilog and memory controllers, and,
where appropriate, all the way to software running on the Hazard3 CPU.

.. important::

   This is a Hazard3-Doom hardware guide, not an authoritative replacement for
   the ULX4M manufacturer's documentation. Always verify the PCB revision and
   fitted components on the board in front of you before relying on a part
   number, memory capacity, power assumption, or pin assignment.

The distinction matters because published ULX4M sources describe multiple board
revisions and component populations. For example, public material has described
both 32/64 MiB SDRAM configurations for ULX4M-LS and several DDR3 populations
for ULX4M-LD. Hazard3-Doom therefore treats the board revision and fitted memory
part as configuration inputs rather than assuming every ULX4M is identical.

.. toctree::
   :maxdepth: 2

   overview-and-variants
   fpga-and-clocking
   memory
   boot-and-flash
   video-and-storage
   interfaces
   pinout-and-revisions
   sources

A useful mental model
---------------------

.. code-block:: text

   +---------------------------------------------------------------+
   | Carrier board / external world                                |
   | USB, display, SD, Ethernet, PCIe/SerDes, GPIO, power          |
   +-------------------------------+-------------------------------+
                                   |
                         CM4-compatible connectors
                                   |
   +-------------------------------v-------------------------------+
   | ULX4M module                                                  |
   |                                                               |
   |  +-------------+       +------------------+                   |
   |  | SPI flash   |<----->| Lattice ECP5     |<----> GPDI/video  |
   |  +-------------+       | FPGA             |<----> JTAG/USB    |
   |                        |                  |<----> SD/GPIO     |
   |  +-------------+       | Hazard3 SoC      |<----> SerDes      |
   |  | SDR/DDR3    |<----->| + controllers    |                   |
   |  +-------------+       +------------------+                   |
   +---------------------------------------------------------------+

Hazard3-Doom does not use every available ULX4M peripheral today. The guide
therefore separates **hardware present on the board** from **hardware currently
implemented or qualified by Hazard3-Doom**.
