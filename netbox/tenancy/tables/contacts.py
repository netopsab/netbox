import django_tables2 as tables
from django_tables2.utils import Accessor

from netbox.tables import NetBoxTable, columns
from tenancy.models import *
from utilities.tables import linkify_phone

__all__ = (
    'ContactAssignmentTable',
    'ContactGroupTable',
    'ContactRoleTable',
    'ContactTable',
)


class ContactGroupTable(NetBoxTable):
    name = columns.MPTTColumn(
        linkify=True
    )
    contact_count = columns.LinkedCountColumn(
        viewname='tenancy:contact_list',
        url_params={'group_id': 'pk'},
        verbose_name='Contacts'
    )
    tags = columns.TagColumn(
        url_name='tenancy:contactgroup_list'
    )

    class Meta(NetBoxTable.Meta):
        model = ContactGroup
        fields = (
            'pk', 'name', 'contact_count', 'description', 'slug', 'tags', 'created', 'last_updated', 'actions',
        )
        default_columns = ('pk', 'name', 'contact_count', 'description')


class ContactRoleTable(NetBoxTable):
    name = tables.Column(
        linkify=True
    )
    tags = columns.TagColumn(
        url_name='tenancy:contactrole_list'
    )

    class Meta(NetBoxTable.Meta):
        model = ContactRole
        fields = ('pk', 'name', 'description', 'slug', 'tags', 'created', 'last_updated', 'actions')
        default_columns = ('pk', 'name', 'description')


class ContactTable(NetBoxTable):
    name = tables.Column(
        linkify=True
    )
    group = tables.Column(
        linkify=True
    )
    phone = tables.Column(
        linkify=linkify_phone,
    )
    comments = columns.MarkdownColumn()
    assignment_count = columns.LinkedCountColumn(
        viewname='tenancy:contactassignment_list',
        url_params={'contact_id': 'pk'},
        verbose_name='Assignments'
    )
    tags = columns.TagColumn(
        url_name='tenancy:contact_list'
    )

    class Meta(NetBoxTable.Meta):
        model = Contact
        fields = (
            'pk', 'name', 'group', 'title', 'phone', 'email', 'address', 'link', 'description', 'comments',
            'assignment_count', 'tags', 'created', 'last_updated',
        )
        default_columns = ('pk', 'name', 'group', 'assignment_count', 'title', 'phone', 'email')


class ContactAssignmentTable(NetBoxTable):
    content_type = columns.ContentTypeColumn(
        verbose_name='Object Type'
    )
    object = tables.Column(
        linkify=True,
        orderable=False
    )
    contact = tables.Column(
        linkify=True
    )
    role = tables.Column(
        linkify=True
    )
    contact_title = tables.Column(
        accessor=Accessor('contact__title'),
        verbose_name='Contact Title'
    )
    contact_phone = tables.Column(
        accessor=Accessor('contact__phone'),
        verbose_name='Contact Phone'
    )
    contact_email = tables.Column(
        accessor=Accessor('contact__email'),
        verbose_name='Contact Email'
    )
    contact_address = tables.Column(
        accessor=Accessor('contact__address'),
        verbose_name='Contact Address'
    )
    contact_link = tables.Column(
        accessor=Accessor('contact__link'),
        verbose_name='Contact Link'
    )
    contact_description = tables.Column(
        accessor=Accessor('contact__description'),
        verbose_name='Contact Description'
    )
    actions = columns.ActionsColumn(
        actions=('edit', 'delete')
    )

    class Meta(NetBoxTable.Meta):
        model = ContactAssignment
        fields = (
            'pk', 'content_type', 'object', 'contact', 'role', 'priority', 'contact_title', 'contact_phone',
            'contact_email', 'contact_address', 'contact_link', 'contact_description', 'actions'
        )
        default_columns = (
            'pk', 'content_type', 'object', 'contact', 'role', 'priority', 'contact_email', 'contact_phone'
        )
