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
#include <linux/stringhash.h>
#include <linux/slab.h>
#include <linux/err.h>
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

	/* NAME_MAX bytes is a legal filename; accept it if terminated. */
	n = strnlen((const char *)file_name, NAME_MAX + 1);
	if (!n || n > NAME_MAX)
		return 0;

	name.name = file_name;
	name.len = n;
	/*
	 * The parent dentry is unavailable in this callback signature.
	 * Hash using the unsalted API; a consumer must not assume this hash
	 * is suitable for a parent-specific dcache lookup.
	 */
	name.hash = full_name_hash(NULL, (const char *)file_name, n);
	return susfs23_fsnotify_compat_observe_414(inode, mask, &name, cookie);
}


static void susfs23_fsnotify_free_mark_414(struct fsnotify_mark *mark)
{
	/* fsnotify calls this only after its SRCU grace period. */
	kfree(mark);
}

const struct fsnotify_ops susfs23_fsnotify_compat_ops_414 = {
	.handle_event = susfs23_handle_event_414,
	.free_mark = susfs23_fsnotify_free_mark_414,
};

struct fsnotify_group *susfs23_fsnotify_compat_create_group_414(void)
{
	return fsnotify_alloc_group(&susfs23_fsnotify_compat_ops_414);
}

int susfs23_fsnotify_compat_add_inode_mark_414(struct fsnotify_group *group,
					      struct inode *inode, u32 mask,
					      struct fsnotify_mark **out)
{
	struct fsnotify_mark *mark;
	int ret;

	if (!group || !inode || !out)
		return -EINVAL;
	*out = NULL;

	mark = kzalloc(sizeof(*mark), GFP_KERNEL);
	if (!mark)
		return -ENOMEM;

	fsnotify_init_mark(mark, group);
	mark->mask = mask;
	/* On 4.14, fsnotify_add_mark replaces fsnotify_add_inode_mark. */
	ret = fsnotify_add_mark(mark, inode, NULL, 0);
	if (ret) {
		/* Drop the initial reference. free_mark() owns final kfree. */
		fsnotify_put_mark(mark);
		return ret;
	}

	/* Caller owns the initial reference; the group owns its list ref. */
	*out = mark;
	return 0;
}

void susfs23_fsnotify_compat_remove_inode_mark_414(
					      struct fsnotify_mark **markp)
{
	struct fsnotify_mark *mark;

	if (!markp || !*markp)
		return;

	mark = *markp;
	*markp = NULL;
	/* Detach from inode/group, then release the caller's initial ref. */
	fsnotify_destroy_mark(mark, mark->group);
	fsnotify_put_mark(mark);
}

void susfs23_fsnotify_compat_destroy_group_414(struct fsnotify_group *group)
{
	if (group && !IS_ERR(group))
		fsnotify_destroy_group(group);
}
