TARGETS = mountkernfs.sh hostname.sh mountdevsubfs.sh procps hwclock.sh urandom networking checkroot.sh checkfs.sh mountall.sh checkroot-bootclean.sh bootmisc.sh mountall-bootclean.sh mountnfs-bootclean.sh mountnfs.sh
INTERACTIVE = checkroot.sh checkfs.sh
mountdevsubfs.sh: mountkernfs.sh
procps: mountkernfs.sh
hwclock.sh: mountdevsubfs.sh
urandom: hwclock.sh
networking: mountkernfs.sh urandom procps
checkroot.sh: hwclock.sh mountdevsubfs.sh hostname.sh
checkfs.sh: checkroot.sh
mountall.sh: checkfs.sh checkroot-bootclean.sh
checkroot-bootclean.sh: checkroot.sh
bootmisc.sh: checkroot-bootclean.sh mountall-bootclean.sh mountnfs-bootclean.sh
mountall-bootclean.sh: mountall.sh
mountnfs-bootclean.sh: mountnfs.sh
mountnfs.sh: networking
