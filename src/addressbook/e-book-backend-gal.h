/* -*- Mode: C; indent-tabs-mode: t; c-basic-offset: 8; tab-width: 8 -*- */
/* Copyright (C) 2000-2004 Novell, Inc. */

#ifndef __E_BOOK_BACKEND_GAL_H__
#define __E_BOOK_BACKEND_GAL_H__

#include "libedata-book/e-book-backend.h"
#include "exchange-component.h"

#ifdef SUNLDAP
/*   copy from openldap ldap.h   */
#define LDAP_RANGE(n,x,y)      (((x) <= (n)) && ((n) <= (y)))
#define LDAP_NAME_ERROR(n)     LDAP_RANGE((n), 0x20, 0x24)
#define LBER_USE_DER			0x01
#define LDAP_CONTROL_PAGEDRESULTS      "1.2.840.113556.1.4.319"
#endif

typedef struct _EBookBackendGALPrivate EBookBackendGALPrivate;

typedef struct {
	EBookBackend             parent_object;
	EBookBackendGALPrivate *priv;
} EBookBackendGAL;

typedef struct {
	EBookBackendClass parent_class;
} EBookBackendGALClass;

EBookBackend *e_book_backend_gal_new      (void);
GType       e_book_backend_gal_get_type (void);

#define E_TYPE_BOOK_BACKEND_GAL        (e_book_backend_gal_get_type ())
#define E_BOOK_BACKEND_GAL(o)          (G_TYPE_CHECK_INSTANCE_CAST ((o), E_TYPE_BOOK_BACKEND_GAL, EBookBackendGAL))
#define E_BOOK_BACKEND_GAL_CLASS(k)    (G_TYPE_CHECK_CLASS_CAST ((k), E_TYPE_BOOK_BACKEND_GAL, EBookBackendGALClass))
#define E_IS_BOOK_BACKEND_GAL(o)       (G_TYPE_CHECK_INSTANCE_TYPE ((o), E_TYPE_BOOK_BACKEND_GAL))
#define E_IS_BOOK_BACKEND_GAL_CLASS(k) (G_TYPE_CHECK_CLASS_TYPE ((k), E_TYPE_BOOK_BACKEND_GAL))

#endif /* ! __E_BOOK_BACKEND_GAL_H__ */

