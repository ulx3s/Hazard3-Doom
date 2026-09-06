Configuration, SPI Flash, USB DFU, and JTAG
===========================================

ULX4M has several programming and boot paths. They solve different problems and
should not be treated as interchangeable.

Three layers to keep separate
-----------------------------

``Board DFU bootloader``
   Persistent FPGA configuration/firmware stored near the start of SPI flash.
   It provides USB DFU access and normally transfers control to the user image.

``Hazard3-Doom FPGA user bitstream``
   The ECP5 configuration containing the Hazard3 SoC, memory interface, video,
   resident monitor preload, and board integration.

``Hazard3 resident monitor / Doom image``
   RISC-V software executed after the FPGA is configured. Rebuilding this
   software does not imply replacing the board DFU bootloader.

See :doc:`../../user-guide/bootloader` for the recovery procedure and
:doc:`../../getting-started/programming` for normal FPGA programming.

SPI flash organization
----------------------

The upstream ULX4M bootloader documentation describes the first 2 MiB of flash
(``0x000000`` through ``0x1fffff``) as the bootloader/protected area and the
normal user bitstream beginning at ``0x200000``.

That separation is one reason Hazard3-Doom documentation strongly discourages
bootloader replacement during normal development. Most FPGA experiments belong
in SRAM or the normal user-image area, not in the protected boot region.

USB DFU
-------

The upstream bootloader enumerates with VID:PID ``1d50:614b``. Hazard3-Doom
uses DFU alternate setting 0 for the normal user bitstream. A typical project
programming command uses ``openFPGALoader`` with the DFU VID/PID and altsetting
explicitly selected.

The current repository also contains a guided ``scripts/ulx4m-bootloader.sh``
workflow for the unusual case where the bootloader itself must be built,
validated in SRAM, installed, or recovered.

.. warning::

   Do not replace a working DFU bootloader just because a Hazard3-Doom bitstream,
   memory profile, or resident monitor changed. Bootloader replacement is a
   recovery/bootloader-development operation.

JTAG
----

ULX4M publishes both an external JTAG path and JTAG-over-GPIO arrangements. In
Hazard3-Doom, JTAG also has two conceptual layers:

* ECP5 configuration/debug access to the FPGA device; and
* the Hazard3 RISC-V Debug Module/DTM reached through the ECP5 JTAG machinery.

The project includes OpenOCD configurations for ULX4M and Tigard-based setups.
For the current ULX4M-LD 85F target the ECP5 device IDCODE used by the project is
``0x01113043``.

SRAM versus flash testing
-------------------------

When validating a new route, memory profile, or risky FPGA change, loading the
bitstream into FPGA SRAM is preferable when the available programmer supports
it. A power cycle then restores the persistent configuration path. Flash the
user image only after the bitstream has passed the intended bring-up tests.
