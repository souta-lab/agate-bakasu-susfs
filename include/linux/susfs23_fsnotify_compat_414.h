/* SPDX-License-Identifier: GPL-2.0 */
/*
 * Linux 4.14 fsnotify callback ABI adapter.
 * Standalone compatibility shim for evaluating v2.3 source API differences.
 */
#ifndef _LINUX_SUSFS23_FSNOTIFY_COMPAT_414_H
#define _LINUX_SUSFS23_FSNOTIFY_COMPAT_414_H
#include <linux/fsnotify_backend.h>
#include <linux/dcache.h>

extern const struct fsnotify_ops susfs23_fsnotify_compat_ops_414;

/* Optional generic observer; no action is taken by the default stub. */
int susfs23_fsnotify_compat_observe_414(struct inode *inode, u32 mask,
				      const struct qstr *name, u32 cookie);
#endif
