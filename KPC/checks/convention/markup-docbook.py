# -*- coding: utf-8 -*-
# Docbook XML markup check

from xml.parsers.expat import ParserCreate
from xml.parsers.expat import ExpatError
from KPC.classes import Error, BaseCheck

# 메시지에 대해 XML 파서를 돌려 well formed인지 검사하고, 태그가 알려진
# DocBook 태그인지 검사한다.

# DocBook: The Definitive Guide 기준
# http://www.docbook.org/tdg/en/html/part2.html

known_db_tags = set([
    'abbrev',
    'abstract',
    'accel',
    'ackno',
    'acronym',
    'action',
    'address',
    'affiliation',
    'alt',
    'anchor',
    'answer',
    'appendix',
    'appendixinfo',
    'application',
    'area',
    'areaset',
    'areaspec',
    'arg',
    'article',
    'articleinfo',
    'artpagenums',
    'attribution',
    'audiodata',
    'audioobject',
    'author',
    'authorblurb',
    'authorgroup',
    'authorinitials',
    'beginpage',
    'bibliocoverage',
    'bibliodiv',
    'biblioentry',
    'bibliography',
    'bibliographyinfo',
    'biblioid',
    'bibliolist',
    'bibliomisc',
    'bibliomixed',
    'bibliomset',
    'biblioref',
    'bibliorelation',
    'biblioset',
    'bibliosource',
    'blockinfo',
    'blockquote',
    'book',
    'bookinfo',
    'bridgehead',
    'callout',
    'calloutlist',
    'caption',
    'caution',
    'chapter',
    'chapterinfo',
    'citation',
    'citebiblioid',
    'citerefentry',
    'citetitle',
    'city',
    'classname',
    'classsynopsis',
    'classsynopsisinfo',
    'cmdsynopsis',
    'co',
    'code',
    'col',
    'colgroup',
    'collab',
    'collabname',
    'colophon',
    'colspec',
    'command',
    'computeroutput',
    'confdates',
    'confgroup',
    'confnum',
    'confsponsor',
    'conftitle',
    'constant',
    'constraint',
    'constraintdef',
    'constructorsynopsis',
    'contractnum',
    'contractsponsor',
    'contrib',
    'copyright',
    'coref',
    'corpauthor',
    'corpcredit',
    'corpname',
    'country',
    'database',
    'date',
    'dedication',
    'destructorsynopsis',
    'edition',
    'editor',
    'email',
    'emphasis',
    'entry',
    'entrytbl',
    'envar',
    'epigraph',
    'equation',
    'errorcode',
    'errorname',
    'errortext',
    'errortype',
    'example',
    'exceptionname',
    'fax',
    'fieldsynopsis',
    'figure',
    'filename',
    'firstname',
    'firstterm',
    'footnote',
    'footnoteref',
    'foreignphrase',
    'formalpara',
    'funcdef',
    'funcparams',
    'funcprototype',
    'funcsynopsis',
    'funcsynopsisinfo',
    'function',
    'glossary',
    'glossaryinfo',
    'glossdef',
    'glossdiv',
    'glossentry',
    'glosslist',
    'glosssee',
    'glossseealso',
    'glossterm',
    'graphic',
    'graphicco',
    'group',
    'guibutton',
    'guiicon',
    'guilabel',
    'guimenu',
    'guimenuitem',
    'guisubmenu',
    'hardware',
    'highlights',
    'holder',
    'honorific',
    'html:form',
    'imagedata',
    'imageobject',
    'imageobjectco',
    'important',
    'index',
    'indexdiv',
    'indexentry',
    'indexinfo',
    'indexterm',
    'informalequation',
    'informalexample',
    'informalfigure',
    'informaltable',
    'initializer',
    'inlineequation',
    'inlinegraphic',
    'inlinemediaobject',
    'interface',
    'interfacename',
    'invpartnumber',
    'isbn',
    'issn',
    'issuenum',
    'itemizedlist',
    'itermset',
    'jobtitle',
    'keycap',
    'keycode',
    'keycombo',
    'keysym',
    'keyword',
    'keywordset',
    'label',
    'legalnotice',
    'lhs',
    'lineage',
    'lineannotation',
    'link',
    'listitem',
    'literal',
    'literallayout',
    'lot',
    'lotentry',
    'manvolnum',
    'markup',
    'mathphrase',
    'medialabel',
    'mediaobject',
    'mediaobjectco',
    'member',
    'menuchoice',
    'methodname',
    'methodparam',
    'methodsynopsis',
    'mml:math',
    'modespec',
    'modifier',
    'mousebutton',
    'msg',
    'msgaud',
    'msgentry',
    'msgexplan',
    'msginfo',
    'msglevel',
    'msgmain',
    'msgorig',
    'msgrel',
    'msgset',
    'msgsub',
    'msgtext',
    'nonterminal',
    'note',
    'objectinfo',
    'olink',
    'ooclass',
    'ooexception',
    'oointerface',
    'option',
    'optional',
    'orderedlist',
    'orgdiv',
    'orgname',
    'otheraddr',
    'othercredit',
    'othername',
    'package',
    'pagenums',
    'para',
    'paramdef',
    'parameter',
    'part',
    'partinfo',
    'partintro',
    'personblurb',
    'personname',
    'phone',
    'phrase',
    'pob',
    'postcode',
    'preface',
    'prefaceinfo',
    'primary',
    'primaryie',
    'printhistory',
    'procedure',
    'production',
    'productionrecap',
    'productionset',
    'productname',
    'productnumber',
    'programlisting',
    'programlistingco',
    'prompt',
    'property',
    'pubdate',
    'publisher',
    'publishername',
    'pubsnumber',
    'qandadiv',
    'qandaentry',
    'qandaset',
    'question',
    'quote',
    'refclass',
    'refdescriptor',
    'refentry',
    'refentryinfo',
    'refentrytitle',
    'reference',
    'referenceinfo',
    'refmeta',
    'refmiscinfo',
    'refname',
    'refnamediv',
    'refpurpose',
    'refsect1',
    'refsect1info',
    'refsect2',
    'refsect2info',
    'refsect3',
    'refsect3info',
    'refsection',
    'refsectioninfo',
    'refsynopsisdiv',
    'refsynopsisdivinfo',
    'releaseinfo',
    'remark',
    'replaceable',
    'returnvalue',
    'revdescription',
    'revhistory',
    'revision',
    'revnumber',
    'revremark',
    'rhs',
    'row',
    'sbr',
    'screen',
    'screenco',
    'screeninfo',
    'screenshot',
    'secondary',
    'secondaryie',
    'sect1',
    'sect1info',
    'sect2',
    'sect2info',
    'sect3',
    'sect3info',
    'sect4',
    'sect4info',
    'sect5',
    'sect5info',
    'section',
    'sectioninfo',
    'see',
    'seealso',
    'seealsoie',
    'seeie',
    'seg',
    'seglistitem',
    'segmentedlist',
    'segtitle',
    'seriesvolnums',
    'set',
    'setindex',
    'setindexinfo',
    'setinfo',
    'sgmltag',
    'shortaffil',
    'shortcut',
    'sidebar',
    'sidebarinfo',
    'simpara',
    'simplelist',
    'simplemsgentry',
    'simplesect',
    'spanspec',
    'state',
    'step',
    'stepalternatives',
    'street',
    'structfield',
    'structname',
    'subject',
    'subjectset',
    'subjectterm',
    'subscript',
    'substeps',
    'subtitle',
    'superscript',
    'surname',
    'svg:svg',
    'symbol',
    'synopfragment',
    'synopfragmentref',
    'synopsis',
    'systemitem',
    'table',
    'task',
    'taskprerequisites',
    'taskrelated',
    'tasksummary',
    'tbody',
    'td',
    'term',
    'termdef',
    'tertiary',
    'tertiaryie',
    'textdata',
    'textobject',
    'tfoot',
    'tgroup',
    'th',
    'thead',
    'tip',
    'title',
    'titleabbrev',
    'toc',
    'tocback',
    'tocchap',
    'tocentry',
    'tocfront',
    'toclevel1',
    'toclevel2',
    'toclevel3',
    'toclevel4',
    'toclevel5',
    'tocpart',
    'token',
    'tr',
    'trademark',
    'type',
    'ulink',
    'uri',
    'userinput',
    'varargs',
    'variablelist',
    'varlistentry',
    'varname',
    'videodata',
    'videoobject',
    'void',
    'volumenum',
    'warning',
    'wordasword',
    'xref',
    'year'
])

