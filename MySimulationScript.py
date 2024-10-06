from m5.objects import System, X86IntelMPIO, TimingSimpleCPU, DDR3_1600_8x8, SimpleMemory, AddrRange, Root
from m5.util import addToPath

addToPath('../common')
from Caches import *

system = System()

# Set up the system clock
system.clk_domain = SrcClockDomain()
system.clk_domain.clock = '1GHz'
system.clk_domain.voltage_domain = VoltageDomain()

system.mem_mode = 'timing'
system.mem_ranges = [AddrRange('512MB')]

# Setup CPU
system.cpu = TimingSimpleCPU()

# Setup memory
system.membus = SystemXBar()
system.memory = SimpleMemory(latency='10ns', bandwidth='100GB/s')

# Configure the CPU caches
system.cpu.icache = L1ICache(opts)
system.cpu.dcache = L1DCache(opts)
system.cpu.icache.connectCPU(system.cpu)
system.cpu.dcache.connectCPU(system.cpu)

# Connect the cache to the memory bus
system.l2bus = L2XBar()
system.cpu.icache.connectBus(system.l2bus)
system.cpu.dcache.connectBus(system.l2bus)

# Setup L2 cache
system.l2cache = L2Cache(opts)
system.l2cache.connectCPUSideBus(system.l2bus)
system.l2cache.connectMemSideBus(system.membus)

# Connect the system up with a memory controller
system.mem_ctrl = DDR3_1600_8x8()
system.mem_ctrl.range = system.mem_ranges[0]
system.mem_ctrl.port = system.membus.master

# Set up the root SimObject and start the simulation
root = Root(full_system = False, system = system)
m5.instantiate()

print("Beginning simulation!")
exit_event = m5.simulate()
print('Exiting @ tick %i because %s' % (m5.curTick(), exit_event.getCause()))
