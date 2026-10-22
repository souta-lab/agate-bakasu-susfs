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

/*
 * Generic 4.14 fsnotify lifecycle helpers. Caller owns an inode reference
 * throughout registration and holds the returned mark's initial reference
 * until remove_inode_mark_414(). No watchers are created automatically.
 */
struct fsnotify_group *susfs23_fsnotify_compat_create_group_414(void);
int susfs23_fsnotify_compat_add_inode_mark_414(struct fsnotify_group *group,
					      struct inode *inode, u32 mask,
					      struct fsnotify_mark **out);
void susfs23_fsnotify_compat_remove_inode_mark_414(
					      struct fsnotify_mark **mark);
void susfs23_fsnotify_compat_destroy_group_414(struct fsnotify_group *group);

/* Optional generic observer; no action is taken by the default stub. */
int susfs23_fsnotify_compat_observe_414(struct inode *inode, u32 mask,
				      const struct qstr *name, u32 cookie);
#endif