tag_error_string = 'XML 태그의 짝이 맞지 않습니다'
notdb_error_string = '<%s>: 알려진 DocBook 태그가 아닙니다'


class NotDocBook(Exception):
    pass


def check_db_tags(name):
    if name == 'KPC_DummyTag':
        pass
    elif name.startswith('placeholder-'):
        # old gnome-doc-utils magic
        pass
    elif (name.startswith('_:item-') or name.startswith('_:link-') or
          name.startswith('_:ulink-')):
        # newer gnome-doc-utils magic
        pass
    elif name not in known_db_tags:
        raise NotDocBook(name)


def start_element(name, attr):
    check_db_tags(name)


def end_element(name):
    check_db_tags(name)


class MarkupDocbookCheck(BaseCheck):
    def check(self, entry, context):
        if not entry.references or '.xml:' not in entry.references[0]:
            # not from an XML file
            return []
        msgid = entry.msgid
        msgstr = entry.msgstr
        if msgid == 'translator-credits':  # gnome-doc-utils magic
            return []
        parser = ParserCreate()
        parser.StartElementHandler = start_element
        parser.EndElementHandler = end_element
        parser.UseForeignDTD(True)
        try:
            parser.Parse('<KPC_DummyTag>' + msgstr + '</KPC_DummyTag>')
        except ExpatError as e:
            return [Error(tag_error_string)]
        except NotDocBook as e:
            return [Error(notdb_error_string % e)]
        return []

name = 'convention/markup-docbook'
description = 'DocBook 마크업의 짝이 맞는지 검사합니다'
checker = MarkupDocbookCheck()
