/*
 * pdebug.h
 *
 *  Created on: 11 апр. 2019 г.
 *      Author: user
 */

#ifndef LOGGING_H_
#define LOGGING_H_
//#include "common.h"

#ifdef __KERNEL__
#   include <linux/module.h>
//#   include <linux/delay.h>

    /* This one if debugging is on, and kernel space */
#   define LOGOUT(lvl, fmt, args...) printk(lvl "%s [task=%p] %s: " fmt, THIS_MODULE->name, current, __func__, ## args)//, mdelay(300)
#else
#   include <stdio.h>
    /* This one for user space */
#   define KERN_INFO ""
#   define LOGOUT(lvl, fmt, args...) fprintf(stdout,lvl fmt, ## args)
#endif

#undef PDEBUG             /* undef it, just in case */

#ifdef PARANOID
#  define PDEBUG(fmt, args...) LOGOUT(KERN_DEBUG, fmt, ## args)
#else
#  define PDEBUG(fmt, args...) /* not debugging: nothing */
#endif

#define PINFO(fmt, args...) LOGOUT(KERN_INFO, fmt, ## args)
#define PNOTICE(fmt, args...) LOGOUT(KERN_NOTICE, fmt, ## args)
#define PWARN(fmt, args...) LOGOUT(KERN_WARNING, fmt, ## args)
#define PERROR(fmt, args...) LOGOUT(KERN_ERR, fmt, ## args)
#define PCRIT(fmt, args...) LOGOUT(KERN_CRIT, fmt, ## args)

#endif /* LOGGING_H_ */
