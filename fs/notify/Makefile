# SPDX-License-Identifier: GPL-2.0
obj-$(CONFIG_FSNOTIFY)		+= fsnotify.o notification.o group.o mark.o \
				   fdinfo.o

obj-y			+= dnotify/
obj-y			+= inotify/
obj-y			+= fanotify/

# Optional, standalone non-registered 4.14 ABI compatibility helper.
obj-$(CONFIG_SUSFS23_FSNOTIFY_ABI_414) += susfs23_fsnotify_compat_414.o
