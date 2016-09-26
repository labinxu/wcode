from docx import Document
from docx.enum.style import WD_STYLE, WD_STYLE_TYPE,WD_BUILTIN_STYLE
def write(docname):
    document = Document()
    styles = document.styles
    #styles.add_style('', WD_STYLE_TYPE.PARAGRAPH)
    #style= WD_STYLE.HYPERLINK
    #print(style)

    #print(str(styles['ListBullet']))

        
    document.add_heading('Document Tile',0)
    p = document.add_paragraph('A plain paragraph having some ')
    #for style in WD_STYLE.__members__:
    for style in styles:
        print(style.name)
        if(style.name == 'HYPERLINK'):
            print('find')
            p.add_run('xxx').style=style
            break
    run = p.add_run('bold').bold = True
    
    p.add_run('italic.').italic = True
    #p.add_hyperlink(text='foobar', url='http://github.com')
    document.add_heading('Heading, level 1', level=1)
    #document.add_paragraph('Intense quote', style=style)
    document.add_paragraph(
        'first item in unordered list', style='ListBullet')
    
    # document.add_paragraph(
    #     'xxx', style=styles['Citation'])
    
    document.add_paragraph(
        'first item in ordered list', style='ListNumber')

    document.add_page_break()
    document.save(docname)
