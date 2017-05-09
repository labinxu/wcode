# -*- coding:utf-8 -*-
'''
title="Personal Queries/ReleaseContent_XMM7360" 
https://utpreloaded.rds.intel.com/CqUtpSms/?Query=149956"

<a href="javascript:__doPostBack(&#39;ctl00$cphToolbox$ctlToolbox$lvwStaticToolbox$ctrl0$ctlQueryTreeView$tvwQueryTreeView&#39;,&#39;sRecent\\27941466&#39;)" onclick="TreeView_SelectNode(ctl00_cphToolbox_ctlToolbox_lvwStaticToolbox_ctrl0_ctlQueryTreeView_tvwQueryTreeView_Data, this,&#39;ctl00_cphToolbox_ctlToolbox_lvwStaticToolbox_ctrl0_ctlQueryTreeView_tvwQueryTreeViewt2&#39;);" title="Personal Queries/ReleaseContent_XMM7360" id="ctl00_cphToolbox_ctlToolbox_lvwStaticToolbox_ctrl0_ctlQueryTreeView_tvwQueryTreeViewt2i" tabindex="-1">
'''
import os
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
'''
<table class="iframe_tab iframe_tab_active_default iframe_tab_selected" tabid="2ad1340b-fa54-49d9-be0f-91922b38a969" cellpadding="0" cellspacing="0" title="[sautter]/Personal Queries/ReleaseContent_XMM7360">
      <tbody><tr>
        <td class="tab_left"></td>
        <td class="tab_center" onclick="$find(&quot;ctl00_cphMain_ctlTabContainer_sctTabContainer&quot;).switchTab(&quot;2ad1340b-fa54-49d9-be0f-91922b38a969&quot;);"><img id="imgIcon" class="tab_icon_resultset" src="/CqUtpSms/Handlers/Master/Expires.ashx?version=1.16.3.1003&amp;url=%2fCqUtpSms%2fThemes%2fIntel%2fImages%2fLayout%2ftrans.gif" style="margin-right:5px;" alt=""></td>
        <td class="tab_center" style="overflow:hidden;" onclick="$find(&quot;ctl00_cphMain_ctlTabContainer_sctTabContainer&quot;).switchTab(&quot;2ad1340b-fa54-49d9-be0f-91922b38a969&quot;);"> 
          <span titleid="2ad1340b-fa54-49d9-be0f-91922b38a969">ReleaseCon...</span>
          <div style="height:0px; width:110px;"></div>
        </td>
        <td class="tab_center" style="width:10px" align="center" onclick="$find(&quot;ctl00_cphMain_ctlTabContainer_sctTabContainer&quot;).closeTab(&quot;2ad1340b-fa54-49d9-be0f-91922b38a969&quot;);" title="Close">
          <a href="#" title="Close">X</a>
        </td>
        <td class="tab_right"></td>
      </tr>
    </tbody></table>
    
    #ctl00_cphToolbar_ctlToolbar_lvwToolbarRight_ctrl10_btnExportXml
    <input type="image" name="ctl00$cphToolbar$ctlToolbar$lvwToolbarRight$ctrl10$btnExportXml" id="ctl00_cphToolbar_ctlToolbar_lvwToolbarRight_ctrl10_btnExportXml" title="Export (XML)" class="toolbar_button_xml toolbar_button_xml_mousedown toolbar_button_xml_mouseup" usesubmitbehavior="false" onmousedown="$(this).addClass('toolbar_button_xml_mousedown');  return true;" onmouseup="$(this).addClass('toolbar_button_xml_mouseup');  return true;" src="/CqUtpSms/Handlers/Master/Expires.ashx?version=1.16.3.1003&amp;url=%2fCqUtpSms%2fThemes%2fIntel%2fImages%2fLayout%2ftrans.gif" onclick="Sys.WebForms.PageRequestManager.getInstance().add_pageLoaded(handleDownloadExport);" style="height:16px;width:16px;border-width:0px;margin-right:5px;">
'''
import time
def test_IE():
    iedriver = r"IEDriverServer.exe"
    os.environ["webdriver.ie.driver"] = iedriver
    capbilitest = DesiredCapabilities()
    driver = webdriver.Ie(iedriver)
#driver.get("https://utpreloaded.rds.intel.com/CqUtpSms/?Query=149956")
#tags = driver.find_elements_by_css_selector('table[title="[sautter]/Personal Queries/ReleaseContent_XMM7360"]')
#print(len(tags))
#for link in tags:
#    print(link.get_attribute("class"))
#    spans = link.find_elements_by_css_selector('span')
#    if "ReleaseCon" in spans[0].text:
#        print("Click %s"%spans[0].text)
#        spans[0].click()
#        time.sleep(1)

    driver.get("https://utpreloaded.rds.intel.com/CqUtpSms/?Query=149956#")
    open('qery.html', 'w').write(driver.page_source)
    frames = driver.find_elements_by_css_selector('iframe')
    for frame in frames:
        driver.switch_to_frame(frame)

    print('===============')
    exportTags = driver.find_elements_by_css_selector('input')
    for export in exportTags:
        if 'btnExportXml' in export.get_attribute("name"):
            export.click()
            break
    time.sleep(20)
    alert = driver.switch_to_alert()
    print(alert.text)
def test_chrome():
    driver=webdriver.Chrome()  #
    driver.get('https://www.baidu.com')
    print driver.title
    driver.quit()

def test_firefox():
    from selenium.webdriver.common.keys import Keys
    driver = webdriver.Firefox()
    driver.get("https://utpreloaded.rds.intel.com/CqUtpSms/?Query=149956#")
    frames = driver.find_elements_by_css_selector('iframe')
    for frame in frames:
        driver.switch_to_frame(frame)

    print('===============')
    exportTags = driver.find_elements_by_css_selector('input')
    for export in exportTags:
        if 'btnExportXml' in export.get_attribute("name"):
            export.click()
            break

test_firefox()
    #export.click()
#        break
#driver.close()
#driver.quit()

#from selenium import webdriver
#from time import sleep

#options = webdriver.ChromeOptions()
#prefs = {'profile.default_content_settings.popups': 0, 'download.default_directory': '.'}
#options.add_experimental_option('prefs', prefs)
#
#driver = webdriver.Chrome(executable_path='D:\\chromedriver.exe', chrome_options=options)
#driver.get('http://sahitest.com/demo/saveAs.htm')
#driver.find_element_by_xpath('//a[text()="testsaveas.zip"]').click()
#sleep(3)
#driver.quit()
