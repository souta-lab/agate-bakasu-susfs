// SPDX-License-Identifier: GPL-2.0
/*
 * Compile-only demonstration of translating 5.10+ inode-event callback
 * parameters to the 4.14 vendor fsnotify_ops.handle_event signature.
 *
 * No active listener/group registration, mount changes, filesystem
 * filtering, or security state changes are performed by this file.
 */
#include <linux/compiler.h>
#include <linux/dcache.h>
#include <linux/fsnotify_backend.h>
#include <linux/limits.h>
#include <linux/string.h>
#include <linux/susfs23_fsnotify_compat_414.h>

int __weak susfs23_fsnotify_compat_observe_414(struct inode *inode, u32 mask,
					       const struct qstr *name,
					       u32 cookie)
{
	return 0;
}

static int susfs23_handle_event_414(struct fsnotify_group *group,
				    struct inode *inode,
				    struct fsnotify_mark *inode_mark,
				    struct fsnotify_mark *vfsmount_mark,
				    u32 mask, const void *data, int data_type,
				    const unsigned char *file_name, u32 cookie,
				    struct fsnotify_iter_info *iter_info)
{
	struct qstr name;
	size_t n;

	/* The newer ABI passes struct qstr; the 4.14 ABI uses a C string. */
	if (!file_name || !inode_mark)
		return 0;

	n = strnlen((const char *)file_name, NAME_MAX);
	if (!n || n >= NAME_MAX)
		return 0;

	name.name = file_name;
	name.len = n;
	name.hash = 0;
	return susfs23_fsnotify_compat_observe_414(inode, mask, &name, cookie);
}

const struct fsnotify_ops susfs23_fsnotify_compat_ops_414 = {
	.handle_event = susfs23_handle_event_414,
};
