import mkplan

def test_get_jiraid():
    print('test_get_jiraid')
    url, jiraid = mkplan.get_jiraid('# =HYPERLINK("https://jira01.devtools.intel.com/browse/OAM-37493","OAM-37493")')
    print(jiraid)
    print(url)

test_get_jiraid()
