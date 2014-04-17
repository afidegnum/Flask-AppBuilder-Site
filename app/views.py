from flask import render_template, redirect
from flask.ext.appbuilder.baseapp import BaseApp
from flask.ext.appbuilder.models.datamodel import SQLAModel
from flask.ext.appbuilder.views import MasterDetailView, GeneralView, IndexView
from flask.ext.appbuilder.baseviews import expose
from flask.ext.appbuilder.charts.views import ChartView, TimeChartView
from flask.ext.babelpkg import lazy_gettext as _

from app import app, db
from models import Group, Gender, Contact


def fill_gender():
    try:
        db.session.add(Gender(name='Male'))
        db.session.add(Gender(name='Female'))
        db.session.commit()
    except:
        db.session.rollback()


class FABView(IndexView):
    """
        A simple view that implements the index for the site
    """
    index_template = 'index.html'


class ContactUsView(IndexView):
    route_base = "/contacts"
    index_template = 'contactus.html'
    @expose('/')
    def index(self):
        return render_template(self.index_template, baseapp = self.baseapp)


class ContactGeneralView(GeneralView):
    datamodel = SQLAModel(Contact, db.session)

    label_columns = {'group': 'Contacts Group'}
    list_columns = ['name', 'personal_celphone', 'birthday', 'group']

    base_order = ('name', 'asc')

    show_fieldsets = [
        ('Summary', {'fields': ['name', 'gender', 'group']}),
        (
            'Personal Info',
            {'fields': ['address', 'birthday', 'personal_phone', 'personal_celphone'], 'expanded': False}),
    ]

    add_fieldsets = [
        ('Summary', {'fields': ['name', 'gender', 'group']}),
        (
            'Personal Info',
            {'fields': ['address', 'birthday', 'personal_phone', 'personal_celphone'], 'expanded': False}),
    ]

    edit_fieldsets = [
        ('Summary', {'fields': ['name', 'gender', 'group']}),
        (
            'Personal Info',
            {'fields': ['address', 'birthday', 'personal_phone', 'personal_celphone'], 'expanded': False}),
    ]

class ContactChartView(ChartView):
    chart_title = 'Grouped contacts'
    label_columns = ContactGeneralView.label_columns
    group_by_columns = ['group', 'gender']
    datamodel = SQLAModel(Contact, db.session)


class ContactTimeChartView(TimeChartView):
    chart_title = 'Grouped Birth contacts'
    chart_type = 'AreaChart'
    label_columns = ContactGeneralView.label_columns
    group_by_columns = ['birthday']
    datamodel = SQLAModel(Contact, db.session)


class GroupGeneralView(GeneralView):
    datamodel = SQLAModel(Group, db.session)
    related_views = [ContactGeneralView]
    #show_template = 'appbuilder/general/model/show_cascade.html'

class ThemesView(IndexView):
    route_base = "/themes"
    index_template = 'contactus.html'
    @expose('/<theme>')
    def index(self, theme):
        if theme:
            self.baseapp.app_theme = "%s.css" % (theme)
        else:
            self.baseapp.app_them = ''
        return redirect(self._get_redirect())
        
        
class GroupMasterView(MasterDetailView):
    datamodel = SQLAModel(Group, db.session)
    related_views = [ContactGeneralView]

fixed_translations_import = [
    _("List Groups"),
    _("List Contacts"),
    _("Contacts Chart"),
    _("Contacts Birth Chart")]


fill_gender()
genapp = BaseApp(app, db, indexview = FABView)

genapp.add_view(GroupGeneralView(), "List Groups", icon="fa-folder-open-o", category="Contacts")
genapp.add_view(GroupMasterView(), "Master Detail Groups", icon="fa-folder-open-o", category="Contacts")
genapp.add_view(ContactGeneralView(), "List Contacts", icon="fa-envelope", category="Contacts")
genapp.add_separator("Contacts")
genapp.add_view(ContactChartView(), "Contacts Chart", icon="fa-dashboard", category="Contacts")
genapp.add_view(ContactTimeChartView(), "Contacts Birth Chart", icon="fa-dashboard", category="Contacts")

genapp.add_view_no_menu(ThemesView())

genapp.add_link(name="Cerulean", href="/themes/cerulean",icon="fa-external-link", category="Themes")
genapp.add_link(name="Amelia", href="/themes/amelia",icon="fa-external-link", category="Themes")
genapp.add_link(name="Flatly", href="/themes/flatly",icon="fa-external-link", category="Themes")
genapp.add_link(name="Journal", href="/themes/journal",icon="fa-external-link", category="Themes")
genapp.add_link(name="Readable", href="/themes/readable",icon="fa-external-link", category="Themes")
genapp.add_link(name="Simplex", href="/themes/simplex",icon="fa-external-link", category="Themes")
genapp.add_link(name="Slate", href="/themes/slate",icon="fa-external-link", category="Themes")
genapp.add_link(name="Spacelab", href="/themes/spacelab",icon="fa-external-link", category="Themes")
genapp.add_link(name="United", href="/themes/united",icon="fa-external-link", category="Themes")
genapp.add_link(name="Default", href="/themes/",icon="fa-external-link", category="Themes")

